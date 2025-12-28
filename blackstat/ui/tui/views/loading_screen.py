from textual.screen import ModalScreen
from textual.widgets import Label, LoadingIndicator
from textual.containers import Vertical, Center

class LoadingScreen(ModalScreen):
    """A modal screen that shows a loading indicator and a message."""

    def __init__(self, message: str = "Loading..."):
        super().__init__()
        self.message = message

    def compose(self):
        with Center():
            with Vertical(id="loading-container"):
                yield LoadingIndicator()
                yield Label(self.message, id="loading-message")

    def on_mount(self):
        self.query_one("#loading-container").styles.background = "rgb(40, 40, 40)"
        self.query_one("#loading-container").styles.border = ("heavy", "white")
        self.query_one("#loading-container").styles.padding = (2, 4)
        self.query_one("#loading-container").styles.width = "auto"
        self.query_one("#loading-container").styles.height = "auto"
        self.query_one("#loading-message").styles.text_align = "center"
        self.query_one("#loading-message").styles.margin = (2, 0, 0, 0)
