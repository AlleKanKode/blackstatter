import duckdb
import os
from pathlib import Path

DB_PATH = Path("data/blackstatter.duckdb")

def get_connection():
    """Returns a DuckDB connection."""
    # Ensure data directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(DB_PATH))

def init_db():
    """Initializes the database with necessary tables."""
    conn = get_connection()
    try:
        conn.execute("""
            CREATE SEQUENCE IF NOT EXISTS product_id_seq;
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY DEFAULT nextval('product_id_seq'),
                name VARCHAR NOT NULL,
                url VARCHAR NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE SEQUENCE IF NOT EXISTS price_id_seq;
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY DEFAULT nextval('price_id_seq'),
                product_id INTEGER NOT NULL,
                price DOUBLE NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source_url VARCHAR NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(id)
            );
        """)
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
