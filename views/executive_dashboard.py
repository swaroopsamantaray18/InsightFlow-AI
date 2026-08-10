# ==========================================================
# INSIGHTFLOW AI
# EXECUTIVE COMMAND CENTER
# Version 2.0
# Developed by Swaroop K Samantaray
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def show_executive_dashboard(df):

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
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.16);
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
            background: linear-gradient(90deg, #ffffff, #9abaff, #8ca5ff);
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
                🏢 &nbsp; EXECUTIVE BUSINESS INTELLIGENCE
            </div>

            <h1>
                Executive <span>Command Center</span>
            </h1>

            <p>
                Monitor business performance, profitability,
                customers, products and market trends from one
                executive analytics environment.
            </p>

        </section>
        """
    )

    st.divider()

    # ======================================================
    # EMPTY DATA PROTECTION
    # ======================================================

    if df is None or df.empty:

        st.warning(
            "⚠️ No data available for the selected filters."
        )

        return

    # ======================================================
    # DATA PREPARATION
    # ======================================================

    data = df.copy()

    # ------------------------------------------------------
    # Convert numeric columns
    # ------------------------------------------------------

    for column in ["Sales", "Profit"]:

        if column in data.columns:

            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    # ------------------------------------------------------
    # Convert date
    # ------------------------------------------------------

    if "Order Date" in data.columns:

        data["Order Date"] = pd.to_datetime(
            data["Order Date"],
            errors="coerce"
        )

    # ======================================================
    # CORE BUSINESS METRICS
    # ======================================================

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

    total_orders = (
        data["Order ID"].nunique()
        if "Order ID" in data.columns
        else len(data)
    )

    total_customers = (
        data["Customer ID"].nunique()
        if "Customer ID" in data.columns
        else 0
    )

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
    sales_growth = 0

    if (
        "Order Date" in data.columns
        and "Sales" in data.columns
    ):

        monthly_growth = (
            data.dropna(subset=["Order Date"])
            .groupby(
                pd.Grouper(
                    key="Order Date",
                    freq="ME"
                )
            )["Sales"]
            .sum()
            .sort_index()
        )

        if len(monthly_growth) >= 2:

            current_month_sales = monthly_growth.iloc[-1]

            previous_month_sales = monthly_growth.iloc[-2]

            if previous_month_sales != 0:

                sales_growth = (
                    (
                        current_month_sales
                        - previous_month_sales
                    )
                    / previous_month_sales
                ) * 100

    # ======================================================
    # BUSINESS PERFORMANCE HEADER
    # ======================================================

    st.subheader("📊 Business Performance")

    # ======================================================
    # KPI CARDS
    # ======================================================

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    # ------------------------------------------------------
    # Revenue
    # ------------------------------------------------------

    with kpi1:

        st.metric(
            "💰 Revenue",
            f"${total_sales:,.0f}"
        )

    # ------------------------------------------------------
    # Profit
    # ------------------------------------------------------

    with kpi2:

        st.metric(
            "📈 Profit",
            f"${total_profit:,.0f}"
        )

    # ------------------------------------------------------
    # Margin
    # ------------------------------------------------------

    with kpi3:

        st.metric(
            "🎯 Profit Margin",
            f"{profit_margin:.2f}%"
        )

    # ------------------------------------------------------
    # Orders
    # ------------------------------------------------------

    with kpi4:

        st.metric(
            "🛒 Orders",
            f"{total_orders:,}"
        )

    # ------------------------------------------------------
    # Customers
    # ------------------------------------------------------

    with kpi5:

        st.metric(
            "👥 Customers",
            f"{total_customers:,}"
        )

    # ======================================================
    # SECONDARY KPIs
    # ======================================================

    st.write("")

    secondary1, secondary2, secondary3, secondary4 = st.columns(4)

    with secondary1:

        st.metric(
            "💵 Average Order Value",
            f"${average_order_value:,.0f}"
        )

    with secondary2:

        st.metric(
            "📅 Latest Monthly Sales",
            f"${current_month_sales:,.0f}"
            if current_month_sales
            else "N/A"
        )

    with secondary3:

        st.metric(
            "📊 Monthly Growth",
            f"{sales_growth:+.2f}%"
            if previous_month_sales
            else "N/A"
        )

    with secondary4:

        if profit_margin >= 20:

            health = "Excellent"

        elif profit_margin >= 10:

            health = "Healthy"

        elif profit_margin >= 0:

            health = "Watch"

        else:

            health = "Critical"

        st.metric(
            "❤️ Business Health",
            health
        )

    st.divider()

    # ======================================================
    # BUSINESS SNAPSHOT
    # ======================================================

    st.subheader("⚡ Business Snapshot")

    snapshot1, snapshot2, snapshot3, snapshot4 = st.columns(4)

    # ======================================================
    # TOP REGION
    # ======================================================

    top_region = "N/A"
    top_region_sales = 0

    if (
        "Region" in data.columns
        and "Sales" in data.columns
    ):

        region_sales = (
            data.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        if not region_sales.empty:

            top_region = str(region_sales.index[0])

            top_region_sales = region_sales.iloc[0]

    # ======================================================
    # TOP CATEGORY
    # ======================================================

    top_category = "N/A"
    top_category_sales = 0

    if (
        "Category" in data.columns
        and "Sales" in data.columns
    ):

        category_sales = (
            data.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        if not category_sales.empty:

            top_category = str(category_sales.index[0])

            top_category_sales = category_sales.iloc[0]

    # ======================================================
    # TOP SEGMENT
    # ======================================================

    top_segment = "N/A"
    top_segment_sales = 0

    if (
        "Segment" in data.columns
        and "Sales" in data.columns
    ):

        segment_sales = (
            data.groupby("Segment")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        if not segment_sales.empty:

            top_segment = str(segment_sales.index[0])

            top_segment_sales = segment_sales.iloc[0]

    # ======================================================
    # TOP PRODUCT
    # ======================================================

    top_product = "N/A"

    if (
        "Product Name" in data.columns
        and "Sales" in data.columns
    ):

        product_sales = (
            data.groupby("Product Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        if not product_sales.empty:

            top_product = str(product_sales.index[0])

    # ======================================================
    # SNAPSHOT DISPLAY
    # ======================================================

    with snapshot1:

        st.metric(
            "🌍 Top Region",
            top_region
        )

        st.caption(
            f"${top_region_sales:,.0f} revenue"
        )

    with snapshot2:

        st.metric(
            "📦 Top Category",
            top_category
        )

        st.caption(
            f"${top_category_sales:,.0f} revenue"
        )

    with snapshot3:

        st.metric(
            "👥 Top Segment",
            top_segment
        )

        st.caption(
            f"${top_segment_sales:,.0f} revenue"
        )

    with snapshot4:

        st.metric(
            "🏆 Top Product",
            top_product
        )

    st.divider()

    # ======================================================
    # REVENUE & PROFIT TREND
    # ======================================================

    st.subheader("📈 Revenue & Profit Trend")

    if (
        "Order Date" in data.columns
        and "Sales" in data.columns
        and "Profit" in data.columns
    ):

        monthly = (
            data.dropna(subset=["Order Date"])
            .groupby(
                pd.Grouper(
                    key="Order Date",
                    freq="ME"
                )
            )
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum")
            )
            .reset_index()
        )

        if not monthly.empty:

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=monthly["Order Date"],
                    y=monthly["Sales"],
                    mode="lines+markers",
                    name="Revenue",
                    line=dict(
                        width=3
                    ),
                    marker=dict(
                        size=7
                    )
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=monthly["Order Date"],
                    y=monthly["Profit"],
                    mode="lines+markers",
                    name="Profit",
                    line=dict(
                        width=3
                    ),
                    marker=dict(
                        size=7
                    )
                )
            )

            fig.update_layout(
                height=450,
                xaxis_title="Month",
                yaxis_title="Amount",
                hovermode="x unified",
                legend_title="Metric",
                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Not enough date information to display the trend."
            )

    else:

        st.info(
            "Required sales, profit or date columns are unavailable."
        )

    # ======================================================
    # REGIONAL + CATEGORY
    # ======================================================

    col1, col2 = st.columns(2)

    # ======================================================
    # REGIONAL PERFORMANCE
    # ======================================================

    with col1:

        st.subheader("🌍 Regional Performance")

        if (
            "Region" in data.columns
            and "Sales" in data.columns
        ):

            regional = (
                data.groupby("Region")
                .agg(
                    Sales=("Sales", "sum"),
                    Profit=("Profit", "sum")
                )
                .reset_index()
                .sort_values(
                    "Sales",
                    ascending=False
                )
            )

            fig_region = px.bar(
                regional,
                x="Region",
                y="Sales",
                color="Profit",
                text_auto=".2s",
                title="Revenue by Region"
            )

            fig_region.update_layout(
                height=420,
                xaxis_title="Region",
                yaxis_title="Revenue",
                margin=dict(
                    l=20,
                    r=20,
                    t=50,
                    b=20
                )
            )

            st.plotly_chart(
                fig_region,
                use_container_width=True
            )

        else:

            st.info(
                "Region data unavailable."
            )

    # ======================================================
    # CATEGORY PERFORMANCE
    # ======================================================

    with col2:

        st.subheader("📦 Category Performance")

        if (
            "Category" in data.columns
            and "Sales" in data.columns
        ):

            category_data = (
                data.groupby("Category")
                .agg(
                    Sales=("Sales", "sum"),
                    Profit=("Profit", "sum")
                )
                .reset_index()
                .sort_values(
                    "Sales",
                    ascending=False
                )
            )

            fig_category = px.bar(
                category_data,
                x="Category",
                y="Sales",
                color="Profit",
                text_auto=".2s",
                title="Revenue by Category"
            )

            fig_category.update_layout(
                height=420,
                xaxis_title="Category",
                yaxis_title="Revenue",
                margin=dict(
                    l=20,
                    r=20,
                    t=50,
                    b=20
                )
            )

            st.plotly_chart(
                fig_category,
                use_container_width=True
            )

        else:

            st.info(
                "Category data unavailable."
            )

    st.divider()

    # ======================================================
    # CUSTOMER SEGMENT + PROFITABILITY
    # ======================================================

    col1, col2 = st.columns(2)

    # ======================================================
    # CUSTOMER SEGMENTS
    # ======================================================

    with col1:

        st.subheader("👥 Customer Segment Performance")

        if (
            "Segment" in data.columns
            and "Sales" in data.columns
        ):

            segment_data = (
                data.groupby("Segment")
                .agg(
                    Sales=("Sales", "sum"),
                    Profit=("Profit", "sum")
                )
                .reset_index()
            )

            fig_segment = px.pie(
                segment_data,
                names="Segment",
                values="Sales",
                hole=0.52,
                title="Revenue Distribution by Segment"
            )

            fig_segment.update_layout(
                height=420,
                margin=dict(
                    l=20,
                    r=20,
                    t=50,
                    b=20
                )
            )

            st.plotly_chart(
                fig_segment,
                use_container_width=True
            )

        else:

            st.info(
                "Segment data unavailable."
            )

    # ======================================================
    # PROFITABILITY
    # ======================================================

    with col2:

        st.subheader("💹 Profitability by Category")

        if (
            "Category" in data.columns
            and "Sales" in data.columns
            and "Profit" in data.columns
        ):

            profit_data = (
                data.groupby("Category")
                .agg(
                    Sales=("Sales", "sum"),
                    Profit=("Profit", "sum")
                )
                .reset_index()
            )

            profit_data["Margin"] = 0.0

            valid_sales = (
                profit_data["Sales"] != 0
            )

            profit_data.loc[
                valid_sales,
                "Margin"
            ] = (
                profit_data.loc[
                    valid_sales,
                    "Profit"
                ]
                /
                profit_data.loc[
                    valid_sales,
                    "Sales"
                ]
                * 100
            )

            fig_profit = px.bar(
                profit_data.sort_values(
                    "Margin",
                    ascending=True
                ),
                x="Margin",
                y="Category",
                orientation="h",
                color="Margin",
                text="Margin",
                title="Profit Margin by Category"
            )

            fig_profit.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside"
            )

            fig_profit.update_layout(
                height=420,
                xaxis_title="Profit Margin (%)",
                yaxis_title=""
            )

            st.plotly_chart(
                fig_profit,
                use_container_width=True
            )

        else:

            st.info(
                "Profitability data unavailable."
            )

    st.divider()

    # ======================================================
    # TOP PRODUCTS
    # ======================================================

    st.subheader("🏆 Top Products by Revenue")

    if (
        "Product Name" in data.columns
        and "Sales" in data.columns
    ):

        top_products = (
            data.groupby("Product Name")
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum")
                if "Profit" in data.columns
                else ("Sales", "sum")
            )
            .reset_index()
            .sort_values(
                "Sales",
                ascending=False
            )
            .head(10)
        )

        top_products_plot = top_products.sort_values(
            "Sales",
            ascending=True
        )

        fig_products = px.bar(
            top_products_plot,
            x="Sales",
            y="Product Name",
            orientation="h",
            color="Profit",
            title="Top 10 Products by Revenue",
            text_auto=".2s"
        )

        fig_products.update_layout(
            height=520,
            xaxis_title="Revenue",
            yaxis_title="",
            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20
            )
        )

        st.plotly_chart(
            fig_products,
            use_container_width=True
        )

    else:

        st.info(
            "Product Name or Sales column is unavailable."
        )

    st.divider()

    # ======================================================
    # BUSINESS HEALTH
    # ======================================================

    st.subheader("❤️ Business Health")

    health_col1, health_col2, health_col3 = st.columns(3)

    # ======================================================
    # PROFIT HEALTH
    # ======================================================

    with health_col1:

        if profit_margin >= 20:

            st.success(
                "🟢 Strong Profitability"
            )

            st.caption(
                f"Current margin: {profit_margin:.2f}%"
            )

        elif profit_margin >= 10:

            st.info(
                "🔵 Healthy Profitability"
            )

            st.caption(
                f"Current margin: {profit_margin:.2f}%"
            )

        elif profit_margin >= 0:

            st.warning(
                "🟡 Profitability Requires Attention"
            )

            st.caption(
                f"Current margin: {profit_margin:.2f}%"
            )

        else:

            st.error(
                "🔴 Loss-Making Performance"
            )

            st.caption(
                f"Current margin: {profit_margin:.2f}%"
            )

    # ======================================================
    # GROWTH HEALTH
    # ======================================================

    with health_col2:

        if sales_growth > 10:

            st.success(
                "🟢 Strong Growth"
            )

        elif sales_growth > 0:

            st.info(
                "🔵 Positive Growth"
            )

        elif sales_growth < 0:

            st.warning(
                "🟡 Sales Declining"
            )

        else:

            st.info(
                "⚪ Growth Data Unavailable"
            )

        if previous_month_sales:

            st.caption(
                f"Month-over-month change: "
                f"{sales_growth:+.2f}%"
            )

    # ======================================================
    # SCALE HEALTH
    # ======================================================

    with health_col3:

        if total_orders > 0:

            st.success(
                "📊 Active Business Volume"
            )

            st.caption(
                f"{total_orders:,} unique orders"
            )

        else:

            st.warning(
                "⚠️ No order activity detected."
            )

    st.divider()

    # ======================================================
    # EXECUTIVE INSIGHTS
    # ======================================================

    st.subheader("🧠 Executive Insights")

    insights = []

    # ------------------------------------------------------
    # Revenue
    # ------------------------------------------------------

    insights.append(
        f"💰 The selected business dataset generated "
        f"**${total_sales:,.0f}** in revenue."
    )

    # ------------------------------------------------------
    # Profit
    # ------------------------------------------------------

    if total_profit >= 0:

        insights.append(
            f"📈 Total profit is **${total_profit:,.0f}**, "
            f"representing a **{profit_margin:.2f}%** "
            f"overall profit margin."
        )

    else:

        insights.append(
            f"⚠️ The business is currently operating at a "
            f"**${abs(total_profit):,.0f} loss**."
        )

    # ------------------------------------------------------
    # Region
    # ------------------------------------------------------

    if top_region != "N/A":

        insights.append(
            f"🌍 **{top_region}** is the strongest "
            f"revenue-generating region with "
            f"**${top_region_sales:,.0f}** in revenue."
        )

    # ------------------------------------------------------
    # Category
    # ------------------------------------------------------

    if top_category != "N/A":

        insights.append(
            f"📦 **{top_category}** is the leading category "
            f"with **${top_category_sales:,.0f}** in revenue."
        )

    # ------------------------------------------------------
    # Segment
    # ------------------------------------------------------

    if top_segment != "N/A":

        insights.append(
            f"👥 **{top_segment}** is the highest-revenue "
            f"customer segment."
        )

    # ------------------------------------------------------
    # Growth
    # ------------------------------------------------------

    if previous_month_sales:

        if sales_growth > 0:

            insights.append(
                f"🚀 Sales increased **{sales_growth:.2f}%** "
                f"compared with the previous month."
            )

        else:

            insights.append(
                f"📉 Sales declined **{abs(sales_growth):.2f}%** "
                f"compared with the previous month."
            )

    # ======================================================
    # DISPLAY INSIGHTS
    # ======================================================

    for insight in insights:

        st.info(insight)

    st.divider()

    # ======================================================
    # EXECUTIVE RECOMMENDATION
    # ======================================================

    st.subheader("🎯 Executive Recommendation")

    recommendations = []

    # ------------------------------------------------------
    # Profitability recommendation
    # ------------------------------------------------------

    if profit_margin >= 20:

        recommendations.append(
            "The business is demonstrating strong profitability. "
            "Management should prioritize scaling the strongest "
            "regions and categories while protecting existing margins."
        )

    elif profit_margin >= 10:

        recommendations.append(
            "Profitability is healthy but has room for improvement. "
            "Management should focus on product mix, pricing discipline "
            "and operational efficiency."
        )

    elif profit_margin >= 0:

        recommendations.append(
            "Revenue generation is positive, but profitability "
            "requires attention. Investigate low-margin products, "
            "discounting and operating costs."
        )

    else:

        recommendations.append(
            "The business is currently operating at a loss. "
            "Immediate attention should be given to pricing, "
            "product profitability, discounting and operating costs."
        )

    # ------------------------------------------------------
    # Growth recommendation
    # ------------------------------------------------------

    if previous_month_sales:

        if sales_growth < 0:

            recommendations.append(
                "Recent sales momentum is negative. Management should "
                "investigate declining categories, regions and products "
                "before increasing growth-related spending."
            )

        elif sales_growth > 10:

            recommendations.append(
                "Strong recent growth suggests an opportunity to scale "
                "high-performing products and regions while maintaining "
                "service and inventory capacity."
            )

    # ------------------------------------------------------
    # Display recommendation
    # ------------------------------------------------------

    for recommendation in recommendations:

        st.success(
            f"🎯 {recommendation}"
        )

    # ======================================================
    # MANAGEMENT SUMMARY
    # ======================================================

    st.divider()

    st.subheader("📋 Management Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:

        st.markdown(
            f"""
            **Business Overview**

            - Revenue: **${total_sales:,.0f}**
            - Profit: **${total_profit:,.0f}**
            - Profit Margin: **{profit_margin:.2f}%**
            - Orders: **{total_orders:,}**
            - Customers: **{total_customers:,}**
            - Average Order Value: **${average_order_value:,.0f}**
            """
        )

    with summary_col2:

        st.markdown(
            f"""
            **Performance Leaders**

            - Top Region: **{top_region}**
            - Top Category: **{top_category}**
            - Top Segment: **{top_segment}**
            - Top Product: **{top_product}**
            - Monthly Growth: **{
                f"{sales_growth:+.2f}%"
                if previous_month_sales
                else "N/A"
            }**
            - Business Health: **{health}**
            """
        )

    # ======================================================
    # FOOTNOTE
    # ======================================================

    st.caption(
        "InsightFlow AI • Executive Command Center • "
        "Metrics respond to the global filters selected in the sidebar."
    )