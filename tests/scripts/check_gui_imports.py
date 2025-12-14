import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

print("Checking GUI imports...")
try:
    from blackstat.ui.nicegui import app
    from blackstat.ui.nicegui.pages import home, product
    print("Imports successful.")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
