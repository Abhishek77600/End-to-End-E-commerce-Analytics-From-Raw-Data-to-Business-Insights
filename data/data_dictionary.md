# Data Dictionary

This project uses the Brazilian E-commerce Public Dataset by Olist, available on Kaggle.

## Raw Data Files

### olist_customers_dataset.csv
- `customer_id`: Unique identifier for each customer
- `customer_unique_id`: Unique identifier for each customer (anonymized)
- `customer_zip_code_prefix`: Zip code prefix
- `customer_city`: Customer city
- `customer_state`: Customer state

### olist_orders_dataset.csv
- `order_id`: Unique identifier for each order
- `customer_id`: Customer identifier
- `order_status`: Order status (delivered, shipped, etc.)
- `order_purchase_timestamp`: Purchase timestamp
- `order_approved_at`: Approval timestamp
- `order_delivered_carrier_date`: Carrier delivery date
- `order_delivered_customer_date`: Customer delivery date
- `order_estimated_delivery_date`: Estimated delivery date

### olist_order_items_dataset.csv
- `order_id`: Order identifier
- `order_item_id`: Sequential number identifying items in the same order
- `product_id`: Product identifier
- `seller_id`: Seller identifier
- `shipping_limit_date`: Shipping limit date
- `price`: Item price
- `freight_value`: Freight value

### olist_order_payments_dataset.csv
- `order_id`: Order identifier
- `payment_sequential`: Sequential payment method
- `payment_type`: Payment method (credit_card, boleto, etc.)
- `payment_installments`: Number of installments
- `payment_value`: Payment value

### olist_order_reviews_dataset.csv
- `review_id`: Unique review identifier
- `order_id`: Order identifier
- `review_score`: Review score (1-5)
- `review_comment_title`: Review title
- `review_comment_message`: Review message
- `review_creation_date`: Review creation date
- `review_answer_timestamp`: Review answer timestamp

### olist_products_dataset.csv
- `product_id`: Product identifier
- `product_category_name`: Product category name (Portuguese)
- `product_name_lenght`: Product name length
- `product_description_lenght`: Product description length
- `product_photos_qty`: Number of product photos
- `product_weight_g`: Product weight in grams
- `product_length_cm`: Product length in cm
- `product_height_cm`: Product height in cm
- `product_width_cm`: Product width in cm

### olist_sellers_dataset.csv
- `seller_id`: Seller identifier
- `seller_zip_code_prefix`: Seller zip code prefix
- `seller_city`: Seller city
- `seller_state`: Seller state

### olist_geolocation_dataset.csv
- `geolocation_zip_code_prefix`: Zip code prefix
- `geolocation_lat`: Latitude
- `geolocation_lng`: Longitude
- `geolocation_city`: City
- `geolocation_state`: State

### product_category_name_translation.csv
- `product_category_name`: Product category name (Portuguese)
- `product_category_name_english`: Product category name (English)

## Processed Data

### cleaned_data.csv
Merged dataset with key fields for analysis:
- `order_id`: Order identifier
- `customer_id`: Customer identifier
- `customer_unique_id`: Unique customer identifier
- `customer_city`: Customer city
- `customer_state`: Customer state
- `order_status`: Order status
- `order_purchase_timestamp`: Purchase timestamp
- `order_approved_at`: Approval timestamp
- `order_delivered_customer_date`: Delivery date
- `order_estimated_delivery_date`: Estimated delivery date
- `product_id`: Product identifier
- `seller_id`: Seller identifier
- `price`: Item price
- `freight_value`: Freight value
- `payment_type`: Payment method
- `payment_value`: Total payment value
- `review_score`: Review score
- `product_category_name_english`: Product category (English)
- `total_revenue`: Calculated total revenue per order
- `cohort`: Customer cohort based on first purchase