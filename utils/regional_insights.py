import streamlit as st


def regional_insights(df):

    # -----------------------
    # Top Region
    # -----------------------

    top_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    top_region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .max()
    )

    # -----------------------
    # Top State
    # -----------------------

    top_state = (
    df.groupby("State/Province")["Sales"]
    .sum()
    .idxmax()
)

    top_state_sales = (
    df.groupby("State/Province")["Sales"]
    .sum()
    .max()
)

    # -----------------------
    # Highest Profit Region
    # -----------------------

    profit_region = (
        df.groupby("Region")["Profit"]
        .sum()
        .idxmax()
    )

    highest_profit = (
        df.groupby("Region")["Profit"]
        .sum()
        .max()
    )

    # -----------------------
    # Weakest Region
    # -----------------------

    weakest_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmin()
    )

    weakest_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .min()
    )

    st.subheader("🤖 Regional Insights")

    col1, col2 = st.columns(2)

    with col1:

        st.success(f"""
🌍 **Top Performing Region**

**{top_region}**

Revenue

**${top_region_sales:,.0f}**

---

📍 **Top State**

**{top_state}**

Revenue

**${top_state_sales:,.0f}**
""")

    with col2:

        st.info(f"""
💰 **Highest Profit Region**

**{profit_region}**

Profit

**${highest_profit:,.0f}**

---

⚠ **Weakest Region**

**{weakest_region}**

Revenue

**${weakest_sales:,.0f}**

---

📈 **Recommendation**

Increase marketing investment in
**{weakest_region}**
while continuing expansion in
**{top_region}**.
""")