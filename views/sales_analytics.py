# ==========================================================
# INSIGHTFLOW AI
# SALES ANALYTICS
# Version 2.0
# Developed by Swaroop K Samantaray
# ==========================================================

import streamlit as st
import pandas as pd

from utils.sales_insights import sales_insights

from utils.charts import (
    monthly_sales_chart,
    region_sales_chart,
    category_sales_chart,
    profit_by_category_chart,
    segment_sales_chart,
    shipmode_chart,
    discount_profit_chart,
)

from utils.kpi import calculate_kpis


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def show_sales_analytics(df):

    # ======================================================
    # EMPTY DATA PROTECTION
    # ======================================================

    if df is None or df.empty:

        st.warning(
            "⚠️ No sales data available for the selected filters."
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
                📈 &nbsp; SALES PERFORMANCE INTELLIGENCE
            </div>

            <h1>
                Sales <span>Analytics</span>
            </h1>

            <p>
                Analyze revenue performance, sales trends,
                profitability, customer segments and operational
                drivers through interactive business intelligence.
            </p>

        </section>
        """
    )

    # ======================================================
    # DATA PREPARATION
    # ======================================================

    data = df.copy()

    # ------------------------------------------------------
    # Numeric conversion
    # ------------------------------------------------------

    for column in [
        "Sales",
        "Profit",
        "Discount",
    ]:

        if column in data.columns:

            data[column] = pd.to_numeric(
                data[column],
                errors="coerce",
            )

    # ------------------------------------------------------
    # Date conversion
    # ------------------------------------------------------

    if "Order Date" in data.columns:

        data["Order Date"] = pd.to_datetime(
            data["Order Date"],
            errors="coerce",
        )

    # ======================================================
    # CORE KPIs
    # ======================================================

    (
        total_sales,
        total_profit,
        total_orders,
        total_customers,
    ) = calculate_kpis(data)

    profit_margin = (
        (total_profit / total_sales) * 100
        if total_sales != 0
        else 0
    )

    average_order_value = (
        total_sales / total_orders
        if total_orders != 0
        else 0
    )

    # ======================================================
    # MONTHLY GROWTH
    # ======================================================

    current_month_sales = 0

    previous_month_sales = 0

    monthly_growth = 0

    if (
        "Order Date" in data.columns
        and "Sales" in data.columns
    ):

        monthly_sales = (
            data
            .dropna(subset=["Order Date"])
            .groupby(
                pd.Grouper(
                    key="Order Date",
                    freq="ME",
                )
            )["Sales"]
            .sum()
            .sort_index()
        )

        if len(monthly_sales) >= 2:

            current_month_sales = monthly_sales.iloc[-1]

            previous_month_sales = monthly_sales.iloc[-2]

            if previous_month_sales != 0:

                monthly_growth = (
                    (
                        current_month_sales
                        - previous_month_sales
                    )
                    / previous_month_sales
                ) * 100

    # ======================================================
    # PAGE PERFORMANCE HEADER
    # ======================================================

    st.subheader("📊 Sales Performance")

    # ======================================================
    # PRIMARY KPI CARDS
    # ======================================================

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:

        st.metric(
            "💰 Total Sales",
            f"${total_sales:,.0f}",
        )

    with k2:

        st.metric(
            "📈 Total Profit",
            f"${total_profit:,.0f}",
        )

    with k3:

        st.metric(
            "🎯 Profit Margin",
            f"{profit_margin:.2f}%",
        )

    with k4:

        st.metric(
            "📦 Orders",
            f"{total_orders:,}",
        )

    with k5:

        st.metric(
            "👥 Customers",
            f"{total_customers:,}",
        )

    # ======================================================
    # SECONDARY KPIs
    # ======================================================

    st.write("")

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.metric(
            "🧾 Average Order Value",
            f"${average_order_value:,.0f}",
        )

    with s2:

        if previous_month_sales:

            st.metric(
                "📅 Latest Month",
                f"${current_month_sales:,.0f}",
            )

        else:

            st.metric(
                "📅 Latest Month",
                "N/A",
            )

    with s3:

        if previous_month_sales:

            st.metric(
                "📊 Monthly Growth",
                f"{monthly_growth:+.2f}%",
            )

        else:

            st.metric(
                "📊 Monthly Growth",
                "N/A",
            )

    with s4:

        if profit_margin >= 20:

            health = "Excellent"

        elif profit_margin >= 10:

            health = "Healthy"

        elif profit_margin >= 0:

            health = "Watch"

        else:

            health = "Critical"

        st.metric(
            "❤️ Sales Health",
            health,
        )

    st.divider()

    # ======================================================
    # REVENUE TREND
    # ======================================================

    st.subheader("📈 Revenue Trend")

    if "Order Date" in data.columns:

        try:

            monthly_chart = monthly_sales_chart(data)

            st.plotly_chart(
                monthly_chart,
                use_container_width=True,
            )

        except Exception as error:

            st.warning(
                f"Unable to render the monthly sales chart: {error}"
            )

    else:

        st.info(
            "Order Date is unavailable for trend analysis."
        )

    st.divider()

    # ======================================================
    # REGIONAL + CATEGORY SALES
    # ======================================================

    st.subheader("🌍 Sales Performance by Market")

    left, right = st.columns(2)

    # ======================================================
    # REGIONAL SALES
    # ======================================================

    with left:

        st.markdown(
            "#### 🌍 Regional Sales"
        )

        if "Region" in data.columns:

            try:

                fig_region = region_sales_chart(data)

                st.plotly_chart(
                    fig_region,
                    use_container_width=True,
                )

            except Exception as error:

                st.warning(
                    f"Unable to render regional analysis: {error}"
                )

        else:

            st.info(
                "Region data unavailable."
            )

    # ======================================================
    # CATEGORY SALES
    # ======================================================

    with right:

        st.markdown(
            "#### 📦 Category Sales"
        )

        if "Category" in data.columns:

            try:

                fig_category = category_sales_chart(data)

                st.plotly_chart(
                    fig_category,
                    use_container_width=True,
                )

            except Exception as error:

                st.warning(
                    f"Unable to render category analysis: {error}"
                )

        else:

            st.info(
                "Category data unavailable."
            )

    st.divider()

    # ======================================================
    # PROFITABILITY ANALYSIS
    # ======================================================

    st.subheader("💹 Profitability Intelligence")

    left, right = st.columns(2)

    # ======================================================
    # PROFIT BY CATEGORY
    # ======================================================

    with left:

        st.markdown(
            "#### 💰 Profit by Category"
        )

        if (
            "Category" in data.columns
            and "Profit" in data.columns
        ):

            try:

                fig_profit = profit_by_category_chart(data)

                st.plotly_chart(
                    fig_profit,
                    use_container_width=True,
                )

            except Exception as error:

                st.warning(
                    f"Unable to render profitability analysis: {error}"
                )

        else:

            st.info(
                "Category or Profit data unavailable."
            )

    # ======================================================
    # DISCOUNT VS PROFIT
    # ======================================================

    with right:

        st.markdown(
            "#### 🏷️ Discount vs Profit"
        )

        if (
            "Discount" in data.columns
            and "Profit" in data.columns
        ):

            try:

                fig_discount = discount_profit_chart(data)

                st.plotly_chart(
                    fig_discount,
                    use_container_width=True,
                )

            except Exception as error:

                st.warning(
                    f"Unable to render discount analysis: {error}"
                )

        else:

            st.info(
                "Discount or Profit data unavailable."
            )

    st.divider()

    # ======================================================
    # CUSTOMER + SHIPPING ANALYSIS
    # ======================================================

    st.subheader("👥 Customer & Operational Analysis")

    left, right = st.columns(2)

    # ======================================================
    # CUSTOMER SEGMENT
    # ======================================================

    with left:

        st.markdown(
            "#### 👥 Customer Segment Sales"
        )

        if "Segment" in data.columns:

            try:

                fig_segment = segment_sales_chart(data)

                st.plotly_chart(
                    fig_segment,
                    use_container_width=True,
                )

            except Exception as error:

                st.warning(
                    f"Unable to render segment analysis: {error}"
                )

        else:

            st.info(
                "Segment data unavailable."
            )

    # ======================================================
    # SHIPPING MODE
    # ======================================================

    with right:

        st.markdown(
            "#### 🚚 Shipping Mode Distribution"
        )

        try:

            fig_shipmode = shipmode_chart(data)

            st.plotly_chart(
                fig_shipmode,
                use_container_width=True,
            )

        except Exception as error:

            st.warning(
                f"Unable to render shipping analysis: {error}"
            )

    st.divider()

    # ======================================================
    # SALES BREAKDOWN TABLE
    # ======================================================

    st.subheader("📋 Sales Breakdown")

    table_col1, table_col2 = st.columns(2)

    # ======================================================
    # CATEGORY TABLE
    # ======================================================

    with table_col1:

        if (
            "Category" in data.columns
            and "Sales" in data.columns
        ):

            category_summary = (
                data
                .groupby("Category")
                .agg(
                    Sales=("Sales", "sum"),
                    Profit=(
                        "Profit",
                        "sum",
                    )
                    if "Profit" in data.columns
                    else (
                        "Sales",
                        "sum",
                    ),
                )
                .reset_index()
            )

            category_summary["Margin"] = (
                category_summary["Profit"]
                / category_summary["Sales"]
                * 100
            ).replace(
                [float("inf"), -float("inf")],
                0,
            ).fillna(0)

            category_summary = (
                category_summary
                .sort_values(
                    "Sales",
                    ascending=False,
                )
            )

            st.dataframe(
                category_summary.style.format(
                    {
                        "Sales": "${:,.0f}",
                        "Profit": "${:,.0f}",
                        "Margin": "{:.2f}%",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    # ======================================================
    # REGION TABLE
    # ======================================================

    with table_col2:

        if (
            "Region" in data.columns
            and "Sales" in data.columns
        ):

            region_summary = (
                data
                .groupby("Region")
                .agg(
                    Sales=("Sales", "sum"),
                    Profit=(
                        "Profit",
                        "sum",
                    )
                    if "Profit" in data.columns
                    else (
                        "Sales",
                        "sum",
                    ),
                )
                .reset_index()
            )

            region_summary["Margin"] = (
                region_summary["Profit"]
                / region_summary["Sales"]
                * 100
            ).replace(
                [float("inf"), -float("inf")],
                0,
            ).fillna(0)

            region_summary = (
                region_summary
                .sort_values(
                    "Sales",
                    ascending=False,
                )
            )

            st.dataframe(
                region_summary.style.format(
                    {
                        "Sales": "${:,.0f}",
                        "Profit": "${:,.0f}",
                        "Margin": "{:.2f}%",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    st.divider()

    # ======================================================
    # SALES CONCENTRATION
    # ======================================================

    st.subheader("🎯 Revenue Concentration")

    if (
        "Product Name" in data.columns
        and "Sales" in data.columns
    ):

        product_sales = (
            data
            .groupby("Product Name")["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        if not product_sales.empty:

            top_10_sales = (
                product_sales
                .head(10)
                .sum()
            )

            total_product_sales = (
                product_sales.sum()
            )

            concentration = (
                top_10_sales
                / total_product_sales
                * 100
                if total_product_sales != 0
                else 0
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "🏆 Top Product",
                    str(
                        product_sales.index[0]
                    ),
                )

            with c2:

                st.metric(
                    "📊 Top 10 Products Revenue",
                    f"${top_10_sales:,.0f}",
                )

            with c3:

                st.metric(
                    "🎯 Top 10 Revenue Share",
                    f"{concentration:.1f}%",
                )

    st.divider()

    # ======================================================
    # BUSINESS INSIGHTS
    # ======================================================

    st.subheader("🧠 Sales Intelligence")

    try:

        sales_insights(data)

    except Exception as error:

        st.warning(
            f"Unable to generate sales insights: {error}"
        )

    st.divider()

    # ======================================================
    # AUTOMATED TAKEAWAYS
    # ======================================================

    st.subheader("🎯 Management Takeaways")

    takeaways = []

    # ------------------------------------------------------
    # Profitability
    # ------------------------------------------------------

    if profit_margin >= 20:

        takeaways.append(
            "🟢 Strong profitability indicates that the current "
            "sales mix is generating healthy returns."
        )

    elif profit_margin >= 10:

        takeaways.append(
            "🔵 Profitability is healthy, but there is potential "
            "to improve margins through product and pricing optimization."
        )

    elif profit_margin >= 0:

        takeaways.append(
            "🟡 Revenue is positive, but margins should be monitored "
            "closely to prevent profitability erosion."
        )

    else:

        takeaways.append(
            "🔴 The business is operating at a loss. Pricing, "
            "discounting and product-level profitability require "
            "immediate attention."
        )

    # ------------------------------------------------------
    # Growth
    # ------------------------------------------------------

    if previous_month_sales:

        if monthly_growth > 10:

            takeaways.append(
                f"🚀 Sales momentum is strong, with monthly revenue "
                f"growing by {monthly_growth:.2f}%."
            )

        elif monthly_growth > 0:

            takeaways.append(
                f"📈 Sales are growing moderately at "
                f"{monthly_growth:.2f}% month-over-month."
            )

        else:

            takeaways.append(
                f"📉 Sales declined by "
                f"{abs(monthly_growth):.2f}% month-over-month. "
                f"Investigate the drivers behind the slowdown."
            )

    # ------------------------------------------------------
    # AOV
    # ------------------------------------------------------

    if average_order_value > 0:

        takeaways.append(
            f"🧾 The average order value is "
            f"**${average_order_value:,.0f}**, providing a useful "
            f"baseline for future upselling and cross-selling strategies."
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
        "InsightFlow AI • Sales Analytics • "
        "All metrics and visualizations respond to the "
        "global filters selected in the sidebar."
    )