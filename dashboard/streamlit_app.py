import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"

ORDER_STATUS_MAPPING = {
    "delivered": "Delivered",
    "shipped": "Shipped",
    "canceled": "Cancelled",
    "unavailable": "Returned",
    "invoiced": "Other",
    "processing": "Other",
    "created": "Other",
    "approved": "Other",
}


def translate_status(status: str) -> str:
    return ORDER_STATUS_MAPPING.get(status, "Other")


@st.cache_data
def load_data() -> pd.DataFrame:
    orders = pd.read_csv(
        RAW_DIR / "olist_orders_dataset.csv",
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
        low_memory=False,
    )
    items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv", parse_dates=["shipping_limit_date"], low_memory=False)
    customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv", low_memory=False)
    reviews = pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv", parse_dates=["review_creation_date", "review_answer_timestamp"], low_memory=False)
    products = pd.read_csv(RAW_DIR / "olist_products_dataset.csv", low_memory=False)
    category_map = pd.read_csv(RAW_DIR / "product_category_name_translation.csv", low_memory=False)

    reviews = reviews.sort_values("review_creation_date").groupby("order_id", as_index=False).last()
    items = items.merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
    items = items.merge(category_map, on="product_category_name", how="left")
    items["category"] = items["product_category_name_english"].fillna(items["product_category_name"]).fillna("Unknown")
    items["total_revenue"] = items["price"].fillna(0) + items["freight_value"].fillna(0)

    df = items.merge(orders, on="order_id", how="left")
    df = df.merge(customers, on="customer_id", how="left")
    df = df.merge(reviews[["order_id", "review_score"]], on="order_id", how="left")

    df["rating"] = df["review_score"].astype(float)
    df["order_date"] = df["order_purchase_timestamp"]
    df["delivered_date"] = df["order_delivered_customer_date"]
    df["estimated_delivery_date"] = df["order_estimated_delivery_date"]
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["delivery_days"] = (df["delivered_date"] - df["order_date"]).dt.days
    df["late_delivery"] = np.where(
        (df["delivered_date"].notna())
        & (df["estimated_delivery_date"].notna())
        & (df["delivered_date"] > df["estimated_delivery_date"]),
        1,
        0,
    )
    df["order_status_clean"] = df["order_status"].map(translate_status).fillna("Other")
    df["cost_estimated"] = df["price"].fillna(0) * 0.68 + df["freight_value"].fillna(0) * 0.15
    df["profit"] = df["total_revenue"] - df["cost_estimated"]
    df["profit_margin"] = np.where(df["total_revenue"] > 0, df["profit"] / df["total_revenue"], 0)

    order_counts_by_customer = df.groupby("customer_unique_id")["order_id"].nunique()
    df["customer_segment"] = df["customer_unique_id"].map(
        lambda customer_id: "Repeat" if order_counts_by_customer.loc[customer_id] > 1 else "New"
    )

    return df


def render_kpis(df: pd.DataFrame) -> None:
    total_orders = df["order_id"].nunique()
    total_revenue = df["total_revenue"].sum()
    total_profit = df["profit"].sum()
    avg_profit_margin = df["profit_margin"].mean() * 100
    avg_delivery_days = df["delivery_days"].mean()
    late_rate = df["late_delivery"].mean() * 100

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🧾 Total orders", f"{total_orders:,}")
    col2.metric("💰 Total revenue", f"R$ {total_revenue:,.0f}")
    col3.metric("📈 Total profit", f"R$ {total_profit:,.0f}")
    col4.metric("📊 Avg. margin", f"{avg_profit_margin:.1f}%")
    col5.metric("🚚 Late deliveries", f"{late_rate:.1f}%")

    with st.expander("Top business highlights", expanded=True):
        top_state = df.groupby("customer_state")["total_revenue"].sum().idxmax()
        top_city = df.groupby("customer_city")["total_revenue"].sum().idxmax()
        best_category = df.groupby("category")["profit"].sum().idxmax()
        worst_category = df.groupby("category")["profit"].sum().idxmin()
        st.write(
            f"• **Top-performing state:** {top_state}  \
             • **Top-performing city:** {top_city}  \
             • **Best category:** {best_category}  \
             • **Worst category:** {worst_category}"
        )


