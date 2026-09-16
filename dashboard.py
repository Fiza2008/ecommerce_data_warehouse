import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

try:
    import plotly.express as px
except ImportError:
    px = None

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "ecommerce_warehouse.db"

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .main {
        background-color: #f7f8fc;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .hero {
        padding: 1.2rem 1.5rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #111827, #374151);
        color: white;
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        margin: 0;
        font-size: 2.1rem;
    }
    .hero p {
        margin: 0.35rem 0 0;
        color: #d1d5db;
    }
    .metric-card {
        background: white;
        padding: 1rem 1.1rem;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
    }
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    if not DB_PATH.exists():
        return None

    conn = sqlite3.connect(DB_PATH)

    fact = pd.read_sql_query("""
        SELECT
            f.*,
            d.date,
            d.year,
            d.quarter,
            d.month,
            d.month_name,
            c.customer_name,
            c.city AS customer_city,
            c.state AS customer_state,
            p.product_name,
            p.category,
            l.city,
            l.state
        FROM fact_sales f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_customer c ON f.customer_key = c.customer_key
        JOIN dim_product p ON f.product_key = p.product_key
        JOIN dim_location l ON f.location_key = l.location_key
    """, conn)

    conn.close()
    fact["date"] = pd.to_datetime(fact["date"])
    return fact


df = load_data()

if df is None:
    st.error("Database not found. Run `python -m etl.pipeline` first.")
    st.stop()

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>🛒 E-Commerce Analytics Dashboard</h1>
    <p>SQL-powered business intelligence from a Python-built data warehouse</p>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar filters ----------
st.sidebar.title("🎛️ Filters")

categories = sorted(df["category"].dropna().unique().tolist())
cities = sorted(df["city"].dropna().unique().tolist())
statuses = sorted(df["status"].dropna().unique().tolist())

selected_categories = st.sidebar.multiselect(
    "Product Category",
    categories,
    default=categories
)

selected_cities = st.sidebar.multiselect(
    "City",
    cities,
    default=cities
)

selected_statuses = st.sidebar.multiselect(
    "Order Status",
    statuses,
    default=["Completed"] if "Completed" in statuses else statuses
)

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered = df[
    df["category"].isin(selected_categories)
    & df["city"].isin(selected_cities)
    & df["status"].isin(selected_statuses)
].copy()

if len(date_range) == 2:
    filtered = filtered[
        (filtered["date"].dt.date >= date_range[0])
        & (filtered["date"].dt.date <= date_range[1])
    ]

# ---------- KPIs ----------
completed = filtered[filtered["status"] == "Completed"]

revenue = completed["net_sales"].sum()
orders = completed["order_id"].nunique()
units = completed["quantity"].sum()
aov = revenue / orders if orders else 0

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Revenue", f"₹{revenue:,.0f}")
c2.metric("🧾 Completed Orders", f"{orders:,}")
c3.metric("📦 Units Sold", f"{units:,.0f}")
c4.metric("🛍️ Average Order Value", f"₹{aov:,.0f}")

st.markdown('<div class="section-title">📈 Sales Performance</div>', unsafe_allow_html=True)

# ---------- Charts ----------
monthly = (
    completed.groupby(["year", "month", "month_name"], as_index=False)["net_sales"]
    .sum()
    .sort_values(["year", "month"])
)
monthly["period"] = monthly["month_name"].str[:3] + " " + monthly["year"].astype(str)

category = (
    completed.groupby("category", as_index=False)["net_sales"]
    .sum()
    .sort_values("net_sales", ascending=False)
)

top_products = (
    completed.groupby("product_name", as_index=False)
    .agg(revenue=("net_sales", "sum"), units=("quantity", "sum"))
    .sort_values("revenue", ascending=False)
    .head(10)
)

city = (
    completed.groupby(["city", "state"], as_index=False)["net_sales"]
    .sum()
    .sort_values("net_sales", ascending=False)
)

if px:
    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            monthly,
            x="period",
            y="net_sales",
            markers=True,
            title="Monthly Revenue Trend",
            labels={"period": "Month", "net_sales": "Revenue (₹)"}
        )
        fig.update_layout(height=370, margin=dict(l=10,r=10,t=55,b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            category,
            x="category",
            y="net_sales",
            title="Revenue by Category",
            labels={"category": "Category", "net_sales": "Revenue (₹)"}
        )
        fig.update_layout(height=370, margin=dict(l=10,r=10,t=55,b=10))
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig = px.bar(
            top_products.sort_values("revenue"),
            x="revenue",
            y="product_name",
            orientation="h",
            title="Top 10 Products by Revenue",
            labels={"revenue": "Revenue (₹)", "product_name": "Product"}
        )
        fig.update_layout(height=430, margin=dict(l=10,r=10,t=55,b=10))
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = px.bar(
            city.head(10).sort_values("net_sales"),
            x="net_sales",
            y="city",
            orientation="h",
            title="Top Cities by Revenue",
            labels={"net_sales": "Revenue (₹)", "city": "City"}
        )
        fig.update_layout(height=430, margin=dict(l=10,r=10,t=55,b=10))
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Plotly is not installed. Run `pip install plotly` to enable charts.")

# ---------- Tables ----------
st.markdown('<div class="section-title">🏆 Top Customers</div>', unsafe_allow_html=True)

top_customers = (
    completed.groupby(["customer_name", "customer_city", "customer_state"], as_index=False)
    .agg(
        orders=("order_id", "nunique"),
        units=("quantity", "sum"),
        spending=("net_sales", "sum")
    )
    .sort_values("spending", ascending=False)
    .head(10)
)

top_customers["spending"] = top_customers["spending"].round(2)

st.dataframe(
    top_customers.rename(columns={
        "customer_name": "Customer",
        "customer_city": "City",
        "customer_state": "State",
        "orders": "Orders",
        "units": "Units",
        "spending": "Total Spend"
    }),
    use_container_width=True,
    hide_index=True
)

st.markdown('<div class="section-title">🔍 Data Warehouse Summary</div>', unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
s1.metric("Fact Rows", f"{len(df):,}")
s2.metric("Customers", f"{df['customer_key'].nunique():,}")
s3.metric("Products", f"{df['product_key'].nunique():,}")
s4.metric("Cities", f"{df['city'].nunique():,}")

st.caption(
    "Built with Python, Pandas, SQL, SQLite and Streamlit. "
    "Data is generated for portfolio/learning purposes."
)
