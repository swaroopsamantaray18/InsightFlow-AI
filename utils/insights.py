import streamlit as st


def generate_business_insights(df):

    # -----------------------------
    # Top Region
    # -----------------------------
    top_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
    )

    region_percent = (
        region_sales.max() /
        region_sales.sum()
    ) * 100

    # -----------------------------
    # Top Category
    # -----------------------------
    top_category = (
        df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    # -----------------------------
    # Top Product
    # -----------------------------
    top_product = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .idxmax()
    )

    # -----------------------------
    # Total Sales
    # -----------------------------
    total_sales = df["Sales"].sum()

    # -----------------------------
    # Total Profit
    # -----------------------------
    total_profit = df["Profit"].sum()

    # -----------------------------
    # Profit Margin
    # -----------------------------
    margin = (total_profit / total_sales) * 100

    st.info(
        f"""
### 🤖 AI Business Insights

✅ **Total Revenue**

The business generated **${total_sales:,.0f}** in total sales.

---

🌍 **Top Performing Region**

**{top_region}** contributes approximately **{region_percent:.1f}%**
of the company's revenue.

---

🏆 **Highest Revenue Category**

**{top_category}** is the strongest performing category.

---

📦 **Best Selling Product**

**{top_product}** generated the highest sales.

---

💰 **Overall Profit Margin**

Current profit margin is **{margin:.2f}%**.

---

### 📈 Business Recommendation

Increase investment in **{top_category}**
while maintaining inventory for
**{top_product}**.

Consider marketing initiatives in regions
outside **{top_region}**
to balance revenue distribution.
"""
    )