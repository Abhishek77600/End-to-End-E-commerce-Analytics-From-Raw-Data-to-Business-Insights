# End-to-End E-commerce Analytics: From Raw Data to Business Insights

This repository contains a full e-commerce analytics project built on the Brazilian Olist dataset. It includes data ingestion, cleaning, exploratory data analysis, funnel and cohort analysis, customer segmentation, revenue evaluation, and dashboard visualization.

## Project overview

This project provides:
- KPI reporting for orders, revenue, profit, and delivery performance
- Funnel analysis from order placement to delivery and review
- Customer segmentation and retention analysis
- Product, category, and geographic revenue insights
- A Streamlit dashboard for interactive business exploration

## Dataset

The project uses the Olist Brazilian E-commerce dataset, which includes:
- orders, customers, sellers, products, reviews, payments, and geolocation data
- detailed order and delivery lifecycle information
- product categories and translated metadata

## Project structure

- `data/raw/`: Raw CSV files from Olist dataset
- `data/processed/`: Cleaned and merged data
- `notebooks/`: Jupyter notebooks for analysis
- `sql/`: SQL scripts for data exploration
- `dashboard/`: Tableau workbook, Streamlit app, and screenshots
- `insights/`: Business insights and recommendations
- `docs/`: Methodology documentation

## Key features

- Total revenue, order, and profitability analysis
- Conversion funnel tracking for delivered and reviewed orders
- Customer segmentation and cohort analytics
- Delivery performance and rating impact analysis
- Category and state-level revenue insights
- Interactive filters via Streamlit dashboard

## Getting started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the notebooks in order:
   - `notebooks/01_EDA.ipynb`
   - `notebooks/02_funnel_analysis.ipynb`
   - `notebooks/03_customer_segmentation.ipynb`

3. Run the dashboard:
   ```bash
   streamlit run dashboard/streamlit_app.py
   ```

## Dashboard contents

- `dashboard/dashboard.twbx`: Tableau workbook
- `dashboard/screenshots/`: Dashboard preview images
- `dashboard/streamlit_app.py`: Streamlit dashboard using processed data

## Technologies used

- Python, pandas, NumPy
- scikit-learn, matplotlib, seaborn
- Jupyter Notebooks
- Tableau
- Streamlit

## Results

The analysis delivers actionable business recommendations for improving conversion rates, customer retention, and revenue performance by identifying top segments, delivery issues, and high-value categories.
