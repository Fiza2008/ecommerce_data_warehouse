-- Data quality checks
SELECT COUNT(*) AS total_sales_rows FROM fact_sales;

SELECT COUNT(*) AS null_customer_keys
FROM fact_sales WHERE customer_key IS NULL;

SELECT COUNT(*) AS invalid_quantities
FROM fact_sales WHERE quantity <= 0;

SELECT COUNT(*) AS negative_sales
FROM fact_sales WHERE net_sales < 0;

SELECT status, COUNT(*) AS orders
FROM fact_sales
GROUP BY status
ORDER BY orders DESC;
