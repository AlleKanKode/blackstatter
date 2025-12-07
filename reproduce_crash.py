from blackstat.models.crud import get_all_products, get_prices_for_product
from blackstat.models.db import init_db
import traceback
import plotext as plt

def check_data_integrity():
    init_db()
    products = get_all_products()
    print(f"Found {len(products)} products.")

    for product in products:
        print(f"Checking product: {product.name} (ID: {product.id})")
        try:
            prices = get_prices_for_product(product.id)
            print(f"  Found {len(prices)} prices.")
            
            if prices:
                sorted_prices = sorted(prices, key=lambda p: p.date)
                dates = [p.date.strftime("%Y-%m-%d %H:%M") for p in sorted_prices]
                values = [p.price for p in sorted_prices]
                
                print(f"  Plotting {len(dates)} points...")
                plt.clear_data()
                # FIX: Set the date format to match our data (no % for plotext)
                plt.date_form("Y-m-d H:M")
                
                plt.plot(dates, values)
                plt.build()
                print("  Plot successful.")
                    
        except Exception as e:
            print(f"CRASH for product {product.id}: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    check_data_integrity()