def render_insights(df: pd.DataFrame) -> None:
    st.markdown("### Business insights")
    revenue_by_month = (
        df.groupby("order_month", as_index=False)["total_revenue"].sum().sort_values("order_month")
    )
    growth = 0.0
    if len(revenue_by_month) > 1 and revenue_by_month.iloc[0, 1] != 0:
        growth = ((revenue_by_month.iloc[-1, 1] - revenue_by_month.iloc[0, 1]) / revenue_by_month.iloc[0, 1]) * 100

    if growth > 0:
        growth_sentence = f"Revenue grew by {growth:.1f}%, indicating an upward trend in recent months."
    elif growth < 0:
        growth_sentence = f"Revenue declined by {abs(growth):.1f}%, indicating a downward trend in recent months."
    else:
        growth_sentence = "Revenue has remained stable over the selected timeframe."

    delivered_pct = (df["order_status_clean"] == "Delivered").mean() * 100
    most_profitable_state = df.groupby("customer_state")["profit"].sum().idxmax()
    profit_by_category = df.groupby("category")["profit"].sum().sort_values(ascending=False)
    top3_profit_pct = profit_by_category.head(3).sum() / profit_by_category.sum() * 100 if not profit_by_category.empty else 0
    delivery_rating_corr = (
        df.dropna(subset=["delivery_days", "rating"])[["delivery_days", "rating"]].corr().loc["delivery_days", "rating"]
    )
    delivery_rating_sentence = (
        "States with higher delivery times tend to have lower ratings." if delivery_rating_corr < 0 else
        "There is a positive relationship between delivery time and ratings in the filtered data."
    )

    st.info(
        f"{growth_sentence}  \
        Delivered orders represent **{delivered_pct:.1f}%** of filtered orders, which reflects a dataset bias toward fulfilled deliveries.  \
        Most profitable state: **{most_profitable_state}**.  \
        Top 3 categories contribute **{top3_profit_pct:.1f}%** of total profit.  \
        {delivery_rating_sentence}",
        icon="💡",
    )


