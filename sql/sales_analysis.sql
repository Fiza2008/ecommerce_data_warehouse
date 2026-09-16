-- 1. Monthly revenue
SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(f.net_sales), 2) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.status = 'Completed'
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- 2. Top 10 products
SELECT
    p.product_name,
    p.category,
    SUM(f.quantity) AS units_sold,
    ROUND(SUM(f.net_sales), 2) AS revenue
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
WHERE f.status = 'Completed'
GROUP BY p.product_key, p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;

-- 3. Revenue by category
SELECT
    p.category,
    SUM(f.quantity) AS units_sold,
    ROUND(SUM(f.net_sales), 2) AS revenue
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
WHERE f.status = 'Completed'
GROUP BY p.category
ORDER BY revenue DESC;

-- 4. Revenue by city
SELECT
    l.city,
    l.state,
    ROUND(SUM(f.net_sales), 2) AS revenue
FROM fact_sales f
JOIN dim_location l ON f.location_key = l.location_key
WHERE f.status = 'Completed'
GROUP BY l.city, l.state
ORDER BY revenue DESC;

-- 5. Average order value
SELECT
    ROUND(SUM(net_sales) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM fact_sales
WHERE status = 'Completed';

-- 6. Monthly running revenue using a window function
WITH monthly AS (
    SELECT
        d.year,
        d.month,
        SUM(f.net_sales) AS revenue
    FROM fact_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE f.status = 'Completed'
    GROUP BY d.year, d.month
)
SELECT
    year,
    month,
    ROUND(revenue,2) AS monthly_revenue,
    ROUND(SUM(revenue) OVER (ORDER BY year, month),2) AS cumulative_revenue
FROM monthly
ORDER BY year, month;
