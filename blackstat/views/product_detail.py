from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable, Label
from textual.binding import Binding
from textual.containers import Vertical
from textual_plotext import PlotextPlot
from blackstat.models.models import Product, PriceTransaction
from blackstat.models.crud import get_prices_for_product, create_price_transaction, update_price_transaction, delete_price_transaction
from blackstat.views.price_form import PriceForm
from blackstat.agent import find_product_price
import asyncio

class ProductDetailView(Screen):
    """Screen to view product details, graph, and price history."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("a", "add_price", "Add Price"),
        Binding("e", "edit_price", "Edit Price"),
        Binding("d", "delete_price", "Delete Price"),
        Binding("u", "copy_url", "Copy URL"),
        Binding("n", "copy_name", "Copy Name"),
        Binding("c", "check_price", "Check Price (AI)"),
    ]

    def __init__(self, product: Product):
        super().__init__()
        self.product = product

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(f"Product: {self.product.name} ({self.product.url})", id="product_label")
        yield PlotextPlot(id="price_graph")
        yield DataTable(cursor_type="row", id="price_table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#price_table", DataTable)
        table.add_columns("ID", "Date", "Price", "Source")
        self.refresh_data()
        table.focus()

    def refresh_data(self) -> None:
        prices = get_prices_for_product(self.product.id)
        
        # Update Table
        table = self.query_one("#price_table", DataTable)
        table.clear()
        for price in prices:
            table.add_row(
                str(price.id),
                str(price.date),
                str(price.price),
                price.source_url,
                key=str(price.id)
            )

        # Update Graph
        plt = self.query_one("#price_graph", PlotextPlot).plt
        plt.clear_data()
        plt.title(f"Price History for {self.product.name}")
        
        if prices:
            # Sort by date for the graph
            sorted_prices = sorted(prices, key=lambda p: p.date)
            dates = [p.date.strftime("%Y-%m-%d %H:%M") for p in sorted_prices]
            values = [p.price for p in sorted_prices]
            plt.date_form("Y-m-d H:M")
            plt.plot(dates, values)
            plt.ylim(0, max(values) * 1.1)
            plt.xlabel("Date")
            plt.ylabel("Price")
        
        self.query_one("#price_graph", PlotextPlot).refresh()

    def action_add_price(self) -> None:
        def handle_add(transaction: PriceTransaction | None) -> None:
            if transaction:
                create_price_transaction(transaction)
                self.refresh_data()
        
        self.app.push_screen(PriceForm(self.product.id), handle_add)

    def action_edit_price(self) -> None:
        table = self.query_one("#price_table", DataTable)
        if table.cursor_coordinate.row < 0:
            self.notify("No price selected", severity="warning")
            return
            
        row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
        transaction_id = int(row_key.value)
        
        prices = get_prices_for_product(self.product.id)
        transaction = next((p for p in prices if p.id == transaction_id), None)
        
        if transaction:
            def handle_edit(updated_transaction: PriceTransaction | None) -> None:
                if updated_transaction:
                    try:
                        update_price_transaction(updated_transaction)
                        self.refresh_data()
                        self.notify("Price updated")
                    except Exception as e:
                        self.notify(f"Error updating price: {e}", severity="error")
            
            self.app.push_screen(PriceForm(self.product.id, transaction), handle_edit)

    def action_delete_price(self) -> None:
        table = self.query_one("#price_table", DataTable)
        if table.cursor_coordinate.row < 0:
            self.notify("No price selected", severity="warning")
            return

        row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
        transaction_id = int(row_key.value)
        delete_price_transaction(transaction_id)
        self.refresh_data()
        self.notify("Price deleted")

    def action_copy_url(self) -> None:
        self.app.copy_to_clipboard(self.product.url)
        self.notify(f"Copied URL: {self.product.url}")

    def action_copy_name(self) -> None:
        self.app.copy_to_clipboard(self.product.name)
        self.notify(f"Copied Name: {self.product.name}")

    async def action_check_price(self) -> None:
        self.notify("Searching for price... this may take a moment.")
        
        # Run the agent in a worker to avoid blocking the UI too much
        # Although find_product_price is async, the agent might do blocking calls internally or we just want to be safe
        result = await find_product_price(self.product.name)
        
        if result:
            self.notify(f"Found price: {result.price} {result.currency}")
            
            # Create new transaction
            transaction = PriceTransaction(
                product_id=self.product.id,
                price=result.price,
                source_url=result.source_url
            )
            create_price_transaction(transaction)
            self.refresh_data()
        else:
            self.notify("Could not find a price.", severity="error")
