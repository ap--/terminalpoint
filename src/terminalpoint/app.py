import os
import re
import subprocess
import tempfile
from os import system
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import var
from textual.widgets import Footer, Markdown

default_slide = """\
# TerminalPoint
###### please open with a slidedeck ...
"""


class Presentation(App):
    CSS = """
    Screen {
        align: center middle;
    }
    #slide {
       & MarkdownH6 {
           width: 100%;
           text-align: center;
           text-style: none;
           border: none;
           color: $text-muted;
       }
    }
    """
    slide_no: var[int] = var(0)
    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle dark mode", show=False),
        Binding("r", "reload_slides", "Reload slides", show=False),
        Binding("q", "quit", "Quit", key_display="q"),
        Binding("h", "previous_slide", "Previous Slide", key_display="h"),
        Binding("l", "next_slide", "Next Slide", key_display="l"),
        Binding("p", "python", "Python", key_display="p"),
        Binding("s", "shell", "Shell", key_display="s"),
    ]

    def __init__(self, file: Path):
        super().__init__()
        self._file = file
        self._tpre = re.compile(r"^---+$", flags=re.MULTILINE)
        self.slides = self._tpre.split(file.read_text())

    def compose(self) -> ComposeResult:
        yield Markdown(self.slides[self.slide_no], id="slide")
        yield Footer()

    def action_reload_slides(self) -> None:
        self.slides[:] = self._tpre.split(self._file.read_text())
        self.slide_no = min(self.slide_no, len(self.slides) - 1)
        self.query_one("#slide", Markdown).update(self.slides[self.slide_no])

    def action_previous_slide(self) -> None:
        self.slide_no = max(0, self.slide_no - 1)
        self.query_one("#slide", Markdown).update(self.slides[self.slide_no])

    def action_next_slide(self) -> None:
        self.slide_no = min(self.slide_no + 1, len(self.slides) - 1)
        self.query_one("#slide", Markdown).update(self.slides[self.slide_no])

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_python(self) -> None:
        with self.suspend():
            system("clear")
            subprocess.run("python", shell=True)

    def action_shell(self) -> None:
        with self.suspend():
            system("clear")
            subprocess.run(os.getenv("SHELL", "bash"), shell=True)


if __name__ == "__main__":
    with tempfile.NamedTemporaryFile(mode="rw", suffix=".tpt.md") as f:
        f.write(default_slide)
        f.flush()
        app = Presentation(file=Path(f.name))
        app.run()
