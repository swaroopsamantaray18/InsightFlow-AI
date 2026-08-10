import streamlit as st


def show_highlights(df):

    # -----------------------
    # Top Region
    # -----------------------

    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
    )

    top_region = region_sales.idxmax()

    # -----------------------
    # Top Category
    # -----------------------

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
    )

    top_category = category_sales.idxmax()

    # -----------------------
    # Best Product
    # -----------------------

    product_sales = (
        df.groupby("Product Name")["Sales"]
        .sum()
    )

    top_product = product_sales.idxmax()

    # -----------------------
    # Profit Margin
    # -----------------------

    total_sales = df["Sales"].sum()

    total_profit = df["Profit"].sum()

    margin = (total_profit / total_sales) * 100

    # -----------------------
    # Average Order
    # -----------------------

    avg_order = (
        total_sales /
        df["Order ID"].nunique()
    )

    st.subheader("🤖 AI Highlights")

    col1, col2 = st.columns(2)

    with col1:

        st.success(f"""
🏆 **Best Category**

{top_category}

🌍 **Top Region**

{top_region}

💰 **Profit Margin**

{margin:.2f}%
""")

    with col2:

        st.info(f"""
📦 **Top Product**

{top_product}

🛒 **Average Order Value**

${avg_order:,.2f}

📈 **Recommendation**

Increase investment in **{top_category}**
while expanding market share outside
**{top_region}**.
""")