# ==========================================================
# INSIGHTFLOW AI
# PRODUCT ANALYTICS
# Version 2.0
# Developed by Swaroop K Samantaray
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.charts import (
    top_products_chart,
    bottom_products_chart,
    profitable_products_chart,
    subcategory_sales_chart,
    pareto_chart,
)

from utils.product_insights import product_insights


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def show_product_analytics(df):

    # ======================================================
    # EMPTY DATA PROTECTION
    # ======================================================

    if df is None or df.empty:

        st.warning(
            "⚠️ No product data available for the selected filters."
        )

        return

    # ======================================================
    # PAGE HEADER
    # ======================================================

    st.html(
        """
        <style>

        .if-page-header {
            width: 100%;
            box-sizing: border-box;

            padding: 36px 42px;
            margin-bottom: 28px;

            border-radius: 22px;

            border: 1px solid rgba(120, 160, 230, 0.20);

            background:
                radial-gradient(
                    circle at 88% 18%,
                    rgba(90, 110, 240, 0.20),
                    transparent 42%
                ),
                linear-gradient(
                    135deg,
                    #172640 0%,
                    #101a2c 55%,
                    #1b214b 100%
                );

            box-shadow:
                0 12px 35px rgba(0, 0, 0, 0.16);
        }

        .if-page-badge {
            display: inline-flex;
            align-items: center;

            padding: 8px 15px;
            margin-bottom: 16px;

            border-radius: 999px;

            border: 1px solid rgba(100, 160, 255, 0.30);

            background: rgba(45, 80, 145, 0.20);

            color: #8db7ff;

            font-size: 12px;
            font-weight: 700;

            letter-spacing: 0.7px;
        }

        .if-page-header h1 {
            margin: 0 0 12px 0;

            font-size: clamp(38px, 4vw, 58px);

            line-height: 1.05;

            font-weight: 850;

            letter-spacing: -2px;

            color: #f5f7ff;
        }

        .if-page-header h1 span {
            background: linear-gradient(
                90deg,
                #ffffff,
                #9abaff,
                #8ca5ff
            );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;

            background-clip: text;
        }

        .if-page-header p {
            max-width: 900px;

            margin: 0;

            font-size: 15px;

            line-height: 1.7;

            color: #9db7dc;
        }

        @media (max-width: 700px) {

            .if-page-header {
                padding: 30px 26px;
            }

            .if-page-header h1 {
                font-size: 40px;
                letter-spacing: -1.5px;
            }

        }

        </style>

        <section class="if-page-header">

            <div class="if-page-badge">
                📦 &nbsp; PRODUCT PERFORMANCE INTELLIGENCE
            </div>

            <h1>
                Product <span>Analytics</span>
            </h1>

            <p>
                Understand product performance, profitability,
                category contribution, revenue concentration and
                opportunities for product optimization.
            </p>

        </section>
        """
    )

    st.divider()

    # ======================================================
    # DATA PREPARATION
    # ======================================================

    data = df.copy()

    for column in [
        "Sales",
        "Profit",
        "Discount",
        "Quantity",
    ]:

        if column in data.columns:

            data[column] = pd.to_numeric(
                data[column],
                errors="coerce",
            )

    # ======================================================
    # BASIC PRODUCT METRICS
    # ======================================================

    total_products = (
        data["Product Name"].nunique()
        if "Product Name" in data.columns
        else 0
    )

    total_subcategories = (
        data["Sub-Category"].nunique()
        if "Sub-Category" in data.columns
        else 0
    )

    total_categories = (
        data["Category"].nunique()
        if "Category" in data.columns
        else 0
    )

    total_sales = (
        data["Sales"].sum()
        if "Sales" in data.columns
        else 0
    )

    total_profit = (
        data["Profit"].sum()
        if "Profit" in data.columns
        else 0
    )

    # ======================================================
    # PRODUCT SALES
    # ======================================================

    if (
        "Product Name" in data.columns
        and "Sales" in data.columns
    ):

        product_sales = (
            data.groupby("Product Name")["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

    else:

        product_sales = pd.Series(
            dtype=float
        )

    # ======================================================
    # PRODUCT PROFIT
    # ======================================================

    if (
        "Product Name" in data.columns
        and "Profit" in data.columns
    ):

        product_profit = (
            data.groupby("Product Name")["Profit"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

    else:

        product_profit = pd.Series(
            dtype=float
        )

    # ======================================================
    # AVERAGE PRODUCT SALES
    # ======================================================

    avg_product_sales = (
        product_sales.mean()
        if not product_sales.empty
        else 0
    )

    # ======================================================
    # AVERAGE PRODUCT PROFIT
    # ======================================================

    avg_product_profit = (
        product_profit.mean()
        if not product_profit.empty
        else 0
    )

    # ======================================================
    # PRODUCT MARGIN
    # ======================================================

    product_margin = (
        (total_profit / total_sales) * 100
        if total_sales != 0
        else 0
    )

    # ======================================================
    # TOP PRODUCT
    # ======================================================

    top_product = (
        product_sales.index[0]
        if not product_sales.empty
        else "N/A"
    )

    top_product_sales = (
        product_sales.iloc[0]
        if not product_sales.empty
        else 0
    )

    # ======================================================
    # TOP PROFITABLE PRODUCT
    # ======================================================

    top_profit_product = (
        product_profit.index[0]
        if not product_profit.empty
        else "N/A"
    )

    top_profit_value = (
        product_profit.iloc[0]
        if not product_profit.empty
        else 0
    )

    # ======================================================
    # PRODUCT PERFORMANCE KPIs
    # ======================================================

    st.subheader("📊 Product Performance")

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:

        st.metric(
            "📦 Products",
            f"{total_products:,}",
        )

    with k2:

        st.metric(
            "🗂️ Sub-Categories",
            f"{total_subcategories:,}",
        )

    with k3:

        st.metric(
            "🏷️ Categories",
            f"{total_categories:,}",
        )

    with k4:

        st.metric(
            "💰 Avg Sales / Product",
            f"${avg_product_sales:,.0f}",
        )

    with k5:

        st.metric(
            "📈 Product Margin",
            f"{product_margin:.2f}%",
        )

    # ======================================================
    # SECONDARY KPIs
    # ======================================================

    st.write("")

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.metric(
            "🏆 Top Product",
            str(top_product)[:25],
        )

    with s2:

        st.metric(
            "💵 Top Product Sales",
            f"${top_product_sales:,.0f}",
        )

    with s3:

        st.metric(
            "🥇 Most Profitable Product",
            str(top_profit_product)[:25],
        )

    with s4:

        st.metric(
            "💰 Avg Product Profit",
            f"${avg_product_profit:,.0f}",
        )

    st.divider()

    # ======================================================
    # TOP & BOTTOM PRODUCTS
    # ======================================================

    st.subheader("🏆 Product Performance Ranking")

    left, right = st.columns(2)

    with left:

        st.markdown(
            "#### 🚀 Top Products by Revenue"
        )

        try:

            fig_top = top_products_chart(
                data
            )

            st.plotly_chart(
                fig_top,
                use_container_width=True,
            )

        except Exception as error:

            st.warning(
                f"Unable to render top products chart: {error}"
            )

    with right:

        st.markdown(
            "#### ⚠️ Lowest Revenue Products"
        )

        try:

            fig_bottom = bottom_products_chart(
                data
            )

            st.plotly_chart(
                fig_bottom,
                use_container_width=True,
            )

        except Exception as error:

            st.warning(
                f"Unable to render bottom products chart: {error}"
            )

    st.divider()

    # ======================================================
    # PROFITABLE PRODUCTS + SUBCATEGORY
    # ======================================================

    st.subheader(
        "💹 Product Profitability & Category Structure"
    )

    left, right = st.columns(2)

    with left:

        st.markdown(
            "#### 💰 Most Profitable Products"
        )

        try:

            fig_profitable = profitable_products_chart(
                data
            )

            st.plotly_chart(
                fig_profitable,
                use_container_width=True,
            )

        except Exception as error:

            st.warning(
                f"Unable to render profitability chart: {error}"
            )

    with right:

        st.markdown(
            "#### 🗂️ Sub-Category Performance"
        )

        if "Sub-Category" in data.columns:

            try:

                fig_subcategory = subcategory_sales_chart(
                    data
                )

                st.plotly_chart(
                    fig_subcategory,
                    use_container_width=True,
                )

            except Exception as error:

                st.warning(
                    f"Unable to render sub-category chart: {error}"
                )

        else:

            st.info(
                "Sub-Category data unavailable."
            )

    st.divider()

    # ======================================================
    # PARETO ANALYSIS
    # ======================================================

    st.subheader(
        "🎯 Revenue Concentration Analysis"
    )

    st.markdown(
        """
        Pareto analysis identifies how much of total revenue
        is generated by the highest-performing products.
        """
    )

    try:

        fig_pareto = pareto_chart(
            data
        )

        st.plotly_chart(
            fig_pareto,
            use_container_width=True,
        )

    except Exception as error:

        st.warning(
            f"Unable to render Pareto analysis: {error}"
        )

    # ======================================================
    # PRODUCT CONCENTRATION METRICS
    # ======================================================

    top_5_share = 0
    top_10_share = 0
    top_20_share = 0

    if not product_sales.empty:

        total_product_revenue = (
            product_sales.sum()
        )

        top_5_revenue = (
            product_sales.head(5).sum()
        )

        top_10_revenue = (
            product_sales.head(10).sum()
        )

        top_20_revenue = (
            product_sales.head(20).sum()
        )

        if total_product_revenue != 0:

            top_5_share = (
                top_5_revenue
                / total_product_revenue
                * 100
            )

            top_10_share = (
                top_10_revenue
                / total_product_revenue
                * 100
            )

            top_20_share = (
                top_20_revenue
                / total_product_revenue
                * 100
            )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "🏆 Top 5 Revenue Share",
                f"{top_5_share:.1f}%",
            )

        with c2:

            st.metric(
                "📊 Top 10 Revenue Share",
                f"{top_10_share:.1f}%",
            )

        with c3:

            st.metric(
                "📈 Top 20 Revenue Share",
                f"{top_20_share:.1f}%",
            )

    st.divider()

    # ======================================================
    # PRODUCT PROFITABILITY MATRIX
    # ======================================================

    st.subheader(
        "📊 Product Sales vs Profitability"
    )

    if (
        "Product Name" in data.columns
        and "Sales" in data.columns
        and "Profit" in data.columns
    ):

        product_matrix = (
            data.groupby("Product Name")
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
            )
            .reset_index()
        )

        product_matrix["Margin"] = (
            product_matrix["Profit"]
            / product_matrix["Sales"]
            * 100
        )

        product_matrix["Margin"] = (
            product_matrix["Margin"]
            .replace(
                [float("inf"), -float("inf")],
                0,
            )
            .fillna(0)
        )

        # Keep the chart readable

        matrix_display = (
            product_matrix.copy()
        )

        if len(matrix_display) > 100:

            matrix_display = (
                matrix_display
                .sort_values(
                    "Sales",
                    ascending=False,
                )
                .head(100)
            )

        fig_matrix = px.scatter(
            matrix_display,
            x="Sales",
            y="Profit",
            size="Sales",
            color="Margin",
            hover_name="Product Name",
            hover_data={
                "Sales": ":,.0f",
                "Profit": ":,.0f",
                "Margin": ":.2f",
            },
            title=(
                "Product Revenue vs Profitability"
            ),
        )

        fig_matrix.update_layout(
            height=550,
            xaxis_title="Revenue",
            yaxis_title="Profit",
            margin=dict(
                l=20,
                r=20,
                t=55,
                b=20,
            ),
        )

        st.plotly_chart(
            fig_matrix,
            use_container_width=True,
        )

    else:

        st.info(
            "Required Product, Sales and Profit "
            "columns are unavailable."
        )

    st.divider()

    # ======================================================
    # PRODUCT PERFORMANCE TABLE
    # ======================================================

    st.subheader(
        "📋 Product Performance Table"
    )

    if (
        "Product Name" in data.columns
        and "Sales" in data.columns
    ):

        if "Profit" in data.columns:

            product_table = (
                data.groupby("Product Name")
                .agg(
                    Sales=("Sales", "sum"),
                    Profit=("Profit", "sum"),
                )
                .reset_index()
            )

            product_table["Margin"] = (
                product_table["Profit"]
                / product_table["Sales"]
                * 100
            )

        else:

            product_table = (
                data.groupby("Product Name")
                .agg(
                    Sales=("Sales", "sum"),
                )
                .reset_index()
            )

            product_table["Profit"] = 0

            product_table["Margin"] = 0

        product_table["Margin"] = (
            product_table["Margin"]
            .replace(
                [float("inf"), -float("inf")],
                0,
            )
            .fillna(0)
        )

        product_table = (
            product_table
            .sort_values(
                "Sales",
                ascending=False,
            )
        )

        st.dataframe(
            product_table.style.format(
                {
                    "Sales": "${:,.0f}",
                    "Profit": "${:,.0f}",
                    "Margin": "{:.2f}%",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "Product Name or Sales column is unavailable."
        )

    st.divider()

    # ======================================================
    # AUTOMATED PRODUCT INSIGHTS
    # ======================================================

    st.subheader(
        "🧠 Product Intelligence"
    )

    try:

        product_insights(
            data
        )

    except Exception as error:

        st.warning(
            f"Unable to generate product insights: {error}"
        )

    st.divider()

    # ======================================================
    # MANAGEMENT TAKEAWAYS
    # ======================================================

    st.subheader(
        "🎯 Management Takeaways"
    )

    takeaways = []

    # ------------------------------------------------------
    # Product concentration
    # ------------------------------------------------------

    if not product_sales.empty:

        if top_10_share >= 60:

            takeaways.append(
                "⚠️ Revenue is highly concentrated among the "
                "top products, with the top 10 generating "
                f"approximately {top_10_share:.1f}% of revenue. "
                "Management should monitor concentration risk."
            )

        elif top_10_share >= 40:

            takeaways.append(
                "🟡 The top 10 products contribute a significant "
                f"{top_10_share:.1f}% of revenue. Maintaining "
                "these products should remain a strategic priority."
            )

        else:

            takeaways.append(
                "🟢 Revenue is relatively diversified across "
                "the product portfolio."
            )

    # ------------------------------------------------------
    # Profitability
    # ------------------------------------------------------

    if product_margin >= 20:

        takeaways.append(
            "🟢 Overall product profitability is strong, "
            "suggesting a healthy product mix."
        )

    elif product_margin >= 10:

        takeaways.append(
            "🔵 Product profitability is healthy, although "
            "there is room to optimize the product mix."
        )

    elif product_margin >= 0:

        takeaways.append(
            "🟡 Product margins are relatively low. "
            "Low-margin products should be investigated "
            "for pricing, discounting and cost optimization."
        )

    else:

        takeaways.append(
            "🔴 The overall product portfolio is generating "
            "negative profitability and requires immediate review."
        )

    # ------------------------------------------------------
    # Top product
    # ------------------------------------------------------

    if top_product != "N/A":

        takeaways.append(
            f"🏆 **{top_product}** is the highest-revenue product "
            f"with approximately **${top_product_sales:,.0f}** "
            "in sales."
        )

    # ------------------------------------------------------
    # Profitable product
    # ------------------------------------------------------

    if top_profit_product != "N/A":

        takeaways.append(
            f"💰 **{top_profit_product}** is the strongest "
            f"profit-generating product with approximately "
            f"**${top_profit_value:,.0f}** in profit."
        )

    # ======================================================
    # DISPLAY TAKEAWAYS
    # ======================================================

    for takeaway in takeaways:

        st.info(
            takeaway
        )

    st.divider()

    # ======================================================
    # FOOTER
    # ======================================================

    st.caption(
        "InsightFlow AI • Product Analytics • "
        "All metrics and visualizations respond to the "
        "global filters selected in the sidebar."
    )