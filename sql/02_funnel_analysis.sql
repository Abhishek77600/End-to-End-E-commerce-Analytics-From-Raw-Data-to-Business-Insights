-- Funnel Analysis SQL Script
-- Analyze the customer journey funnel

-- Overall funnel: Ordered -> Delivered
SELECT
    'Total Orders' as stage,
    COUNT(DISTINCT order_id) as count
FROM orders
UNION ALL
SELECT
    'Delivered Orders' as stage,
    COUNT(DISTINCT order_id) as count
FROM orders
WHERE order_status = 'delivered';

-- Delivery performance analysis
SELECT
    CASE
        WHEN order_delivered_customer_date <= order_estimated_delivery_date THEN 'On Time'
        ELSE 'Late'
    END as delivery_status,
    COUNT(*) as orders,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM orders
WHERE order_status = 'delivered'
GROUP BY delivery_status;

-- Average delivery time by state
SELECT
    c.customer_state,
    COUNT(*) as orders,
    ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)), 1) as avg_delivery_days
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY orders DESC
LIMIT 10;

-- Funnel by product category
SELECT
    ct.product_category_name_english as category,
    COUNT(DISTINCT CASE WHEN o.order_status = 'delivered' THEN o.order_id END) as delivered_orders,
    COUNT(DISTINCT o.order_id) as total_orders,
    ROUND(COUNT(DISTINCT CASE WHEN o.order_status = 'delivered' THEN o.order_id END) * 100.0 / COUNT(DISTINCT o.order_id), 2) as delivery_rate
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN category_translation ct ON p.product_category_name = ct.product_category_name
GROUP BY ct.product_category_name_english
ORDER BY total_orders DESC
LIMIT 10;