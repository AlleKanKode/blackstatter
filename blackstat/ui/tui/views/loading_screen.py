from textual.screen import ModalScreen
from textual.widgets import Label, LoadingIndicator
from textual.containers import Vertical, Center

class LoadingScreen(ModalScreen):
    """A modal screen that shows a loading indicator and a message."""

    DEFAULT_CSS = """
    LoadingScreen {
        align: center middle;
    }

    #loading-container {
        background: $surface;
        border: heavy $primary;
        padding: 2 4;
        width: auto;
        height: auto;
    }

    #loading-message {
        text-align: center;
        margin-top: 2;
    }
    """

    def __init__(self, message: str = "Loading..."):
        super().__init__()
        self.message = message

    def compose(self):
        with Center():
            with Vertical(id="loading-container"):
                yield LoadingIndicator()
                yield Label(self.message, id="loading-message")
