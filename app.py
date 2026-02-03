import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Analytics Lite", layout="wide")

st.title("📊 Sales Analytics Lite")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    required_columns = {"date", "product", "region", "quantity", "revenue"}

    if not required_columns.issubset(df.columns):
        st.error("CSV must contain: date, product, region, quantity, revenue")
    else:
        df["date"] = pd.to_datetime(df["date"])

        # --- Raw data ---
        st.subheader("Raw Data")
        st.dataframe(df)

        # --- Metrics ---
        total_revenue = df["revenue"].sum()
        total_quantity = df["quantity"].sum()

        col1, col2 = st.columns(2)

        col1.metric("Total Revenue", f"${total_revenue:,.0f}")
        col2.metric("Total Units Sold", int(total_quantity))

        # --- Analytics ---
        df["month"] = df["date"].dt.to_period("M").astype(str)

        monthly_sales = df.groupby("month")["revenue"].sum().reset_index()

        top_products = (
            df.groupby("product")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        sales_by_region = (
            df.groupby("region")["revenue"]
            .sum()
            .reset_index()
        )

        # --- Charts ---
        st.subheader("📈 Monthly Revenue")
        fig_month = px.line(monthly_sales, x="month", y="revenue")
        st.plotly_chart(fig_month, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏆 Top Products")
            fig_products = px.bar(top_products, x="product", y="revenue")
            st.plotly_chart(fig_products, use_container_width=True)

        with col2:
            st.subheader("🌍 Revenue by Region")
            fig_region = px.pie(sales_by_region, names="region", values="revenue")
            st.plotly_chart(fig_region, use_container_width=True)
