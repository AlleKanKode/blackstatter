from nicegui import ui
import asyncio
from blackstat.ui.nicegui.layout import layout
from blackstat.models.crud import get_product, get_prices_for_product, create_price_transaction, delete_price_transaction
from blackstat.models.price_transaction import PriceTransaction
from blackstat.controllers.price_agent import find_product_price

@ui.page('/product/{product_id}')
def product_page(product_id: int):
    # Wrap content in layout
    with layout():
        product = get_product(product_id)
        if not product:
            ui.label("Product not found").classes("text-red text-xl")
            return

        async def check_price_ai():
            spinner.set_visibility(True)
            ui.notify("Agent searching for price...")
            try:
                # Run async agent
                result = await find_product_price(product.name)
                if result:
                    ui.notify(f"Found: {result.price} {result.currency}", color='positive')
                    create_price_transaction(PriceTransaction(
                        product_id=product.id,
                        price=result.price,
                        source_url=result.source_url
                    ))
                    refresh_view()
                else:
                    ui.notify("Could not find price", color='negative')
            except Exception as e:
                ui.notify(f"Error: {e}", color='negative')
            finally:
                spinner.set_visibility(False)

        def refresh_view():
            chart_container.clear()
            table_container.clear()
            
            prices = get_prices_for_product(product.id)
            
            # Chart
            with chart_container:
                if prices:
                    sorted_prices = sorted(prices, key=lambda p: p.date)
                    dates = [p.date.strftime("%Y-%m-%d %H:%M") for p in sorted_prices]
                    values = [p.price for p in sorted_prices]
                    
                    ui.echart({
                        'title': {'text': 'Price History', 'textStyle': {'color': '#fff'}},
                        'tooltip': {'trigger': 'axis'},
                        'xAxis': {'type': 'category', 'data': dates, 'axisLabel': {'color': '#aaa'}},
                        'yAxis': {'type': 'value', 'axisLabel': {'color': '#aaa'}},
                        'series': [{'data': values, 'type': 'line', 'smooth': True, 'color': '#5898d4'}]
                    }).classes('w-full h-64')
                else:
                    ui.label("No price history yet.").classes("text-grey italic")

            # Table
            with table_container:
                if prices:
                    # Using a simple column for list to easier formatting
                    for p in prices:
                        with ui.card().classes('w-full mb-2 p-2 bg-grey-9'):
                            with ui.row().classes('justify-between items-center w-full'):
                                ui.label(f"{p.price} DKK").classes('text-lg font-bold text-positive')
                                ui.label(p.date.strftime("%Y-%m-%d %H:%M")).classes('text-grey text-sm')
                                ui.button(icon='delete', color='negative', 
                                          on_click=lambda id=p.id: delete_price(id)).props('flat sm')
                            ui.link('Source', p.source_url, new_tab=True).classes('text-xs text-info truncate block max-w-md')

        def delete_price(t_id):
            delete_price_transaction(t_id)
            refresh_view()
            ui.notify("Price deleted")

        async def add_price_dialog():
            with ui.dialog() as dialog, ui.card():
                ui.label('Add Price').classes('text-xl font-bold')
                price_input = ui.number('Price').classes('w-full')
                url_input = ui.input('Source URL').classes('w-full')
                
                def save():
                    if not price_input.value:
                        ui.notify('Please enter a price', color='warning')
                        return
                    
                    try:
                        price_val = float(price_input.value)
                        create_price_transaction(PriceTransaction(
                            product_id=product.id,
                            price=price_val,
                            source_url=url_input.value or "Manual Entry"
                        ))
                        ui.notify('Price added', color='positive')
                        dialog.close()
                        refresh_view()
                    except ValueError:
                        ui.notify('Invalid price', color='negative')

                with ui.row().classes('justify-end w-full mt-4'):
                    ui.button('Cancel', on_click=dialog.close).props('flat')
                    ui.button('Save', on_click=save)
            
            dialog.open()

        # UI Structure
        with ui.row().classes('items-center gap-4 mb-4'):
            ui.link('Back', '/').classes('text-grey no-underline hover:text-white')
            ui.label(product.name).classes('text-3xl font-bold')
            spinner = ui.spinner(size='lg').classes('ml-auto')
            spinner.set_visibility(False)
            ui.button('Add Price', icon='add', on_click=add_price_dialog).props('unelevated color=secondary')
            ui.button('Check Price', icon='smart_toy', on_click=check_price_ai).props('color=accent')

        ui.link(product.url, product.url, new_tab=True).classes('text-secondary mb-6 block')

        chart_container = ui.column().classes('w-full mb-6 p-4 bg-dark rounded-lg')
        table_container = ui.column().classes('w-full')

        refresh_view()


