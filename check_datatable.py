from textual.app import App, ComposeResult
from textual.widgets import DataTable

class TestApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("A", "B")
        k1 = table.add_row("1", "2", key="k1")
        k2 = table.add_row("3", "4", key="k2")
        table.cursor_coordinate = (1, 0) # Select second row
        
        with open("output.txt", "w") as f:
            f.write(f"Cursor Row Index: {table.cursor_row}\n")
            
            try:
                # ordered_rows returns a list of RowKey objects or similar?
                # Let's inspect what it returns
                rows = table.ordered_rows
                f.write(f"Ordered Rows Type: {type(rows)}\n")
                if rows:
                    f.write(f"Row 0: {rows[0]}\n")
                    f.write(f"Row 0 type: {type(rows[0])}\n")
                    # If it's a RowKey, it might be the key itself
                    f.write(f"Key at index 1: {rows[1]}\n")
            except Exception as e:
                f.write(f"Ordered rows failed: {e}\n")

            try:
                cell_key = table.coordinate_to_cell_key(table.cursor_coordinate)
                row_key = cell_key.row_key
                f.write(f"Row Key: {row_key}\n")
                f.write(f"Row Key Type: {type(row_key)}\n")
                f.write(f"Row Key Dir: {dir(row_key)}\n")
                if hasattr(row_key, "value"):
                    f.write(f"Row Key Value: {row_key.value}\n")
            except Exception as e:
                f.write(f"Coordinate to cell key failed: {e}\n")

        self.exit()

if __name__ == "__main__":
    TestApp().run()
