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

# 💡 Business Questions Answered

The warehouse can answer questions such as:

1. What is monthly revenue?
2. Which products generate the most revenue?
3. Which categories sell the most units?
4. Which cities generate the most revenue?
5. What is the average order value?
6. Who are the highest-value customers?
7. What is cumulative revenue over time?
8. How are customers distributed by spending segment?
9. How many orders are completed, returned, or cancelled?
10. Which products have the highest sales volume?

---

# 🧩 Data Engineering Concepts Demonstrated

This project demonstrates:

- ETL
- Data cleaning
- Data validation
- Data transformation
- Data warehousing
- Star schema
- Fact tables
- Dimension tables
- Surrogate keys
- Data granularity
- SQL joins
- Aggregations
- CTEs
- Window functions
- Indexing
- BI reporting
- Pipeline testing

---

# ☁️ Future Improvements

The project can be extended with:

- PostgreSQL
- Amazon S3
- AWS Glue
- Amazon Redshift
- Apache Airflow
- Apache Spark
- Kafka
- Docker
- GitHub Actions
- Automated data-quality monitoring
- Incremental ETL
- Slowly Changing Dimensions
- Cloud-based Power BI deployment

---

# 🎤 Interview Explanation

### Short version

> I built an e-commerce data warehouse using Python, Pandas, SQL and SQLite. I created an ETL pipeline that extracts raw customer, product and transaction data, cleans and validates it, creates dimension tables and a sales fact table, and loads everything into a star-schema warehouse. I then used SQL for analytical queries such as revenue trends, top products, customer segmentation and cumulative revenue, with Power BI used for reporting.

### If asked "Why did you use a star schema?"

> I used a star schema because it separates measurable business events in the fact table from descriptive information in dimension tables. This simplifies analytical joins and makes the warehouse suitable for BI reporting.

### If asked "What is the grain of your fact table?"

> One row represents one product line within an order.

### If asked "What did your ETL pipeline do?"

> Extract reads the raw CSV files, Transform performs cleaning, validation, date processing, surrogate-key creation and metric calculations, and Load writes the resulting dimensions and fact table into the SQLite warehouse.

---

# 📄 Resume Description

**E-Commerce Data Warehouse & BI Analytics | Python, SQL, Pandas, SQLite, Power BI**

- Developed a Python-based ETL pipeline to extract, clean, validate, transform, and load **5,000+ e-commerce orders** into a star-schema data warehouse with fact and dimension tables.
- Designed SQL analytics using **joins, CTEs, aggregations, and window functions** to analyze revenue, products, customers, locations, and order performance.
- Prepared warehouse data for Power BI reporting with KPI metrics, revenue trends, product analysis, customer segmentation, and data-quality checks.

---

# ⭐ Key Interview Topics From This Project

Be prepared to explain:

```text
1. What is ETL?
2. ETL vs ELT
3. What is a data warehouse?
4. OLTP vs OLAP
5. What is a star schema?
6. Fact table vs dimension table
7. What is data granularity?
8. What are surrogate keys?
9. Primary key vs foreign key
10. INNER JOIN vs LEFT JOIN
11. GROUP BY vs HAVING
12. CTE
13. Window functions
14. Indexes
15. Data validation
16. Handling missing values
17. Incremental ETL
18. Slowly Changing Dimensions
19. Data lake vs data warehouse
20. How would you move this pipeline to AWS?
```

---

## 👩‍💻 Author

**Fiza Naz Shaik**

B.Tech Computer Science & Engineering — AI/ML  
VIT-AP

---

## ⭐ If you found this project useful

Consider giving the repository a ⭐ on GitHub!
