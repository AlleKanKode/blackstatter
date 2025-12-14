from nicegui import ui
from blackstat.ui.nicegui.layout import layout
from blackstat.models.crud import get_all_products, create_product, delete_product
from blackstat.models.product import Product

@ui.page('/')
def home_page():
    with layout():
        # Helper to refresh the list
        def refresh_grid():
            products_container.clear()
            with products_container:
                products = get_all_products()
                if not products:
                    ui.label("No products found.").classes("text-grey italic")
                    return
                
                with ui.grid(columns=3).classes('w-full gap-4'):
                    for p in products:
                        with ui.card().classes('w-full hover:shadow-lg transition-shadow'):
                            with ui.row().classes('justify-between items-center w-full'):
                                ui.link(p.name, f'/product/{p.id}').classes('text-lg font-bold text-primary no-underline')
                                ui.button(icon='delete', color='negative', on_click=lambda id=p.id: delete_and_refresh(id)).props('flat')
                            
                            ui.link(p.url, p.url, new_tab=True).classes('text-sm text-grey truncate w-full block mb-2')
                            
        def delete_and_refresh(product_id):
            delete_product(product_id)
            ui.notify(f'Product {product_id} deleted', color='info')
            refresh_grid()

        async def add_product_dialog():
            with ui.dialog() as dialog, ui.card():
                ui.label('Add Product').classes('text-xl font-bold')
                name = ui.input('Name').classes('w-full')
                url = ui.input('URL').classes('w-full')
                
                def save():
                    if not name.value or not url.value:
                        ui.notify('Please fill all fields', color='warning')
                        return
                    create_product(Product(name=name.value, url=url.value))
                    ui.notify('Product added', color='positive')
                    dialog.close()
                    refresh_grid()

                with ui.row().classes('justify-end w-full mt-4'):
                    ui.button('Cancel', on_click=dialog.close).props('flat')
                    ui.button('Save', on_click=save)
            
            dialog.open()

        # Header Actions
        with ui.row().classes('w-full justify-between items-center mb-6'):
            ui.label('Product Dashboard').classes('text-3xl font-light text-white')
            ui.button('Add Product', icon='add', on_click=add_product_dialog).props('unelevated color=secondary')

        # Content defined inside the layout context
        products_container = ui.column().classes('w-full')
        refresh_grid()
