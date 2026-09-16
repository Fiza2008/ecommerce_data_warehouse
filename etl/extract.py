from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

def extract():
    return {
        "customers": pd.read_csv(RAW_DIR / "customers.csv"),
        "products": pd.read_csv(RAW_DIR / "products.csv"),
        "orders": pd.read_csv(RAW_DIR / "orders.csv", parse_dates=["order_date"]),
        "order_items": pd.read_csv(RAW_DIR / "order_items.csv"),
        "payments": pd.read_csv(RAW_DIR / "payments.csv"),
    }
