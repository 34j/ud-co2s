from datetime import datetime
from pathlib import Path
from typing import Annotated

import plotext as plt
import typer
from rich.console import Console

from ._main import read_co2

app = typer.Typer()


@app.command()
def _main(
    once: Annotated[bool, typer.Option(help="Only get values once")] = False,
    plot: Annotated[bool, typer.Option(help="Plot the values")] = False,
    log: Annotated[bool, typer.Option(help="Log the values")] = False,
    log_path: Annotated[Path, typer.Option(help="Path to the log file")] = Path(
        "ud-co2s.log"
    ),
) -> None:
    c = Console()
    if plot:
        dates = []
        ppms = []
    for data in read_co2(1 if once else None):
        c.clear()
        c.print(
            f"CO2: {data.co2_ppm} ppm, "
            f"Humidity: {data.humidity_percent}%, "
            f"Temperature: {data.temperature}°C"
        )
        if log:
            with log_path.open("a") as file:
                file.write(
                    f"{datetime.now().astimezone().isoformat()},{data.co2_ppm},"
                    f"{data.humidity_percent},{data.temperature}\n"
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
                    pass
