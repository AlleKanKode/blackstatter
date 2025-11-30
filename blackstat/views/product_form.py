from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label
from textual.containers import Grid
from blackstat.models.models import Product

class ProductForm(ModalScreen[Product]):
    """A screen to add or edit a product."""

    def __init__(self, product: Product = None):
        super().__init__()
        self.product = product

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Name:"),
            Input(value=self.product.name if self.product else "", id="name"),
            Label("URL:"),
            Input(value=self.product.url if self.product else "", id="url"),
            Button("Save", variant="primary", id="save"),
            Button("Cancel", variant="error", id="cancel"),
            id="dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            try:
                name = self.query_one("#name", Input).value
                url = self.query_one("#url", Input).value
                
                if self.product:
                    self.product.name = name
                    self.product.url = url
                    self.dismiss(self.product)
                else:
                    self.dismiss(Product(name=name, url=url))
            except Exception as e:
                self.notify(f"Error saving product: {e}", severity="error")
        elif event.button.id == "cancel":
            self.dismiss(None)
