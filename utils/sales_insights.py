import streamlit as st


def sales_insights(df):

    best_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    best_category = (
        df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    best_segment = (
        df.groupby("Segment")["Sales"]
        .sum()
        .idxmax()
    )

    margin = (
        df["Profit"].sum()
        /
        df["Sales"].sum()
    ) * 100

    st.subheader("📊 Business Insights")

    st.success(f"""
✅ **Top Region:** {best_region}

🏆 **Best Category:** {best_category}

👥 **Highest Revenue Segment:** {best_segment}

💰 **Overall Profit Margin:** {margin:.2f}%
""")