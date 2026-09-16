# 🛒 E-Commerce Data Warehouse & BI Analytics

> A complete data engineering project that transforms raw e-commerce transaction data into a **star-schema data warehouse** using Python ETL and SQL, with Power BI-ready analytical reporting.

## 📌 Project Overview

This project simulates an e-commerce company's analytics platform.

Raw customer, product, order, order-item, and payment data is extracted from CSV files, cleaned and transformed using **Python/Pandas**, loaded into a **dimensional data warehouse in SQLite**, and analyzed using SQL.

The final warehouse is designed for BI reporting and can be connected to **Power BI** for interactive dashboards.

```text
Raw CSV Data
     ↓
Extract
     ↓
Clean + Validate
     ↓
Transform
     ↓
Star Schema Warehouse
     ↓
SQL Analytics
     ↓
Power BI Dashboard
```

---

## 🎯 Objectives

- Build a complete ETL pipeline
- Practice data cleaning and validation
- Design a star-schema data warehouse
- Work with fact and dimension tables
- Perform analytical SQL queries
- Create reusable data-processing scripts
- Prepare data for Power BI reporting
- Demonstrate data quality and troubleshooting concepts

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │   Raw CSV Files     │
                    │ Customers           │
                    │ Products            │
                    │ Orders              │
                    │ Order Items         │
                    │ Payments            │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Python ETL Pipeline │
                    │ Extract             │
                    │ Transform           │
                    │ Validate            │
                    │ Load                │
                    └──────────┬──────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │ SQLite Data Warehouse    │
                 │                          │
                 │       fact_sales         │
                 │          / | \            │
                 │         /  |  \           │
                 │ dim_customer              │
                 │ dim_product               │
                 │ dim_date                  │
                 │ dim_location              │
                 └────────────┬─────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │    SQL Analytics    │
                    │ Revenue             │
                    │ Products            │
                    │ Customers           │
                    │ Locations           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Power BI       │
                    │ Interactive Reports │
                    └─────────────────────┘
```

---

# ⭐ Key Features

## 1. Data Extraction

The pipeline reads multiple raw CSV datasets:

- Customers
- Products
- Orders
- Order Items
- Payments

The extraction layer keeps data ingestion separate from transformation and loading.

---

## 2. Data Cleaning & Validation

The transformation layer performs:

- Duplicate removal
- Missing-value handling
- Data-type conversion
- Text standardization
- Positive quantity validation
- Price validation
- Date processing
- Referential joins

This makes the project demonstrate practical **data quality checks**, rather than simply loading raw files.

---

## 3. Dimensional Data Warehouse

The project uses a **Star Schema**.

### Fact Table

`fact_sales`

Contains measurable business events:

- Quantity
- Unit price
- Gross sales
- Discount
- Shipping
- Net sales
- Order status

### Dimension Tables

`dim_customer`

Stores customer attributes.

`dim_product`

Stores product and category attributes.

`dim_date`

Stores calendar attributes such as:

- Year
- Quarter
- Month
- Week
- Day
- Day name

`dim_location`

Stores city and state information.

---

# 🧠 Why Star Schema?

A star schema separates:

**Facts**
> What happened?

from:

**Dimensions**
> Who, what, where, and when?

For example:

```text
             Customer
                 |
                 |
Product ---- Sales ---- Date
                 |
                 |
              Location
```

This makes analytical queries easier to organize and is a common dimensional modeling pattern for BI systems.

---

# 🔄 ETL Workflow

## Extract

Python reads the raw CSV files using Pandas.

```python
customers = pd.read_csv("customers.csv")
products = pd.read_csv("products.csv")
orders = pd.read_csv("orders.csv")
```

## Transform

The data is cleaned and converted into warehouse-ready structures.

Examples:

- Remove duplicates
- Convert dates
- Validate numeric values
- Create surrogate keys
- Create date dimension
- Calculate gross sales
- Allocate order-level discounts and shipping costs

## Load

The transformed DataFrames are written into SQLite tables.

Indexes are also created on frequently joined fact-table keys.

---

# 📐 Fact Table Grain

An important design decision is the grain of `fact_sales`.

> **One row represents one product line within one order.**

For example:

```text
Order 1001
 ├── Product A × 2
 ├── Product B × 1
 └── Product C × 3
```

becomes three fact rows.

This makes product-level and order-level analysis possible.

---

# 📊 SQL Analytics

The project contains SQL queries for:

### Monthly Revenue

```sql
SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(f.net_sales), 2) AS revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
WHERE f.status = 'Completed'
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;
```

### Top Products

```sql
SELECT
    p.product_name,
    p.category,
    SUM(f.quantity) AS units_sold,
    ROUND(SUM(f.net_sales), 2) AS revenue
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
WHERE f.status = 'Completed'
GROUP BY p.product_key, p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;
```

### Customer Analysis

```sql
SELECT
    c.customer_name,
    COUNT(DISTINCT f.order_id) AS orders,
    ROUND(SUM(f.net_sales), 2) AS total_spend
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
WHERE f.status = 'Completed'
GROUP BY c.customer_key, c.customer_name
ORDER BY total_spend DESC
LIMIT 20;
```

### Window Function

The project also demonstrates cumulative revenue using a SQL window function.

```sql
SUM(revenue) OVER (
    ORDER BY year, month
)
```

This is useful interview material because it demonstrates more than basic `SELECT` and `GROUP BY`.

---

# 📈 Power BI Dashboard

The warehouse can be connected to Power BI to build:

### KPI Cards

- Total Revenue
- Total Orders
- Units Sold
- Average Order Value
- Completed Order Rate

### Charts

- Monthly Revenue Trend
- Revenue by Category
- Top 10 Products
- Revenue by City
- Customer Segments
- Order Status Distribution

After creating the dashboard, save a screenshot as:

```text
powerbi/dashboard_screenshot.png
```

---

# 📁 Project Structure

```text
ecommerce-data-warehouse/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   ├── orders.csv
│   │   ├── order_items.csv
│   │   └── payments.csv
│   │
│   └── processed/
│
├── database/
│   └── ecommerce_warehouse.db
│
├── etl/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
│
├── sql/
│   ├── schema.sql
│   ├── data_quality.sql
│   ├── sales_analysis.sql
│   └── customer_analysis.sql
│
├── powerbi/
│   └── POWER_BI_GUIDE.md
│
├── dashboard.py
│   └── Streamlit web dashboard
│
├── tests/
│   └── test_pipeline.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python | ETL pipeline |
| Pandas | Data cleaning & transformation |
| SQLite | Local analytical warehouse |
| SQL | Data analysis |
| Power BI | Business intelligence |
| Pytest | Pipeline testing |
| Git/GitHub | Version control |

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ecommerce-data-warehouse
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the ETL Pipeline

From the project root:

```bash
python -m etl.pipeline
```

Expected output:

```text
Starting E-Commerce ETL pipeline...
Extracted: ...
Transformed: ...
Warehouse loaded successfully: ...
```

The SQLite warehouse will be created at:

```text
database/ecommerce_warehouse.db
```

---

# 🧪 Run Tests

```bash
pytest
```

The tests verify:

- Raw data extraction
- Expected dataset sizes
- Warehouse table creation
- Fact-table generation
- Null-value handling

---

# 🔍 Data Quality Checks

The project includes SQL checks for:

- Total fact records
- Missing customer keys
- Invalid quantities
- Negative sales
- Order-status distribution

Run:

```text
sql/data_quality.sql
```

---

## ⭐ If you found this project useful

Consider giving the repository a ⭐ on GitHub!
