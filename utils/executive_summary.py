import streamlit as st


def executive_summary(df):

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()

    total_orders = df["Order ID"].nunique()

    total_customers = df["Customer ID"].nunique()

    avg_order = total_sales / total_orders

    profit_margin = (total_profit / total_sales) * 100

    st.success(f"""

# 📄 Executive Summary

The business generated **${total_sales:,.0f}**
from **{total_orders:,} orders**
served to **{total_customers:,} customers**.

The average order value is
**${avg_order:,.2f}**.

Overall profit stands at
**${total_profit:,.0f}**
with a healthy profit margin of
**{profit_margin:.2f}%**.

The dashboard below provides
detailed insights into regional
performance, product performance,
category trends and customer behavior.

""")