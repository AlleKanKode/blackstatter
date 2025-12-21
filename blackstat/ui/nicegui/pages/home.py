from nicegui import ui
from blackstat.ui.nicegui.layout import layout
from blackstat.models.crud import get_all_products, create_product, delete_product
from blackstat.models.product import Product

# NiceGUI bruger '@ui.page' decoratoren til at håndtere routing.
# Hver gang en bruger besøger '/', bliver 'home_page' funktionen kørt.
@ui.page('/')
def home_page():
    # Denne funktion køres én gang per page-load. Alt defineret herunder er "scoped"
    # til den enkelte klient (browser tab). Det sikrer at brugere ikke deler state ved en fejl.

    # 'with layout():' er en context manager. I NiceGUI bruges 'with' flittigt til at bygge
    # hierarkiet af elementer (dom træet). 
    # Funktionen 'layout' fungerer som en "master template". Den sætter header, footer, 
    # styling (theme) og navigation op. Alt indlejret i denne blok vises i 'main content' 
    # området mellem header og footer (der hvor 'yield' kaldes i layout.py).
    with layout():
        # Helper to refresh the list
        # Helper funktion defineret som "closure" inde i page-funktionen.
        # På den måde har den adgang til lokale variabler som 'products_container'
        # og kan opdatere UI'et for netop denne bruger session.
        def refresh_grid():
            # Opdaterings-mønster: Tøm containeren og genopbyg indholdet.
            products_container.clear()
            
            # 'with products_container:' sikrer at de nye elementer vi opretter nu,
            # bliver placeret inde i denne container og ikke nederst på siden.
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

        # Asynkron funktion til dialoger. NiceGUI understøtter både sync og async handlers.
        async def add_product_dialog():
            # Opretter dialogen men viser den ikke med det samme.
            # 'with' blokken definerer hvad der er INDE i dialogen.
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
        
        # Her opretter vi en tom container (column) som placeholder.
        # Vi gemmer referencen i 'products_container' så vi kan manipulere den senere
        # (f.eks. i 'refresh_grid' funktionen).
        products_container = ui.column().classes('w-full')
        
        # Kald funktionen første gang for at tegne det initielle indhold.
        refresh_grid()
