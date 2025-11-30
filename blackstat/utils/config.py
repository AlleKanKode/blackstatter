import os
import locale
from dotenv import load_dotenv

load_dotenv()

def get_locale_setting():
    return os.getenv("LOCALE", "")

def apply_locale():
    loc = get_locale_setting()
    try:
        if loc:
            locale.setlocale(locale.LC_ALL, loc)
        else:
            locale.setlocale(locale.LC_ALL, "") # Use system default
    except locale.Error as e:
        print(f"Error setting locale: {e}")
