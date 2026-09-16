from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path(__file__).resolve().parents[1] / "database" / "ecommerce_warehouse.db"

def load(warehouse):
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    for table, df in warehouse.items():
        df.to_sql(table, conn, if_exists="replace", index=False)

    # Useful indexes for analytical joins
    indexes = [
        "CREATE INDEX idx_fact_date ON fact_sales(date_key)",
        "CREATE INDEX idx_fact_customer ON fact_sales(customer_key)",
        "CREATE INDEX idx_fact_product ON fact_sales(product_key)",
        "CREATE INDEX idx_fact_location ON fact_sales(location_key)",
    ]
    for statement in indexes:
        conn.execute(statement)
    conn.commit()
    conn.close()
    return DB_PATH
