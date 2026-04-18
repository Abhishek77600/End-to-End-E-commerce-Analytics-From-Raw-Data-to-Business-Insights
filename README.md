# End-to-End E-commerce Analytics: From Raw Data to Business Insights

This project demonstrates a complete e-commerce analytics pipeline using the Brazilian E-commerce Public Dataset by Olist. It covers data ingestion, cleaning, exploratory analysis, funnel analysis, customer segmentation, and business insights generation.

## Dataset
The project uses the Olist Brazilian E-commerce dataset, which includes:
- 100k+ orders from 2016-2018
- Customer and seller information
- Product details and categories
- Order reviews and payments

## Project Structure

- `data/raw/`: Raw CSV files from Olist dataset
- `data/processed/`: Cleaned and merged data
- `notebooks/`: Jupyter notebooks for analysis
- `sql/`: SQL scripts for data exploration
- `dashboard/`: Tableau dashboard files and screenshots
- `insights/`: Executive summary and recommendations
- `docs/`: Methodology documentation

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the analysis notebooks in order:**
   - `01_EDA.ipynb`: Data loading, cleaning, and exploratory analysis
   - `02_funnel_analysis.ipynb`: Funnel analysis, cohort analysis, and segmentation
   - `03_customer_segmentation.ipynb`: Detailed customer segmentation with RFM analysis

3. **Run the live dashboard:**
   - Install Streamlit: `pip install streamlit`
   - Run: `streamlit run dashboard/streamlit_app.py`

4. **View results:**
   - Processed data in `data/processed/`
   - Business insights in `insights/recommendations.md`

## Key Analyses

- **Customer Segmentation**: K-means clustering on RFM (Recency, Frequency, Monetary) features
- **Funnel Analysis**: Order journey from purchase to delivery
- **Cohort Analysis**: Customer retention by acquisition cohorts
- **Revenue Analysis**: Segment performance and trends

## Technologies Used

- Python (pandas, scikit-learn, matplotlib, seaborn)
- Jupyter Notebooks
- Tableau (for dashboard visualization)
- Streamlit (for live dashboard exploration)

## Dashboard
- `dashboard/dashboard.twbx`: Tableau workbook
- `dashboard/screenshots/`: dashboard preview images
- `dashboard/streamlit_app.py`: live Streamlit dashboard using processed data

## Results

The analysis identifies key customer segments, delivery performance metrics, and actionable business recommendations for improving conversion rates and customer retention.