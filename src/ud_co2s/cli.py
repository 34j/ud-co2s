from __future__ import annotations

import threading
from datetime import datetime
from logging import getLogger
from pathlib import Path
from typing import Annotated

import numpy as np
import pandas as pd
import plotext as plt
import seaborn as sns
import typer
import unhandled_exit
from PIL import Image, ImageDraw, ImageFont
from rich.console import Console
from thermofeel import (
    calculate_heat_index_simplified,
    celsius_to_kelvin,
    kelvin_to_celsius,
)

from ._main import CO2Data, read_co2

LOG = getLogger(__name__)
try:
    import pystray
except Exception as e:
    LOG.exception(e)
global pystray_icon
global current_data
current_data: CO2Data
pystray_icon: pystray.Icon
app = typer.Typer()


def _create_icon_image(
    value: int,
    *,
    width: int = 64,
    height: int = 64,
    background_color: float | tuple[float, ...] | str | None = 0,
) -> Image.Image:
    # create image
    image = Image.new("RGBA", (width, height), background_color)
    dc = ImageDraw.Draw(image)

    # load font
    font = ImageFont.load_default(40)

    # set color based on value
    palette = sns.color_palette("Spectral", as_cmap=True)
    color = palette(1 - np.clip((value - 440) / 1000, 0.0, 1.0))
    color = tuple(int(255 * c) for c in color)

    # draw text
    two_lines = value >= 1000
    if two_lines:
        margin = (-4, -8)
        dc.text((margin[0], margin[1]), f"{value // 100:0>2}", fill=color, font=font)
        dc.text(
            (margin[0], 32 + margin[1]), f"{value % 100:0>2}", fill=color, font=font
        )
    else:
        dc.text((-4, 15), f"{value}", fill=color, font=font)

    # return image
    return image


