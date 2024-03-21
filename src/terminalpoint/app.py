import os
import re
import subprocess
from os import system

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
        Binding("q", "quit", "Quit", key_display="q"),
        Binding("h", "previous_slide", "Previous Slide", key_display="h"),
        Binding("l", "next_slide", "Next Slide", key_display="l"),
        Binding("p", "python", "Python", key_display="p"),
        Binding("s", "shell", "Shell", key_display="s"),
    ]

    def __init__(self, slides: str):
        super().__init__()
        _slides = re.split(r"^-+$", slides, flags=re.MULTILINE)
        self.slides: list[str] = _slides

    def compose(self) -> ComposeResult:
        yield Markdown(self.slides[0], id="slide")
        yield Footer()

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
    app = Presentation(default_slide)
    app.run()
