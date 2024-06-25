from typing import Annotated

import typer

from ._main import read_co2

app = typer.Typer()


@app.command()
def _main(
    once: Annotated[bool, typer.Option("--once", "-o", help="Only print one value")]
) -> None:
    for data in read_co2():
        typer.echo(data)
        if once:
            break