def render_charts(df: pd.DataFrame) -> None:
    st.subheader("Revenue and Conversion Analytics")

    orders_by_month = (
        df.groupby("order_month", as_index=False)["order_id"].nunique().rename(columns={"order_id": "orders"}).sort_values("order_month")
    )
    revenue_by_month = (
        df.groupby("order_month", as_index=False)["total_revenue"].sum().sort_values("order_month")
    )

    monthly_fig = px.line(
        orders_by_month,
        x="order_month",
        y="orders",
        title="Monthly Order Trends",
        labels={"order_month": "Month", "orders": "Orders"},
        markers=True,
    )
    monthly_fig.add_bar(
        x=revenue_by_month["order_month"],
        y=revenue_by_month["total_revenue"],
        name="Revenue",
        marker_color="#636EFA",
        yaxis="y2",
    )
    monthly_fig.update_layout(
        xaxis_tickangle=-45,
        yaxis2=dict(title="Revenue (R$)", overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.01),
        title="Monthly Orders and Revenue",
        font=dict(size=12),
    )

    delivered_orders = df.loc[df["order_status_clean"] == "Delivered", "order_id"].nunique()
    reviewed_orders = df.loc[
        (df["order_status_clean"] == "Delivered") & (df["rating"].notna()),
        "order_id",
    ].nunique()
    funnel_data = pd.DataFrame(
        {
            "stage": ["Orders", "Delivered", "Reviewed"],
            "count": [
                df["order_id"].nunique(),
                delivered_orders,
                min(reviewed_orders, delivered_orders),
            ],
        }
    )
    funnel_fig = px.funnel(
        funnel_data,
        x="count",
        y="stage",
        title="Order → Delivered → Reviewed Funnel",
        labels={"count": "Orders", "stage": "Stage"},
    )

    col1, col2 = st.columns(2)
    col1.plotly_chart(monthly_fig, use_container_width=True)
    col2.plotly_chart(funnel_fig, use_container_width=True)

    st.markdown("### Profit and Delivery Insights")
    profit_by_category = (
        df.groupby("category", as_index=False)["profit"].sum().sort_values("profit", ascending=False).head(12)
    )
    profit_cat_fig = px.bar(
        profit_by_category,
        x="profit",
        y="category",
        orientation="h",
        title="Profit by Category",
        labels={"profit": "Profit (R$)", "category": "Category"},
    )

    profit_by_state = (
        df.groupby("customer_state", as_index=False)["profit"].sum().sort_values("profit", ascending=False).head(12)
    )
    profit_state_fig = px.bar(
        profit_by_state,
        x="customer_state",
        y="profit",
        title="Profit by State",
        labels={"customer_state": "State", "profit": "Profit (R$)"},
    )

    avg_delivery_state = (
        df.groupby("customer_state", as_index=False)["delivery_days"].mean().sort_values("delivery_days")
    )
    delivery_state_fig = px.bar(
        avg_delivery_state.head(12),
        x="delivery_days",
        y="customer_state",
        orientation="h",
        title="Average Delivery Time by State",
        labels={"delivery_days": "Avg delivery days", "customer_state": "State"},
    )

    col1, col2 = st.columns(2)
    col1.plotly_chart(profit_cat_fig, use_container_width=True)
    col2.plotly_chart(profit_state_fig, use_container_width=True)
    st.plotly_chart(delivery_state_fig, use_container_width=True)

    st.subheader("Delivery Time vs Review Rating")
    scatter_fig = px.scatter(
        df,
        x="delivery_days",
        y="rating",
        color="order_status_clean",
        size="total_revenue",
        hover_data=["order_id", "customer_state", "category"],
        title="Delivery Time vs Rating",
        labels={"delivery_days": "Delivery Days", "rating": "Review Rating"},
    )
    scatter_fig.update_layout(font=dict(size=12))
    st.plotly_chart(scatter_fig, use_container_width=True)

    st.subheader("Status Distribution and Customer Segmentation")
    status_fig = px.pie(
        df["order_status_clean"].value_counts().reset_index(name="count").rename(columns={"index": "order_status_clean"}),
        names="order_status_clean",
        values="count",
        title="Order Status Distribution",
    )
    segment_fig = px.bar(
        df["customer_segment"].value_counts().reset_index(name="count").rename(columns={"index": "customer_segment"}),
        x="customer_segment",
        y="count",
        title="Customer Segmentation: New vs Repeat",
        labels={"customer_segment": "Segment", "count": "Orders"},
    )

    col1, col2 = st.columns(2)
    col1.plotly_chart(status_fig, use_container_width=True)
    col2.plotly_chart(segment_fig, use_container_width=True)

    st.subheader("Top Products and Revenue Heatmap")
    top_products = (
        df.groupby(["product_id", "category"], as_index=False)["total_revenue"].sum()
        .sort_values("total_revenue", ascending=False)
        .head(12)
        .reset_index(drop=True)
    )
    top_products["product_label"] = [f"Product {i+1} ({cat})" for i, cat in enumerate(top_products["category"])]
    top_products_fig = px.bar(
        top_products,
        x="total_revenue",
        y="product_label",
        orientation="h",
        title="Top Products by Revenue",
        labels={"product_label": "Product", "total_revenue": "Revenue (R$)"},
        hover_data={"product_id": True, "category": True},
    )

    heatmap_data = (
        df.groupby(["customer_state", "category"], as_index=False)["total_revenue"].sum()
    )
    heatmap_fig = px.density_heatmap(
        heatmap_data,
        x="customer_state",
        y="category",
        z="total_revenue",
        title="State vs Category Revenue Heatmap",
        labels={"customer_state": "State", "category": "Category", "total_revenue": "Revenue (R$)"},
        color_continuous_scale="Viridis",
    )

    st.plotly_chart(top_products_fig, use_container_width=True)
    st.plotly_chart(heatmap_fig, use_container_width=True)


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")
    st.sidebar.caption("Use these controls to refine the dashboard views.")

    min_date, max_date = st.sidebar.date_input(
        "Order date range",
        [df["order_date"].min().date(), df["order_date"].max().date()],
        key="date_range",
        help="Filter orders by purchase date range.",
    )

    order_status = st.sidebar.multiselect(
        "Order status",
        options=sorted(df["order_status_clean"].unique()),
        default=sorted(df["order_status_clean"].unique()),
        help="Include only selected order statuses.",
    )

    states = st.sidebar.multiselect(
        "Customer state",
        options=sorted(df["customer_state"].dropna().unique()),
        default=sorted(df["customer_state"].dropna().unique()),
        help="Focus on orders from specific states.",
    )

    categories = st.sidebar.multiselect(
        "Product category",
        options=sorted(df["category"].dropna().unique()),
        default=sorted(df["category"].dropna().unique()),
        help="Filter by product category.",
    )

    with st.sidebar.expander("More filters", expanded=False):
        min_rating = st.slider(
            "Minimum review rating",
            min_value=0.0,
            max_value=5.0,
            value=0.0,
            step=0.5,
            help="Show orders with review ratings above this threshold.",
        )

    filtered = df[
        (df["order_date"].dt.date >= min_date)
        & (df["order_date"].dt.date <= max_date)
        & (df["order_status_clean"].isin(order_status))
        & (df["customer_state"].isin(states))
        & (df["category"].isin(categories))
        & (df["rating"].fillna(0) >= min_rating)
    ]

    return filtered


def main() -> None:
    st.set_page_config(
        page_title="E-commerce Analytics Dashboard",
        layout="wide",
        page_icon="📈",
    )

    st.title("E-commerce Analytics Dashboard")
    st.markdown(
        "This dashboard now includes realistic order status distribution, profit metrics, delivery analytics, funnel conversion, and interactive filters for date, state, and product category."
    )
    st.warning(
        "Dataset is biased toward delivered orders, so delivered share may remain high even after filtering. Use the status distribution chart for the complete breakdown."
    )

    df = load_data()
    filtered_df = filter_data(df)

    if filtered_df.empty:
        st.warning("No data matches the current filter selection. Please adjust the filters.")
        return

    render_kpis(filtered_df)
    render_insights(filtered_df)
    render_charts(filtered_df)


if __name__ == "__main__":
    main()
