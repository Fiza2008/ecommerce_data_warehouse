import pandas as pd

def transform(data):
    customers = data["customers"].copy()
    products = data["products"].copy()
    orders = data["orders"].copy()
    items = data["order_items"].copy()

    # Remove duplicate records
    customers = customers.drop_duplicates(subset=["customer_id"])
    products = products.drop_duplicates(subset=["product_id"])
    orders = orders.drop_duplicates(subset=["order_id"])
    items = items.drop_duplicates(subset=["order_id", "product_id"])

    # Standardize text
    for df, cols in [
        (customers, ["customer_name","email","city","state"]),
        (products, ["product_name","category"]),
        (orders, ["status"])
    ]:
        for col in cols:
            df[col] = df[col].astype(str).str.strip()

    # Validate numeric fields
    products["unit_price"] = pd.to_numeric(products["unit_price"], errors="coerce")
    items["quantity"] = pd.to_numeric(items["quantity"], errors="coerce")
    items["unit_price"] = pd.to_numeric(items["unit_price"], errors="coerce")
    orders["total_amount"] = pd.to_numeric(orders["total_amount"], errors="coerce")

    products = products.dropna(subset=["product_id","unit_price"])
    items = items.dropna(subset=["order_id","product_id","quantity","unit_price"])
    orders = orders.dropna(subset=["order_id","customer_id","order_date","total_amount"])

    # Keep valid positive quantities/prices
    items = items[(items["quantity"] > 0) & (items["unit_price"] >= 0)]

    # Create date dimension
    dates = pd.DataFrame({
        "date": pd.date_range(
            orders["order_date"].min().normalize(),
            orders["order_date"].max().normalize(),
            freq="D"
        )
    })
    dates["date_key"] = dates["date"].dt.strftime("%Y%m%d").astype(int)
    dates["year"] = dates["date"].dt.year
    dates["quarter"] = dates["date"].dt.quarter
    dates["month"] = dates["date"].dt.month
    dates["month_name"] = dates["date"].dt.month_name()
    dates["week"] = dates["date"].dt.isocalendar().week.astype(int)
    dates["day"] = dates["date"].dt.day
    dates["day_name"] = dates["date"].dt.day_name()

    # Build location dimension from customer location
    locations = customers[["city","state"]].drop_duplicates().reset_index(drop=True)
    locations.insert(0, "location_key", range(1, len(locations)+1))

    # Surrogate keys for dimensions
    customers["customer_key"] = range(1, len(customers)+1)
    products["product_key"] = range(1, len(products)+1)

    # Fact table: order-item grain
    fact = (
        items.merge(orders[["order_id","customer_id","order_date","status","discount","shipping_fee"]],
                    on="order_id", how="inner")
             .merge(customers[["customer_id","customer_key","city","state"]],
                    on="customer_id", how="inner")
             .merge(products[["product_id","product_key"]],
                    on="product_id", how="inner")
             .merge(locations, on=["city","state"], how="left")
    )
    fact["date_key"] = fact["order_date"].dt.strftime("%Y%m%d").astype(int)
    fact["gross_amount"] = fact["quantity"] * fact["unit_price"]
    # Allocate order-level discount/shipping across items proportionally
    item_gross = fact.groupby("order_id")["gross_amount"].transform("sum")
    fact["allocated_discount"] = (fact["discount"] * fact["gross_amount"] / item_gross.replace(0,1)).round(2)
    fact["allocated_shipping"] = (fact["shipping_fee"] * fact["gross_amount"] / item_gross.replace(0,1)).round(2)
    fact["net_sales"] = (fact["gross_amount"] - fact["allocated_discount"] + fact["allocated_shipping"]).round(2)

    fact["sales_key"] = range(1, len(fact)+1)

    return {
        "dim_customer": customers[["customer_key","customer_id","customer_name","email","city","state"]],
        "dim_product": products[["product_key","product_id","product_name","category","unit_price"]],
        "dim_date": dates[["date_key","date","year","quarter","month","month_name","week","day","day_name"]],
        "dim_location": locations[["location_key","city","state"]],
        "fact_sales": fact[[
            "sales_key","order_id","date_key","customer_key","product_key","location_key",
            "quantity","unit_price","gross_amount","allocated_discount",
            "allocated_shipping","net_sales","status"
        ]],
    }
