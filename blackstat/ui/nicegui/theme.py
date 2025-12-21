from nicegui import ui

def apply_theme():
    # Use the same color palette idea as the TUI if applicable, or a modern dark theme
    ui.colors(
        primary='#5898d4',
        #primary='#ff0000',
        secondary='#26a69a',
        accent='#ff4081',
        dark='#1d1d1d',
        positive='#21ba45',
        negative='#c10015',
        info='#31ccec',
        warning='#f2c037'
    )
    # Force dark mode for now as per requirement for "premium/sleek"
    ui.dark_mode().enable()
