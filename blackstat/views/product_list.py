from textual.app import ComposeResult
from textual.widgets import Static, DataTable
from textual.binding import Binding
from textual import on
from blackstat.models.crud import get_all_products, create_product, update_product, delete_product, get_product
from blackstat.views.product_form import ProductForm
from blackstat.views.product_detail import ProductDetailView
from blackstat.models.models import Product

class ProductListView(Static):
    """A widget to display a list of products."""

    BINDINGS = [
        Binding("a", "add_product", "Add Product"),
        Binding("e", "edit_product", "Edit Product"),
        Binding("d", "delete_product", "Delete Product"),
        Binding("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield DataTable(cursor_type="row")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("ID", "Name", "URL", "Created At")
        self.refresh_products()
        table.focus()

    def refresh_products(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        products = get_all_products()
        for product in products:
            table.add_row(
                str(product.id),
                product.name,
                product.url,
                str(product.created_at),
                key=str(product.id)
            )

    def action_add_product(self) -> None:
        def handle_add(product: Product | None) -> None:
            if product:
                create_product(product)
                self.refresh_products()
        
        self.app.push_screen(ProductForm(), handle_add)

    def action_edit_product(self) -> None:
        table = self.query_one(DataTable)
        if table.cursor_coordinate.row < 0:
            self.notify("No product selected", severity="warning")
            return
            
        row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
        product_id = int(row_key.value)
        product = get_product(product_id)
        
        if product:
            def handle_edit(updated_product: Product | None) -> None:
                if updated_product:
                    try:
                        update_product(updated_product)
                        self.refresh_products()
                        self.notify("Product updated")
                    except Exception as e:
                        self.notify(f"Error updating product: {e}", severity="error")
            
            self.app.push_screen(ProductForm(product), handle_edit)

    def action_delete_product(self) -> None:
        table = self.query_one(DataTable)
        if table.cursor_coordinate.row < 0:
            self.notify("No product selected", severity="warning")
            return

        row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
        product_id = int(row_key.value)
        delete_product(product_id)
        self.refresh_products()
        self.notify("Product deleted")

    def action_refresh(self) -> None:
        self.refresh_products()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        product_id = int(event.row_key.value)
        product = get_product(product_id)
        if product:
            self.app.push_screen(ProductDetailView(product))

