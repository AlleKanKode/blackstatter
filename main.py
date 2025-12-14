
from blackstat.models.db import init_db
from blackstat.utils.config import apply_locale
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="BlackStatter Price Tracker")
    parser.add_argument("--gui", action="store_true", help="Launch the graphical user interface (NiceGUI)")
    args = parser.parse_args()

    apply_locale()
    init_db()

    if args.gui:
        from blackstat.ui.nicegui.app import run_gui
        run_gui()
    else:
        from blackstat.ui.tui.app import BlackStatterApp
        app = BlackStatterApp()
        app.run()

if __name__ == "__main__":
    main()
