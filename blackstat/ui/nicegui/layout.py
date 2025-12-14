from nicegui import ui
from contextlib import contextmanager
from .theme import apply_theme

@contextmanager
def layout():
    apply_theme()
    
    with ui.header().classes('items-center justify-between no-wrap p-0 bg-primary'):
        with ui.row().classes('items-center gap-2 p-2'):
            ui.icon('ShowChart', size='md')
            ui.label('BlackStatter').classes('text-lg font-bold')

        with ui.row().classes('items-center gap-4 p-2'):
            ui.link('Products', '/').classes('text-white no-underline hover:underline')
            # Add more links here later

    with ui.column().classes('w-full p-4 gap-4'):
        yield

    with ui.footer().classes('bg-grey-9'):
        ui.label('BlackStatter © 2025').classes('text-xs text-grey-4')
