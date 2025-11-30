from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable, Label
from textual.binding import Binding
from textual.containers import Vertical
from textual_plotext import PlotextPlot
from blackstat.models.models import Product, PriceTransaction
from blackstat.models.crud import get_prices_for_product, create_price_transaction, update_price_transaction, delete_price_transaction
from blackstat.views.price_form import PriceForm

class ProductDetailView(Screen):
    """Screen to view product details, graph, and price history."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("a", "add_price", "Add Price"),
        Binding("e", "edit_price", "Edit Price"),
        Binding("d", "delete_price", "Delete Price"),
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
            plt.plot(dates, values)
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
        if not table.cursor_row_key:
            self.notify("No price selected", severity="warning")
            return
            
        # We need to find the transaction object. 
        # Since we only have the ID in the key, we'll fetch all and find it, or fetch by ID.
        # But our CRUD has get_prices_for_product. 
        # Let's just fetch all and filter, or add a get_price_transaction to CRUD.
        # For now, I'll iterate the current list in memory if I had it, but I don't store it.
        # I'll rely on the table key which is the ID.
        
        transaction_id = int(table.cursor_row_key.value)
        # I need a get_price_transaction function in CRUD.
        # I'll add it to CRUD later. For now, I'll hack it by fetching all.
        prices = get_prices_for_product(self.product.id)
        transaction = next((p for p in prices if p.id == transaction_id), None)
        
        if transaction:
            def handle_edit(updated_transaction: PriceTransaction | None) -> None:
                if updated_transaction:
                    update_price_transaction(updated_transaction)
                    self.refresh_data()
            
            self.app.push_screen(PriceForm(self.product.id, transaction), handle_edit)

    def action_delete_price(self) -> None:
        table = self.query_one("#price_table", DataTable)
        if not table.cursor_row_key:
            self.notify("No price selected", severity="warning")
            return

        transaction_id = int(table.cursor_row_key.value)
        delete_price_transaction(transaction_id)
        self.refresh_data()
        self.notify("Price deleted")
