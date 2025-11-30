from datetime import datetime
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label
from textual.containers import Grid
from blackstat.models.models import PriceTransaction

class PriceForm(ModalScreen[PriceTransaction]):
    """A screen to add or edit a price transaction."""

    def __init__(self, product_id: int, transaction: PriceTransaction = None):
        super().__init__()
        self.product_id = product_id
        self.transaction = transaction

    def compose(self) -> ComposeResult:
        current_price = str(self.transaction.price) if self.transaction else ""
        current_url = self.transaction.source_url if self.transaction else ""
        
        yield Grid(
            Label("Price:"),
            Input(value=current_price, id="price", type="number"),
            Label("Source URL:"),
            Input(value=current_url, id="source_url"),
            Button("Save", variant="primary", id="save"),
            Button("Cancel", variant="error", id="cancel"),
            id="dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            try:
                price = float(self.query_one("#price", Input).value)
            except ValueError:
                self.notify("Invalid price", severity="error")
                return

            source_url = self.query_one("#source_url", Input).value
            
            if self.transaction:
                self.transaction.price = price
                self.transaction.source_url = source_url
                self.dismiss(self.transaction)
            else:
                self.dismiss(PriceTransaction(
                    product_id=self.product_id,
                    price=price,
                    source_url=source_url,
                    date=datetime.now()
                ))
        elif event.button.id == "cancel":
            self.dismiss(None)
