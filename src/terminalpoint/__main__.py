import sys
from pathlib import Path
from typing import Optional

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

import typer

from terminalpoint import __version__
from terminalpoint.app import Presentation

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"{__version__}")
        raise typer.Exit()


@app.command()
def run(
    presentation: Path = typer.Argument(
        file_okay=True,
        dir_okay=False,
        exists=True,
        help="Path to the presentation file.",
    ),
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    """Display a presentation"""
    _ = version
    Presentation(file=presentation).run()


if __name__ == "__main__":
    app()
