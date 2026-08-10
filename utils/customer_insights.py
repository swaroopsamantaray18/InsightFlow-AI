import streamlit as st


def customer_insights(df):

    top_customer = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .idxmax()
    )

    top_sales = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .max()
    )

    loyal_customer = (
        df.groupby("Customer Name")
        .size()
        .idxmax()
    )

    loyal_orders = (
        df.groupby("Customer Name")
        .size()
        .max()
    )

    avg_value = (
        df["Sales"].sum() /
        df["Customer ID"].nunique()
    )

    st.subheader("🤖 Customer Insights")

    st.success(f"""
🏆 **Highest Revenue Customer**

{top_customer}

Revenue

${top_sales:,.0f}

---

👑 **Most Loyal Customer**

{loyal_customer}

Orders

{loyal_orders}

---

💰 **Average Customer Value**

${avg_value:,.0f}

---

📈 **Recommendation**

Reward your highest-value customers with loyalty programs while re-engaging inactive customers through targeted marketing campaigns.
""")