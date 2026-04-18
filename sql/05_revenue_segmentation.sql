-- Revenue Segmentation SQL Script
-- Segment customers by revenue contribution

-- Customer revenue segments
WITH customer_revenue AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) as order_count,
        ROUND(SUM(oi.price), 2) as total_revenue,
        ROUND(AVG(oi.price), 2) as avg_order_value,
        MAX(o.order_purchase_timestamp) as last_order_date
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
revenue_percentiles AS (
    SELECT
        customer_unique_id,
        total_revenue,
        NTILE(4) OVER (ORDER BY total_revenue DESC) as revenue_quartile
    FROM customer_revenue
)
SELECT
    CASE
        WHEN rp.revenue_quartile = 1 THEN 'High Value'
        WHEN rp.revenue_quartile = 2 THEN 'Medium-High Value'
        WHEN rp.revenue_quartile = 3 THEN 'Medium-Low Value'
        ELSE 'Low Value'
    END as segment,
    COUNT(*) as customers,
    ROUND(AVG(cr.total_revenue), 2) as avg_revenue,
    ROUND(SUM(cr.total_revenue), 2) as total_segment_revenue,
    ROUND(AVG(cr.order_count), 2) as avg_orders
FROM revenue_percentiles rp
JOIN customer_revenue cr ON rp.customer_unique_id = cr.customer_unique_id
GROUP BY rp.revenue_quartile
ORDER BY rp.revenue_quartile;

-- Revenue by product category
SELECT
    ct.product_category_name_english as category,
    COUNT(DISTINCT o.order_id) as orders,
    COUNT(DISTINCT c.customer_unique_id) as customers,
    ROUND(SUM(oi.price), 2) as total_revenue,
    ROUND(AVG(oi.price), 2) as avg_order_value,
    ROUND(SUM(oi.price) / COUNT(DISTINCT c.customer_unique_id), 2) as revenue_per_customer
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN category_translation ct ON p.product_category_name = ct.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY ct.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 15;

-- Geographic revenue analysis
SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) as orders,
    COUNT(DISTINCT c.customer_unique_id) as customers,
    ROUND(SUM(oi.price), 2) as total_revenue,
    ROUND(AVG(oi.price), 2) as avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC
LIMIT 10;

-- Monthly revenue trends
SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) as month,
    COUNT(DISTINCT o.order_id) as orders,
    COUNT(DISTINCT c.customer_unique_id) as customers,
    ROUND(SUM(oi.price), 2) as revenue,
    ROUND(AVG(oi.price), 2) as avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY strftime('%Y-%m', o.order_purchase_timestamp)
ORDER BY month;