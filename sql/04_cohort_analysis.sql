-- Cohort Analysis SQL Script
-- Analyze customer cohorts over time

-- Cohort size by month
WITH customer_first_order AS (
    SELECT
        c.customer_unique_id,
        MIN(o.order_purchase_timestamp) as first_order_date
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT
    strftime('%Y-%m', first_order_date) as cohort_month,
    COUNT(*) as cohort_size
FROM customer_first_order
GROUP BY strftime('%Y-%m', first_order_date)
ORDER BY cohort_month;

-- Cohort retention analysis (simplified)
WITH customer_first_order AS (
    SELECT
        c.customer_unique_id,
        MIN(o.order_purchase_timestamp) as first_order_date,
        strftime('%Y-%m', MIN(o.order_purchase_timestamp)) as cohort_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
cohort_orders AS (
    SELECT
        cfo.customer_unique_id,
        cfo.cohort_month,
        strftime('%Y-%m', o.order_purchase_timestamp) as order_month,
        (strftime('%Y', o.order_purchase_timestamp) - strftime('%Y', cfo.first_order_date)) * 12 +
        (strftime('%m', o.order_purchase_timestamp) - strftime('%m', cfo.first_order_date)) as cohort_index
    FROM customer_first_order cfo
    JOIN customers c ON cfo.customer_unique_id = c.customer_unique_id
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
)
SELECT
    cohort_month,
    cohort_index,
    COUNT(DISTINCT customer_unique_id) as retained_customers
FROM cohort_orders
GROUP BY cohort_month, cohort_index
ORDER BY cohort_month, cohort_index
LIMIT 20;

-- Average revenue per cohort
WITH customer_first_order AS (
    SELECT
        c.customer_unique_id,
        MIN(o.order_purchase_timestamp) as first_order_date
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT
    strftime('%Y-%m', cfo.first_order_date) as cohort_month,
    COUNT(DISTINCT cfo.customer_unique_id) as customers,
    COUNT(o.order_id) as orders,
    ROUND(SUM(oi.price), 2) as total_revenue,
    ROUND(AVG(oi.price), 2) as avg_order_value,
    ROUND(SUM(oi.price) / COUNT(DISTINCT cfo.customer_unique_id), 2) as revenue_per_customer
FROM customer_first_order cfo
JOIN customers c ON cfo.customer_unique_id = c.customer_unique_id
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY strftime('%Y-%m', cfo.first_order_date)
ORDER BY cohort_month;