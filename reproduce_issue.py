from blackstat.models.models import Product
from blackstat.models.crud import create_product, update_product, get_product, delete_product
from blackstat.models.db import init_db

def test_update_flow():
    init_db()
    
    # 1. Create
    p = Product(name="Original Name", url="http://orig.com")
    created = create_product(p)
    print(f"Created: {created}")
    
    # 2. Get
    fetched = get_product(created.id)
    print(f"Fetched: {fetched}")
    
    # 3. Modify (Simulate Form)
    fetched.name = "Updated Name"
    fetched.url = "http://updated.com"
    
    # 4. Update
    try:
        update_product(fetched)
        print("Update successful")
    except Exception as e:
        print(f"Update failed: {e}")
        raise

    # 5. Verify
    final = get_product(created.id)
    print(f"Final: {final}")
    assert final.name == "Updated Name"
    
    # Cleanup
    delete_product(created.id)

if __name__ == "__main__":
    test_update_flow()
