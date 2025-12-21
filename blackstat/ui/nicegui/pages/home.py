from nicegui import ui, events
from typing import Optional
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
        
        # Grid reference for later access
        grid: Optional[ui.aggrid] = None
        
        async def navigate_to_product(e: events.GenericEventArguments):
            # Only navigate if clicking the name column, not when using checkbox
            if e.args['colId'] == 'name' and e.args['data']:
                ui.navigate.to(f'/product/{e.args["data"]["id"]}')

        async def navigate_on_enter(e: events.GenericEventArguments):
             try:
                 # Check for key in nested structure (requested via args)
                 key = e.args.get('event', {}).get('key')
                 
                 if key == 'Enter':
                     if e.args.get('data'):
                         ui.navigate.to(f'/product/{e.args["data"]["id"]}')
             except Exception as ex:
                 print(f"Error in navigate_on_enter: {ex}")
                 print(f"Args: {e.args}")

        async def delete_selected():
            nonlocal grid
            if not grid: return
            
            rows = await grid.get_selected_rows()
            if not rows:
                ui.notify("No rows selected", color="warning")
                return

            for row in rows:
                delete_product(row['id'])
            
            ui.notify(f"Deleted {len(rows)} products")
            refresh_grid()

        def refresh_grid():
            nonlocal grid
            # Opdaterings-mønster: Tøm containeren og genopbyg indholdet.
            products_container.clear()
            
            # 'with products_container:' sikrer at de nye elementer vi opretter nu,
            # bliver placeret inde i denne container og ikke nederst på siden.
            with products_container:
                products = get_all_products()
                if not products:
                    ui.label("No products found.").classes("text-grey italic")
                    return
                
                # Definér kolonner til AG Grid
                column_defs = [
                    {'headerName': 'ID', 'field': 'id', 'checkboxSelection': True, 'width': 80},
                    {'headerName': 'Name', 'field': 'name', 'filter': True, 'sortable': True, 'resizable': True},
                    {'headerName': 'URL', 'field': 'url', 'sortable': True, 'resizable': True},
                ]

                # Konverter produkter til liste af dicts for AG Grid
                # Note: Vi bruger html=True for at kunne rendere links hvis nødvendigt, 
                # men her holder vi det simpelt med ren tekst og row events.
                row_data = [
                    {'id': p.id, 'name': p.name, 'url': p.url} for p in products
                ]

                with ui.row().classes('w-full justify-end mb-2'):
                     ui.button('Delete Selected', on_click=delete_selected, icon='delete').props('outline color=negative')

                grid = ui.aggrid({
                    'columnDefs': column_defs,
                    'rowData': row_data,
                    'rowSelection': 'multiple',
                    'class': 'ag-theme-balham-dark' # Use dark theme to match layout
                }).classes('w-full h-96').on('cellClicked', navigate_to_product).on('cellKeyDown', navigate_on_enter, args=['data', 'event.key', 'colId'])

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
