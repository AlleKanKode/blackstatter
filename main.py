from blackstat.tui import BlackStatterApp
from blackstat.models.db import init_db
from blackstat.utils.config import apply_locale

def main():
    apply_locale()
    init_db()
    app = BlackStatterApp()
    app.run()

if __name__ == "__main__":
    main()
