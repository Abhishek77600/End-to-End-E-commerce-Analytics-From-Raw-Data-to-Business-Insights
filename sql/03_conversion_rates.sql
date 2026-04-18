-- Conversion Rates SQL Script
-- Calculate conversion rates at each funnel step

-- Order status conversion rates
WITH status_counts AS (
    SELECT
        order_status,
        COUNT(*) as count
    FROM orders
    GROUP BY order_status
),
total_orders AS (
    SELECT COUNT(*) as total FROM orders
)
SELECT
    sc.order_status,
    sc.count,
    ROUND(sc.count * 100.0 / tot.total, 2) as percentage
FROM status_counts sc
CROSS JOIN total_orders tot
ORDER BY sc.count DESC;

-- Payment method analysis
SELECT
    payment_type,
    COUNT(*) as orders,
    ROUND(SUM(payment_value), 2) as total_value,
    ROUND(AVG(payment_value), 2) as avg_value,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM order_payments
GROUP BY payment_type
ORDER BY total_value DESC;

-- Review score distribution
SELECT
    review_score,
    COUNT(*) as reviews,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM order_reviews
GROUP BY review_score
ORDER BY review_score;

-- Conversion by customer state
SELECT
    c.customer_state,
    COUNT(DISTINCT c.customer_unique_id) as customers,
    COUNT(DISTINCT o.order_id) as orders,
    ROUND(COUNT(DISTINCT o.order_id) * 1.0 / COUNT(DISTINCT c.customer_unique_id), 2) as orders_per_customer
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY orders DESC
LIMIT 10;