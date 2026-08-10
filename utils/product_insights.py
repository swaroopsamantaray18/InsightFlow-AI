import streamlit as st


def product_insights(df):

    top_product = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .idxmax()
    )

    profitable_product = (
        df.groupby("Product Name")["Profit"]
        .sum()
        .idxmax()
    )

    top_category = (
        df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    st.subheader("🤖 Product Insights")

    st.success(f"""
🏆 **Top Revenue Product**

{top_product}

💰 **Most Profitable Product**

{profitable_product}

📦 **Best Performing Category**

{top_category}

📈 **Recommendation**

Increase inventory and promotion for
**{top_category}**, especially the product:

**{top_product}**
""")