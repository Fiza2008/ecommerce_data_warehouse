from etl.extract import extract
from etl.transform import transform
from etl.load import load

def main():
    print("Starting E-Commerce ETL pipeline...")
    raw = extract()
    print("Extracted:", {k: len(v) for k, v in raw.items()})

    warehouse = transform(raw)
    print("Transformed:", {k: len(v) for k, v in warehouse.items()})

    db = load(warehouse)
    print(f"Warehouse loaded successfully: {db}")

if __name__ == "__main__":
    main()
