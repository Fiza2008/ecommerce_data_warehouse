# Power BI Dashboard Guide

Connect Power BI Desktop to `database/ecommerce_warehouse.db`.

## Recommended model

Use these relationships:

- dim_customer[customer_key] 1 -> * fact_sales[customer_key]
- dim_product[product_key] 1 -> * fact_sales[product_key]
- dim_date[date_key] 1 -> * fact_sales[date_key]
- dim_location[location_key] 1 -> * fact_sales[location_key]

## KPI cards

Create:
- Total Revenue
- Total Orders
- Units Sold
- Average Order Value
- Completed Order Rate

## Recommended visuals

1. Line chart: Monthly Revenue
2. Bar chart: Revenue by Category
3. Bar chart: Top 10 Products
4. Map/bar chart: Revenue by City
5. Donut chart: Payment/Order Status
6. Table: Top Customers

## Suggested dashboard title

**E-Commerce Sales & Customer Analytics Dashboard**

Take a screenshot of the finished dashboard and save it as:
`powerbi/dashboard_screenshot.png`
