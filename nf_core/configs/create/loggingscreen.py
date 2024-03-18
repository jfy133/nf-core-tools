from textwrap import dedent

from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Markdown, Static

markdown = """
Visualising logging output.
"""


class LoggingScreen(Screen):
    """A screen to show the final logs."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Markdown(
            dedent(
                """
                # Logging
                """
            )
        )
        yield Static(
            f"\n[green]{' ' * 40},--.[grey39]/[green],-."
            + "\n[blue]        ___     __   __   __   ___     [green]/,-._.--~\\"
            + "\n[blue]|\ | |__  __ /  ` /  \ |__) |__      [yellow]   }  {"
            + "\n[blue]   | \| |       \__, \__/ |  \ |___     [green]\`-._,-`-,"
            + "\n[green]                                       `._,._,'\n",
            id="logo",
        )
        yield Markdown(markdown)
        yield Center(self.parent.LOG_HANDLER.console)
        if self.parent.LOGGING_STATE == "config created":
            yield Center(
                Button("Close App", id="close_app", variant="success"),
                classes="cta",
            )
        else:
            yield Center(
                Button("Continue", id="close_screen", variant="success", disabled=True),
                classes="cta",
            )
