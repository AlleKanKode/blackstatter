from nicegui import ui
from blackstat.models.db import init_db
from .theme import apply_theme
# Import pages to register them
from .pages import home

def init_nicegui():
    init_db()
    # We don't need to do much here if pages use @ui.page decorator
    # just ensure they are imported.

def run_gui():
    init_nicegui()
    ui.run(title='BlackStatter', dark=True, reload=True) # Reload=True for development
