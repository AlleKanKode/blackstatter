from blackstat.models.crud import get_all_products, get_prices_for_product
from blackstat.models.db import init_db

def inspect_data():
    init_db()
    products = get_all_products()
    
    for product in products:
        prices = get_prices_for_product(product.id)
        if len(prices) >= 2:
            print(f"Product: {product.name} (ID: {product.id})")
            sorted_prices = sorted(prices, key=lambda p: p.date)
            for p in sorted_prices:
                print(f"  Date: {p.date}, Price: {p.price}, Source: {p.source_url}")
            
            values = [p.price for p in sorted_prices]
            if len(set(values)) == 1:
                print("  -> All prices are identical.")
            else:
                print(f"  -> Prices vary: {values}")
            print("-" * 40)

if __name__ == "__main__":
    inspect_data()
