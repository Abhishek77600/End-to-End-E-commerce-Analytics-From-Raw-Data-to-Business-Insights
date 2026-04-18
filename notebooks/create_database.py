import sqlite3
import pandas as pd
import os

# Create SQLite database
db_path = 'data/processed/ecommerce.db'
conn = sqlite3.connect(db_path)

# List of CSV files to load
csv_files = {
    'customers': 'data/raw/olist_customers_dataset.csv',
    'orders': 'data/raw/olist_orders_dataset.csv',
    'order_items': 'data/raw/olist_order_items_dataset.csv',
    'order_payments': 'data/raw/olist_order_payments_dataset.csv',
    'order_reviews': 'data/raw/olist_order_reviews_dataset.csv',
    'products': 'data/raw/olist_products_dataset.csv',
    'sellers': 'data/raw/olist_sellers_dataset.csv',
    'geolocation': 'data/raw/olist_geolocation_dataset.csv',
    'category_translation': 'data/raw/product_category_name_translation.csv'
}

# Load each CSV into SQLite table
for table_name, csv_path in csv_files.items():
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Loaded {table_name} with {len(df)} rows")
    else:
        print(f"File not found: {csv_path}")

# Create a merged view for easier analysis
merged_query = """
CREATE VIEW IF NOT EXISTS order_summary AS
SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    o.order_purchase_timestamp as order_date,
    o.order_delivered_customer_date as delivered_date,
    o.order_estimated_delivery_date as estimated_delivery_date,
    o.order_status,
    oi.product_id,
    p.product_category_name,
    ct.product_category_name_english as category,
    oi.price,
    oi.freight_value,
    op.payment_value as total,
    ore.review_score as rating
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation ct ON p.product_category_name = ct.product_category_name
LEFT JOIN (
    SELECT order_id, SUM(payment_value) as payment_value
    FROM order_payments
    GROUP BY order_id
) op ON o.order_id = op.order_id
LEFT JOIN order_reviews ore ON o.order_id = ore.order_id;
"""

conn.execute(merged_query)
conn.commit()

print("Created order_summary view")
print(f"Database created at {db_path}")

conn.close()