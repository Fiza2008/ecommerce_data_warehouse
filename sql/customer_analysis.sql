-- Customer analytics

-- Top customers by spend
SELECT
    c.customer_name,
    c.city,
    c.state,
    COUNT(DISTINCT f.order_id) AS orders,
    ROUND(SUM(f.net_sales), 2) AS total_spend
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
WHERE f.status = 'Completed'
GROUP BY c.customer_key, c.customer_name, c.city, c.state
ORDER BY total_spend DESC
LIMIT 20;

-- Customer segmentation by total spend
WITH customer_spend AS (
    SELECT
        customer_key,
        SUM(net_sales) AS spend
    FROM fact_sales
    WHERE status = 'Completed'
    GROUP BY customer_key
)
SELECT
    CASE
        WHEN spend >= 20000 THEN 'High Value'
        WHEN spend >= 10000 THEN 'Medium Value'
        ELSE 'Standard'
    END AS customer_segment,
    COUNT(*) AS customers,
    ROUND(SUM(spend),2) AS revenue
FROM customer_spend
GROUP BY customer_segment
ORDER BY revenue DESC;
