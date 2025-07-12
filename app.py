import streamlit as st
import pandas as pd
import os
import datetime

st.set_page_config(page_title="SmartRetail 360° - Restock Alerts", layout='wide')
st.title("🚨 Live Restocking Alerts Dashboard")

#  Refresh Button
if 'refresh' not in st.session_state:
    st.session_state.refresh = False

if st.button("🔄 Refresh Data"):
    st.session_state.refresh = not st.session_state.refresh

# last updated time
st.caption(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Load Data
if os.path.exists("restock_alerts.csv"):
    df = pd.read_csv("restock_alerts.csv")
else:
    st.error("❌ restock_alerts.csv not found. Please export it from your notebook.")
    st.stop()

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
region_filter = st.sidebar.selectbox("Filter by Region", ['All'] + sorted(df['region'].unique()))
product_filter = st.sidebar.selectbox("Filter by Product ID", ['All'] + sorted(df['product_id'].unique()))

# Filter Data
filtered_df = df[df['restock_flag'] == 1]

if region_filter != 'All':
    filtered_df = filtered_df[filtered_df['region'] == region_filter]
if product_filter != 'All':
    filtered_df = filtered_df[filtered_df['product_id'] == product_filter]

st.subheader("🛒 Products Needing Restock")
st.dataframe(filtered_df[['product_id', 'region', 'inventory', 'predicted_units_sold', 'restock_qty']].sort_values(by='restock_qty', ascending=False))

st.subheader("📊 Restock Quantity per Product")
chart_df = filtered_df.groupby('product_id')['restock_qty'].sum().reset_index()
st.bar_chart(chart_df.set_index('product_id'))