def _main_task(
    once: bool,
    plot: bool,
    log: bool,
    log_path: Path,
    port: str,
    icon: bool,
    notify_ppm: int,
) -> None:
    c = Console()
    if plot:
        dates: list[datetime] = []
        dates_formatted: list[str] = []
        ppms: list[int] = []
        # data_hist = pd.read_csv(log_path, header=None,
        # names=["date", "co2", "humidity", "temperature",
        # "humidity_raw", "temperature_raw"])
    for data in read_co2(count=1 if once else None, port=None if port == "" else port):
        c.clear()
        ppm_diff_per_hour = 0.0
        RMR_est = 0.0
        ventelation_per_hour = 0.0
        if plot and len(ppms) > 0:
            diff_time = pd.Timedelta("1min")
            dates_ = np.array(dates[-100:])
            ppms_ = np.array(ppms[-100:])

            diffs = np.abs(pd.Timestamp.now() - np.array(dates_) - diff_time)
            diff_time_before_idx = np.argmin(diffs)
            diff_time_before = diffs[diff_time_before_idx] + diff_time
            diff_time_before_ppm = ppms_[diff_time_before_idx]
            ppm_diff = data.co2_ppm - diff_time_before_ppm
            ppm_diff_per_hour = ppm_diff / (diff_time_before / pd.Timedelta("1h"))

            n_tatami_mats = 6
            n_human = 1
            v = 1.62 * 2.44 * n_tatami_mats

            # estimated RMR
            co2_per_hour_est = ppm_diff_per_hour * 1e-6 * v
            RMR_est = co2_per_hour_est / 0.0132 / n_human - 1

            # estimated ventilation per hour
            RMR = 0
            co2_per_hour = (RMR + 1) * 0.0132 * n_human
            out_ppm = 440
            ventelation_per_hour = (
                (co2_per_hour - co2_per_hour_est) / (data.co2_ppm - out_ppm) * 1e6
            )
        heat_index = kelvin_to_celsius(
            calculate_heat_index_simplified(
                np.array([celsius_to_kelvin(data.temperature_calibrated)]),
                np.array([data.humidity_calibrated]),
            )[0]
        )
        heat_index_level = {
            float("-inf"): ("OK", "ffffff"),
            27: ("Caution", "ffff66"),
            32: ("Extreme caution", "ffd700"),
            41: ("Danger", "ff8c00"),
            54: ("Extreme danger", "ff0000"),
        }
        heat_index_level_idx = max(
            [level for level in heat_index_level if heat_index >= level]
        )
        heat_index_level_name, heat_index_level_color = heat_index_level[
            heat_index_level_idx
        ]
        # net = kelvin_to_celsius(calculate_normal_effective_temperature(
        # celsius_to_kelvin(data.temperature_calibrated), 0, data.humidity_calibrated))
        c.print(
            f"CO2: {data.co2_ppm} ppm, "
            f"Heat Index: [#{heat_index_level_color}]"
            f"{heat_index:.1f} \\[{heat_index_level_name}][/], "
            f"Humidity: {data.humidity_calibrated:.1f}%, "
            f"Temperature: {data.temperature_calibrated:.1f}°C"
            + (
                f", PPM Diff: {ppm_diff_per_hour:.1f} ppm/h, "
                f"RMR: {RMR_est:.1f}, "
                f"Ventelation: {ventelation_per_hour:.1f} m^3/h"
                if plot
                else ""
            )
        )
        if log:
            with log_path.open("a") as file:
                file.write(
                    f"{datetime.now().astimezone().isoformat()},{data.co2_ppm},"
                    f"{data.humidity_calibrated},{data.temperature_calibrated},"
                    f"{data.humidity},{data.temperature}\n"
                )
                # data_hist.append(
                #     {
                #         "date": datetime.now().astimezone().isoformat(),
                #         "co2": data.co2_ppm,
                #         "humidity": data.humidity_calibrated,
                #         "temperature": data.temperature_calibrated,
                #         "humidity_raw": data.humidity,
                #         "temperature_raw": data.temperature,
                #     }
                # )
        if plot:
            # dates = data_hist["date"].dt.strftime("%Y/%m/%d %H:%M:%S")
            # ppms = data_hist["co2"]
            ppms.append(data.co2_ppm)
            dates.append(pd.Timestamp.now())
            dates_formatted.append(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            if len(ppms) > 1:
                try:
                    plt.clear_figure()
                    plt.canvas_color("black")
                    plt.axes_color("black")
                    plt.ticks_color("white")
                    plt.plot_size(height=(plt.terminal_height() or 10) - 2)
                    plt.date_form("Y/m/d H:M:S")
                    plt.plot(dates_formatted, ppms)
                    plt.show()
                except Exception as e:
                    c.print(e)
        if icon:
            global pystray_icon
            global current_data
            current_data = data
            background_color = (0, 0, 0, 0)
            if pystray_icon.HAS_NOTIFICATION:
                if data.co2_ppm > notify_ppm:
                    background_color = (255, 0, 0, 255)
            pystray_icon.icon = _create_icon_image(
                data.co2_ppm, background_color=background_color
            )
            pystray_icon.title = (
                f"HI: {heat_index:.1f}, "
                f"{data.temperature_calibrated:.1f}°C, {data.humidity_calibrated:.1f}%"
            )


@app.command()
def _main(
    once: Annotated[bool, typer.Option(help="Only get values once")] = False,
    plot: Annotated[bool, typer.Option(help="Plot the values")] = True,
    log: Annotated[bool, typer.Option(help="Log the values")] = True,
    log_path: Annotated[Path, typer.Option(help="Path to the log file")] = Path(
        "ud-co2s.log"
    ),
    port: Annotated[str, typer.Option(help="The serial port to use")] = "",
    icon: Annotated[bool, typer.Option(help="Show the icon")] = True,
    notify_ppm: Annotated[int, typer.Option(help="The CO2 ppm to notify")] = 1000,
) -> None:
    unhandled_exit.activate()
    if icon:
        global pystray_icon
        pystray_icon = pystray.Icon(
            "UD-CO2S", icon=_create_icon_image(0), title="UD-CO2S"
        )
        pystray_icon.menu = pystray.Menu(
            *(
                [
                    pystray.MenuItem(
                        "Notify",
                        lambda: pystray_icon.notify(
                            f"CO2: {current_data.co2_ppm} ppm, "
                            f"Humidity: {current_data.humidity_calibrated:.1f}%, "
                            f"Temperature: {current_data.temperature_calibrated:.1f}°C"
                        ),
                        default=pystray_icon.HAS_DEFAULT_ACTION,
                        # visible=not pystray_icon.HAS_DEFAULT_ACTION,
                    )
                ]
                if pystray_icon.HAS_NOTIFICATION
                else []
            )
            + [
                pystray.MenuItem(
                    "Exit",
                    lambda: pystray_icon.stop(),
                )
            ]
        )
        pystray_icon.update_menu()
        threading.Thread(
            target=_main_task,
            args=(once, plot, log, log_path, port, icon, notify_ppm),
            daemon=True,
        ).start()
        pystray_icon.run()
    else:
        _main_task(once, plot, log, log_path, port, icon, notify_ppm)
