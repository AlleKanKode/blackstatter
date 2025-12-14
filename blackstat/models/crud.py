from typing import List, Optional
from datetime import datetime
from .db import get_connection
from .product import Product
from .price_transaction import PriceTransaction

# Product CRUD

def create_product(product: Product) -> Product:
    conn = get_connection()
    try:
        # We let the DB handle ID generation if not provided
        query = """
            INSERT INTO products (name, url, created_at)
            VALUES (?, ?, ?)
            RETURNING id, name, url, created_at
        """
        result = conn.execute(query, (product.name, product.url, product.created_at)).fetchone()
        return Product(id=result[0], name=result[1], url=result[2], created_at=result[3])
    finally:
        conn.close()

def get_all_products() -> List[Product]:
    conn = get_connection()
    try:
        results = conn.execute("SELECT id, name, url, created_at FROM products ORDER BY name").fetchall()
        return [Product(id=r[0], name=r[1], url=r[2], created_at=r[3]) for r in results]
    finally:
        conn.close()

def get_product(product_id: int) -> Optional[Product]:
    conn = get_connection()
    try:
        result = conn.execute("SELECT id, name, url, created_at FROM products WHERE id = ?", (product_id,)).fetchone()
        if result:
            return Product(id=result[0], name=result[1], url=result[2], created_at=result[3])
        return None
    finally:
        conn.close()

def update_product(product: Product) -> bool:
    conn = get_connection()
    try:
        query = """
            UPDATE products
            SET name = ?, url = ?
            WHERE id = ?
        """
        conn.execute(query, (product.name, product.url, product.id))
        return True # DuckDB doesn't easily return rowcount in all versions, assuming success if no error
    finally:
        conn.close()

def delete_product(product_id: int) -> bool:
    conn = get_connection()
    try:
        conn.execute("DELETE FROM prices WHERE product_id = ?", (product_id,))
        conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        return True
    finally:
        conn.close()

# Price Transaction CRUD

def create_price_transaction(transaction: PriceTransaction) -> PriceTransaction:
    conn = get_connection()
    try:
        query = """
            INSERT INTO prices (product_id, price, date, source_url)
            VALUES (?, ?, ?, ?)
            RETURNING id, product_id, price, date, source_url
        """
        result = conn.execute(query, (transaction.product_id, transaction.price, transaction.date, transaction.source_url)).fetchone()
        return PriceTransaction(id=result[0], product_id=result[1], price=result[2], date=result[3], source_url=result[4])
    finally:
        conn.close()

def get_prices_for_product(product_id: int) -> List[PriceTransaction]:
    conn = get_connection()
    try:
        results = conn.execute("SELECT id, product_id, price, date, source_url FROM prices WHERE product_id = ? ORDER BY date DESC", (product_id,)).fetchall()
        return [PriceTransaction(id=r[0], product_id=r[1], price=r[2], date=r[3], source_url=r[4]) for r in results]
    finally:
        conn.close()

def update_price_transaction(transaction: PriceTransaction) -> bool:
    conn = get_connection()
    try:
        query = """
            UPDATE prices
            SET price = ?, date = ?, source_url = ?
            WHERE id = ?
        """
        conn.execute(query, (transaction.price, transaction.date, transaction.source_url, transaction.id))
        return True
    finally:
        conn.close()

def delete_price_transaction(transaction_id: int) -> bool:
    conn = get_connection()
    try:
        conn.execute("DELETE FROM prices WHERE id = ?", (transaction_id,))
        return True
    finally:
        conn.close()
