import pytest
from datetime import datetime
from blackstat.models.models import Product, PriceTransaction
from blackstat.models.crud import create_product, get_all_products, create_price_transaction, get_prices_for_product, delete_product
from blackstat.models.db import init_db, get_connection

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Use an in-memory DB or a test file for testing. 
    # Since our code uses a hardcoded path in db.py, we might want to mock it or just use a separate test DB.
    # For simplicity, I'll patch the DB_PATH or just run against the dev DB but clean it up.
    # Better: refactor db.py to allow overriding path.
    # But for now, let's just run init_db to ensure tables exist.
    init_db()
    yield
    # Cleanup could go here

def test_create_product():
    p = Product(name="Test Product", url="http://example.com")
    created = create_product(p)
    assert created.id is not None
    assert created.name == "Test Product"

def test_get_products():
    products = get_all_products()
    assert len(products) > 0

def test_price_transaction():
    p = Product(name="Price Test", url="http://price.com")
    created_p = create_product(p)
    
    t = PriceTransaction(product_id=created_p.id, price=100.0, source_url="http://price.com", date=datetime.now())
    created_t = create_price_transaction(t)
    
    assert created_t.id is not None
    assert created_t.price == 100.0
    
    prices = get_prices_for_product(created_p.id)
    assert len(prices) == 1
    assert prices[0].price == 100.0
    
    # Cleanup
    delete_product(created_p.id)
