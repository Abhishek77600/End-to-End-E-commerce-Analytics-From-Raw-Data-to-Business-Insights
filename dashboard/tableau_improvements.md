# Tableau Workbook Improvement Recommendations

This file documents recommended enhancements for `dashboard/dashboard.twbx` to make the workbook more interactive and business-ready.

## Recommended KPI tiles
- Total revenue
- Total orders
- Average order value
- Average customer rating
- Average delivery time
- On-time delivery / delivery delay rate

## Recommended filters
- Order date range
- Product category
- Order status
- Customer state
- Minimum rating

## Recommended charts
- Revenue trend by purchase month
- Orders by state (bar or map)
- Top product categories by revenue
- Order status distribution
- Delivery time distribution
- Review rating distribution
- Top cities by revenue

## Dashboard layout suggestions
- Use a top KPI row for executive summary metrics
- Place date and category filters in the left pane
- Use a combined tile for revenue + order volume trend
- Add a separate section for customer retention and repeat purchase insights if available

## Notes
- The live Streamlit dashboard in `dashboard/streamlit_app.py` already implements these same insights using the cleaned data.
- If you want, I can also help turn these recommendations into a second Tableau worksheet and dashboard layout plan.