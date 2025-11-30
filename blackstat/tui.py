from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.binding import Binding
from .views.product_list import ProductListView

class BlackStatterApp(App):
    """A Textual app to track product prices."""

    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield ProductListView()
        yield Footer()

    def action_quit(self) -> None:
        self.exit()
