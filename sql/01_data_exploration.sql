-- Data Exploration SQL Script
-- This script explores the Olist e-commerce data

-- Basic data overview
SELECT 'Customers' as table_name, COUNT(*) as row_count FROM customers
UNION ALL
SELECT 'Orders' as table_name, COUNT(*) as row_count FROM orders
UNION ALL
SELECT 'Order Items' as table_name, COUNT(*) as row_count FROM order_items
UNION ALL
SELECT 'Products' as table_name, COUNT(*) as row_count FROM products;

-- Sample orders
SELECT * FROM orders LIMIT 10;

-- Order status distribution
SELECT order_status, COUNT(*) as count, ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM orders
GROUP BY order_status
ORDER BY count DESC;

-- Top 10 customer cities by order count
SELECT c.customer_city, COUNT(*) as order_count
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_city
ORDER BY order_count DESC
LIMIT 10;

-- Revenue by product category
SELECT ct.product_category_name_english as category, COUNT(*) as orders, ROUND(SUM(oi.price), 2) as total_revenue, ROUND(AVG(oi.price), 2) as avg_order_value
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN category_translation ct ON p.product_category_name = ct.product_category_name
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY ct.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;

-- Monthly order trends
SELECT strftime('%Y-%m', o.order_purchase_timestamp) as month, COUNT(*) as orders, ROUND(SUM(oi.price), 2) as revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY strftime('%Y-%m', o.order_purchase_timestamp)
ORDER BY month;