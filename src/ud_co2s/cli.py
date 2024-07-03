import threading
from datetime import datetime
from logging import getLogger
from pathlib import Path
from typing import Annotated

import numpy as np
import plotext as plt
import seaborn as sns
import typer
import unhandled_exit
from PIL import Image, ImageDraw, ImageFont
from rich.console import Console

from ._main import CO2Data, read_co2

LOG = getLogger(__name__)
try:
    import pystray
except Exception as e:
    LOG.exception(e)
global pystray_icon
global current_data
current_data: CO2Data
pystray_icon: "pystray.Icon"
app = typer.Typer()


def _create_icon_image(value: int, *, width: int = 64, height: int = 64) -> Image:
    # create image
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
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
        dates = []
        ppms = []
    for data in read_co2(count=1 if once else None, port=None if port == "" else port):
        c.clear()
        c.print(
            f"CO2: {data.co2_ppm} ppm, "
            f"Humidity: {data.humidity_calibrated:.1f}%, "
            f"Temperature: {data.temperature_calibrated:.1f}°C"
        )
        if log:
            with log_path.open("a") as file:
                file.write(
                    f"{datetime.now().astimezone().isoformat()},{data.co2_ppm},"
                    f"{data.humidity_calibrated},{data.temperature_calibrated},"
                    f"{data.humidity},{data.temperature}\n"
                )
        if plot:
            ppms.append(data.co2_ppm)
            dates.append(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            if len(ppms) > 2:
                try:
                    plt.clear_figure()
                    plt.canvas_color("black")
                    plt.axes_color("black")
                    plt.ticks_color("white")
                    plt.plot_size(height=(plt.terminal_height() or 10) - 2)
                    plt.date_form("Y/m/d H:M:S")
                    plt.plot(dates, ppms)
                    plt.show()
                except Exception as e:
                    c.print(e)
        if icon:
            global pystray_icon
            global current_data
            current_data = data
            pystray_icon.icon = _create_icon_image(data.co2_ppm)
            if pystray_icon.HAS_NOTIFICATION:
                pystray_icon.remove_notification()
                if data.co2_ppm > notify_ppm:
                    pystray_icon.notify(f"CO2: {data.co2_ppm} ppm")


@app.command()
def _main(
    once: Annotated[bool, typer.Option(help="Only get values once")] = False,
    plot: Annotated[bool, typer.Option(help="Plot the values")] = False,
    log: Annotated[bool, typer.Option(help="Log the values")] = False,
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
