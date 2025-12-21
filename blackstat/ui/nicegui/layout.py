from nicegui import ui
from contextlib import contextmanager
from .theme import apply_theme

@contextmanager
def layout():
    # Denne funktion fungerer som en global skabelon (template) for applikationen.
    # Ved at bruge @contextmanager kan vi bruge 'with layout():' syntaksen på siderne.
    # Alt kode inde i 'with layout():' blokken på en side bliver "injectet" der hvor 'yield' står herunder.
    # Sætter globale styles og farver for applikationen.
    apply_theme()
    
    # --- HEADER ---
    # Definerer den øverste bjælke som går igen på alle sider.
    with ui.header().classes('items-center justify-between no-wrap p-0 bg-primary'):
        with ui.row().classes('items-center gap-2 p-2'):
            ui.icon('ShowChart', size='md')
            ui.label('BlackStatter').classes('text-lg font-bold')

        with ui.row().classes('items-center gap-4 p-2'):
            ui.link('Products', '/').classes('text-white no-underline hover:underline')
            # Add more links here later

    # --- MAIN CONTENT ---
    # Her definerer vi containeren til hovedindholdet.
    with ui.column().classes('w-full p-4 gap-4'):
        # 'yield' er nøglen: Her indsættes det indhold som er defineret inde i 'with layout():' 
        # blokken ude på de enkelte sider (f.eks. i home.py).
        yield

    # --- FOOTER ---
    # Definerer bunden af siden.
    with ui.footer().classes('bg-grey-9'):
        ui.label('BlackStatter © 2025').classes('text-xs text-grey-4')
