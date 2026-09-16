import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from etl.extract import extract
from etl.transform import transform

def test_extract():
    data = extract()
    assert len(data["customers"]) == 500
    assert len(data["products"]) == 20
    assert len(data["orders"]) == 5000

def test_transform():
    warehouse = transform(extract())
    assert set(["dim_customer","dim_product","dim_date","dim_location","fact_sales"]).issubset(warehouse)
    assert len(warehouse["dim_customer"]) == 500
    assert len(warehouse["dim_product"]) == 20
    assert len(warehouse["fact_sales"]) > 0
    assert warehouse["fact_sales"]["net_sales"].notna().all()
