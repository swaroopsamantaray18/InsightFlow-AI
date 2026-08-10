# ==========================================================
# INSIGHTFLOW AI
# CUSTOMER ANALYTICS
# Version 2.0
# Developed by Swaroop K Samantaray
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.charts import (
    top_customers_chart,
    customer_segment_chart,
    orders_per_customer_chart,
    customer_value_chart,
)

from utils.customer_insights import customer_insights


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def show_customer_analytics(df):

    # ======================================================
    # EMPTY DATA PROTECTION
    # ======================================================

    if df is None or df.empty:

        st.warning(
            "⚠️ No customer data available for the selected filters."
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
                👥 &nbsp; CUSTOMER INTELLIGENCE
            </div>

            <h1>
                Customer <span>Analytics</span>
            </h1>

            <p>
                Understand customer behaviour, purchasing patterns,
                segment contribution, customer value and revenue
                concentration to support smarter customer strategies.
            </p>

        </section>
        """
    )

    st.divider()

    # ======================================================
    # DATA PREPARATION
    # ======================================================

    data = df.copy()

    # ------------------------------------------------------
    # Numeric columns
    # ------------------------------------------------------

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
    # BASIC CUSTOMER METRICS
    # ======================================================

    total_customers = (
        data["Customer ID"].nunique()
        if "Customer ID" in data.columns
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

    total_orders = (
        data["Order ID"].nunique()
        if "Order ID" in data.columns
        else 0
    )

    # ======================================================
    # AVERAGE ORDERS PER CUSTOMER
    # ======================================================

    avg_orders = (
        total_orders / total_customers
        if total_customers != 0
        else 0
    )

    # ======================================================
    # AVERAGE CUSTOMER VALUE
    # ======================================================

    avg_customer_value = (
        total_sales / total_customers
        if total_customers != 0
        else 0
    )

    # ======================================================
    # CUSTOMER PROFIT VALUE
    # ======================================================

    avg_customer_profit = (
        total_profit / total_customers
        if total_customers != 0
        else 0
    )

    # ======================================================
    # CUSTOMER MARGIN
    # ======================================================

    customer_margin = (
        (total_profit / total_sales) * 100
        if total_sales != 0
        else 0
    )

    # ======================================================
    # CUSTOMER SALES
    # ======================================================

    if (
        "Customer ID" in data.columns
        and "Sales" in data.columns
    ):

        customer_sales = (
            data.groupby("Customer ID")["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

    else:

        customer_sales = pd.Series(
            dtype=float
        )

    # ======================================================
    # CUSTOMER PROFIT
    # ======================================================

    if (
        "Customer ID" in data.columns
        and "Profit" in data.columns
    ):

        customer_profit = (
            data.groupby("Customer ID")["Profit"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

    else:

        customer_profit = pd.Series(
            dtype=float
        )

    # ======================================================
    # BEST CUSTOMER
    # ======================================================

    best_customer = "N/A"

    best_customer_sales = 0

    if (
        "Customer Name" in data.columns
        and "Sales" in data.columns
    ):

        customer_name_sales = (
            data.groupby("Customer Name")["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        if not customer_name_sales.empty:

            best_customer = str(
                customer_name_sales.index[0]
            )

            best_customer_sales = (
                customer_name_sales.iloc[0]
            )

    # ======================================================
    # CUSTOMER PERFORMANCE KPIs
    # ======================================================

    st.subheader("📊 Customer Performance")

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:

        st.metric(
            "👥 Customers",
            f"{total_customers:,}",
        )

    with k2:

        st.metric(
            "🛒 Avg Orders / Customer",
            f"{avg_orders:.2f}",
        )

    with k3:

        st.metric(
            "💰 Avg Customer Value",
            f"${avg_customer_value:,.0f}",
        )

    with k4:

        st.metric(
            "💵 Avg Customer Profit",
            f"${avg_customer_profit:,.0f}",
        )

    with k5:

        st.metric(
            "🎯 Customer Margin",
            f"{customer_margin:.2f}%",
        )

    # ======================================================
    # SECONDARY KPIs
    # ======================================================

    st.write("")

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.metric(
            "⭐ Best Customer",
            best_customer[:25],
        )

    with s2:

        st.metric(
            "💰 Best Customer Revenue",
            f"${best_customer_sales:,.0f}",
        )

    with s3:

        st.metric(
            "📦 Total Orders",
            f"{total_orders:,}",
        )

    with s4:

        st.metric(
            "💵 Total Revenue",
            f"${total_sales:,.0f}",
        )

    st.divider()

    # ======================================================
    # CUSTOMER RANKING
    # ======================================================

    st.subheader(
        "🏆 Customer Performance Ranking"
    )

    left, right = st.columns(2)

    # ======================================================
    # TOP CUSTOMERS
    # ======================================================

    with left:

        st.markdown(
            "#### 🏆 Top Customers by Revenue"
        )

        try:

            fig_top_customers = top_customers_chart(
                data
            )

            st.plotly_chart(
                fig_top_customers,
                use_container_width=True,
            )

        except Exception as error:

            st.warning(
                f"Unable to render top customer chart: {error}"
            )

    # ======================================================
    # CUSTOMER VALUE
    # ======================================================

    with right:

        st.markdown(
            "#### 💰 Customer Value Distribution"
        )

        try:

            fig_customer_value = customer_value_chart(
                data
            )

            st.plotly_chart(
                fig_customer_value,
                use_container_width=True,
            )

        except Exception as error:

            st.warning(
                f"Unable to render customer value chart: {error}"
            )

    st.divider()

    # ======================================================
    # CUSTOMER SEGMENTS
    # ======================================================

    st.subheader(
        "👥 Customer Segmentation"
    )

    left, right = st.columns(2)

    # ======================================================
    # SEGMENT CHART
    # ======================================================

    with left:

        st.markdown(
            "#### 👥 Revenue by Customer Segment"
        )

        if "Segment" in data.columns:

            try:

                fig_segment = customer_segment_chart(
                    data
                )

                st.plotly_chart(
                    fig_segment,
                    use_container_width=True,
                )

            except Exception as error:

                st.warning(
                    f"Unable to render segment chart: {error}"
                )

        else:

            st.info(
                "Segment data unavailable."
            )

    # ======================================================
    # ORDERS PER CUSTOMER
    # ======================================================

    with right:

        st.markdown(
            "#### 🛒 Orders per Customer"
        )

        try:

            fig_orders = orders_per_customer_chart(
                data
            )

            st.plotly_chart(
                fig_orders,
                use_container_width=True,
            )

        except Exception as error:

            st.warning(
                f"Unable to render orders-per-customer chart: {error}"
            )

    st.divider()

    # ======================================================
    # CUSTOMER REVENUE CONCENTRATION
    # ======================================================

    st.subheader(
        "🎯 Customer Revenue Concentration"
    )

    top_5_share = 0
    top_10_share = 0
    top_20_share = 0

    if not customer_sales.empty:

        total_customer_revenue = (
            customer_sales.sum()
        )

        top_5_customer_revenue = (
            customer_sales.head(5).sum()
        )

        top_10_customer_revenue = (
            customer_sales.head(10).sum()
        )

        top_20_customer_revenue = (
            customer_sales.head(20).sum()
        )

        top_5_share = (
            top_5_customer_revenue
            / total_customer_revenue
            * 100
            if total_customer_revenue != 0
            else 0
        )

        top_10_share = (
            top_10_customer_revenue
            / total_customer_revenue
            * 100
            if total_customer_revenue != 0
            else 0
        )

        top_20_share = (
            top_20_customer_revenue
            / total_customer_revenue
            * 100
            if total_customer_revenue != 0
            else 0
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "🏆 Top 5 Customer Share",
                f"{top_5_share:.1f}%",
            )

        with c2:

            st.metric(
                "📊 Top 10 Customer Share",
                f"{top_10_share:.1f}%",
            )

        with c3:

            st.metric(
                "📈 Top 20 Customer Share",
                f"{top_20_share:.1f}%",
            )

        # --------------------------------------------------
        # Concentration interpretation
        # --------------------------------------------------

        if top_10_share >= 50:

            st.warning(
                "⚠️ Revenue is highly concentrated among a small "
                "group of customers. Customer retention and "
                "concentration risk should be monitored."
            )

        elif top_10_share >= 30:

            st.info(
                "🟡 A meaningful portion of revenue comes from "
                "the top customers. Retention of these customers "
                "should remain a strategic priority."
            )

        else:

            st.success(
                "🟢 Customer revenue is relatively diversified "
                "across the customer base."
            )

    else:

        st.info(
            "Customer revenue data unavailable."
        )

    st.divider()

    # ======================================================
    # CUSTOMER SALES VS PROFIT
    # ======================================================

    st.subheader(
        "📊 Customer Revenue vs Profitability"
    )

    if (
        "Customer ID" in data.columns
        and "Sales" in data.columns
        and "Profit" in data.columns
    ):

        customer_matrix = (
            data.groupby("Customer ID")
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
            )
            .reset_index()
        )

        customer_matrix["Margin"] = (
            customer_matrix["Profit"]
            / customer_matrix["Sales"]
            * 100
        )

        customer_matrix["Margin"] = (
            customer_matrix["Margin"]
            .replace(
                [float("inf"), -float("inf")],
                0,
            )
            .fillna(0)
        )

        # --------------------------------------------------
        # Keep chart readable
        # --------------------------------------------------

        matrix_display = (
            customer_matrix.copy()
        )

        if len(matrix_display) > 300:

            matrix_display = (
                matrix_display
                .sort_values(
                    "Sales",
                    ascending=False,
                )
                .head(300)
            )

        fig_matrix = px.scatter(
            matrix_display,
            x="Sales",
            y="Profit",
            size="Sales",
            color="Margin",
            hover_name="Customer ID",
            hover_data={
                "Sales": ":,.0f",
                "Profit": ":,.0f",
                "Margin": ":.2f",
            },
            title=(
                "Customer Revenue vs Profitability"
            ),
        )

        fig_matrix.update_layout(
            height=520,
            xaxis_title="Customer Revenue",
            yaxis_title="Customer Profit",
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
            "Required Customer ID, Sales and Profit "
            "columns are unavailable."
        )

    st.divider()

    # ======================================================
    # CUSTOMER PERFORMANCE TABLE
    # ======================================================

    st.subheader(
        "📋 Customer Performance Table"
    )

    if (
        "Customer ID" in data.columns
        and "Sales" in data.columns
    ):

        aggregation = {
            "Sales": (
                "Sales",
                "sum",
            )
        }

        if "Order ID" in data.columns:

            aggregation["Orders"] = (
                "Order ID",
                "nunique",
            )

        else:

            aggregation["Orders"] = (
                "Customer ID",
                "count",
            )

        if "Profit" in data.columns:

            aggregation["Profit"] = (
                "Profit",
                "sum",
            )

        else:

            aggregation["Profit"] = (
                "Sales",
                "sum",
            )

        customer_table = (
            data.groupby("Customer ID")
            .agg(**aggregation)
            .reset_index()
        )

        customer_table["Customer Value"] = (
            customer_table["Sales"]
        )

        customer_table["Margin"] = (
            customer_table["Profit"]
            / customer_table["Sales"]
            * 100
        )

        customer_table["Margin"] = (
            customer_table["Margin"]
            .replace(
                [float("inf"), -float("inf")],
                0,
            )
            .fillna(0)
        )

        customer_table = (
            customer_table
            .sort_values(
                "Sales",
                ascending=False,
            )
        )

        st.dataframe(
            customer_table.style.format(
                {
                    "Sales": "${:,.0f}",
                    "Profit": "${:,.0f}",
                    "Customer Value": "${:,.0f}",
                    "Margin": "{:.2f}%",
                    "Orders": "{:,.0f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "Customer ID or Sales data unavailable."
        )

    st.divider()

    # ======================================================
    # CUSTOMER INSIGHTS
    # ======================================================

    st.subheader(
        "🧠 Customer Intelligence"
    )

    try:

        customer_insights(
            data
        )

    except Exception as error:

        st.warning(
            f"Unable to generate customer insights: {error}"
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
    # Customer value
    # ------------------------------------------------------

    if avg_customer_value > 0:

        takeaways.append(
            f"💰 The average customer contributes approximately "
            f"**${avg_customer_value:,.0f}** in revenue."
        )

    # ------------------------------------------------------
    # Order frequency
    # ------------------------------------------------------

    if avg_orders >= 3:

        takeaways.append(
            f"🟢 Customers place an average of "
            f"**{avg_orders:.2f} orders**, indicating strong "
            "purchase frequency."
        )

    elif avg_orders >= 2:

        takeaways.append(
            f"🔵 Customers place approximately "
            f"**{avg_orders:.2f} orders** on average, providing "
            "an opportunity to strengthen repeat purchasing."
        )

    else:

        takeaways.append(
            f"🟡 Average order frequency is only "
            f"**{avg_orders:.2f} orders per customer**. "
            "Retention, cross-selling and repeat-purchase "
            "strategies could improve customer value."
        )

    # ------------------------------------------------------
    # Customer concentration
    # ------------------------------------------------------

    if not customer_sales.empty:

        if top_10_share >= 50:

            takeaways.append(
                f"⚠️ The top 10 customers generate "
                f"**{top_10_share:.1f}%** of customer revenue. "
                "This indicates meaningful customer concentration risk."
            )

        elif top_10_share >= 30:

            takeaways.append(
                f"🟡 The top 10 customers contribute "
                f"**{top_10_share:.1f}%** of revenue. "
                "High-value customer retention should remain a priority."
            )

        else:

            takeaways.append(
                f"🟢 The top 10 customers contribute "
                f"approximately **{top_10_share:.1f}%** of revenue, "
                "suggesting relatively diversified customer revenue."
            )

    # ------------------------------------------------------
    # Best customer
    # ------------------------------------------------------

    if best_customer != "N/A":

        takeaways.append(
            f"⭐ **{best_customer}** is the highest-value customer "
            f"with approximately **${best_customer_sales:,.0f}** "
            "in revenue."
        )

    # ------------------------------------------------------
    # Customer margin
    # ------------------------------------------------------

    if customer_margin >= 20:

        takeaways.append(
            "🟢 Customer-level profitability is strong."
        )

    elif customer_margin >= 10:

        takeaways.append(
            "🔵 Customer-level profitability is healthy, "
            "with opportunities to improve value from lower-margin customers."
        )

    elif customer_margin >= 0:

        takeaways.append(
            "🟡 Customer profitability is relatively low. "
            "Review discounting, service costs and customer mix."
        )

    else:

        takeaways.append(
            "🔴 The customer portfolio is currently generating "
            "negative profitability and requires immediate investigation."
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
        "InsightFlow AI • Customer Analytics • "
        "All metrics and visualizations respond to the "
        "global filters selected in the sidebar."
    )