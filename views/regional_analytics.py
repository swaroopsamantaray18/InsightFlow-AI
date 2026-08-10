# ==========================================================
# INSIGHTFLOW AI
# REGIONAL ANALYTICS
# Version 2.0
# Developed by Swaroop K Samantaray
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.charts import (
    region_revenue_chart,
    region_profit_chart,
    state_sales_chart,
    region_margin_chart,
    state_map_chart,
)

from utils.regional_insights import regional_insights


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def show_regional_analytics(df):

    # ======================================================
    # EMPTY DATA PROTECTION
    # ======================================================

    if df is None or df.empty:

        st.warning(
            "⚠️ No regional data available for the selected filters."
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
            background: radial-gradient(circle at 88% 18%, rgba(90, 110, 240, 0.20), transparent 42%), linear-gradient(135deg, #172640 0%, #101a2c 55%, #1b214b 100%);
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
            .if-page-header { padding: 30px 26px; }
            .if-page-header h1 { font-size: 40px; letter-spacing: -1.5px; }
        }

        </style>

        <section class="if-page-header">
            <div class="if-page-badge">
                🌍 &nbsp; GEOGRAPHIC BUSINESS INTELLIGENCE
            </div>
            <h1>
                Regional <span>Analytics</span>
            </h1>
            <p>
                Analyze regional performance, state-level sales,
                profitability, margins and geographic business
                opportunities across your market.
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

    total_regions = (
        data["Region"].nunique()
        if "Region" in data.columns
        else 0
    )

    total_states = (
        data["State/Province"].nunique()
        if "State/Province" in data.columns
        else 0
    )

    overall_margin = (
        (total_profit / total_sales) * 100
        if total_sales != 0
        else 0
    )

    # ======================================================
    # REGIONAL SALES
    # ======================================================

    if (
        "Region" in data.columns
        and "Sales" in data.columns
    ):

        region_sales = (
            data.groupby("Region")["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

    else:

        region_sales = pd.Series(dtype=float)

    # ======================================================
    # REGIONAL PROFIT
    # ======================================================

    if (
        "Region" in data.columns
        and "Profit" in data.columns
    ):

        region_profit = (
            data.groupby("Region")["Profit"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

    else:

        region_profit = pd.Series(dtype=float)

    # ======================================================
    # REGIONAL MARGIN
    # ======================================================

    if (
        "Region" in data.columns
        and "Sales" in data.columns
        and "Profit" in data.columns
    ):

        regional_summary = (
            data.groupby("Region")
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
            )
            .reset_index()
        )

        regional_summary["Margin"] = (
            regional_summary["Profit"]
            / regional_summary["Sales"]
            * 100
        )

        regional_summary["Margin"] = (
            regional_summary["Margin"]
            .replace(
                [float("inf"), -float("inf")],
                0,
            )
            .fillna(0)
        )

    else:

        regional_summary = pd.DataFrame()

    # ======================================================
    # TOP REGION
    # ======================================================

    if not region_sales.empty:

        top_region = str(
            region_sales.index[0]
        )

        top_region_sales = (
            region_sales.iloc[0]
        )

    else:

        top_region = "N/A"

        top_region_sales = 0

    # ======================================================
    # LOWEST REGION
    # ======================================================

    if not region_sales.empty:

        weakest_region = str(
            region_sales.index[-1]
        )

        weakest_region_sales = (
            region_sales.iloc[-1]
        )

    else:

        weakest_region = "N/A"

        weakest_region_sales = 0

    # ======================================================
    # HIGHEST PROFIT REGION
    # ======================================================

    if not region_profit.empty:

        highest_profit_region = str(
            region_profit.index[0]
        )

        highest_profit_value = (
            region_profit.iloc[0]
        )

    else:

        highest_profit_region = "N/A"

        highest_profit_value = 0

    # ======================================================
    # LOWEST PROFIT REGION
    # ======================================================

    if not region_profit.empty:

        lowest_profit_region = str(
            region_profit.index[-1]
        )

        lowest_profit_value = (
            region_profit.iloc[-1]
        )

    else:

        lowest_profit_region = "N/A"

        lowest_profit_value = 0

    # ======================================================
    # TOP STATE
    # ======================================================

    if (
        "State/Province" in data.columns
        and "Sales" in data.columns
    ):

        state_sales = (
            data.groupby("State/Province")["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

    else:

        state_sales = pd.Series(dtype=float)

    if not state_sales.empty:

        top_state = str(
            state_sales.index[0]
        )

        top_state_sales = (
            state_sales.iloc[0]
        )

    else:

        top_state = "N/A"

        top_state_sales = 0

    # ======================================================
    # REGIONAL KPI SECTION
    # ======================================================

    st.subheader("📊 Geographic Performance")

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:

        st.metric(
            "🌍 Regions",
            f"{total_regions:,}",
        )

    with k2:

        st.metric(
            "📍 States",
            f"{total_states:,}",
        )

    with k3:

        st.metric(
            "💰 Revenue",
            f"${total_sales:,.0f}",
        )

    with k4:

        st.metric(
            "📈 Profit",
            f"${total_profit:,.0f}",
        )

    with k5:

        st.metric(
            "🎯 Overall Margin",
            f"{overall_margin:.2f}%",
        )

    # ======================================================
    # SECONDARY KPIs
    # ======================================================

    st.write("")

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.metric(
            "🏆 Top Region",
            top_region,
        )

        st.caption(
            f"${top_region_sales:,.0f} revenue"
        )

    with s2:

        st.metric(
            "📍 Top State",
            top_state,
        )

        st.caption(
            f"${top_state_sales:,.0f} revenue"
        )

    with s3:

        st.metric(
            "💹 Highest Profit Region",
            highest_profit_region,
        )

        st.caption(
            f"${highest_profit_value:,.0f} profit"
        )

    with s4:

        st.metric(
            "📉 Weakest Region",
            weakest_region,
        )

        st.caption(
            f"${weakest_region_sales:,.0f} revenue"
        )

    st.divider()

    # ======================================================
    # REGIONAL REVENUE + PROFIT
    # ======================================================

    st.subheader("🌍 Regional Revenue & Profitability")

    left, right = st.columns(2)

    # ======================================================
    # REGIONAL REVENUE
    # ======================================================

    with left:

        st.markdown(
            "#### 💰 Revenue by Region"
        )

        if "Region" in data.columns:

            try:

                fig_revenue = region_revenue_chart(
                    data
                )

                st.plotly_chart(
                    fig_revenue,
                    use_container_width=True,
                )

            except Exception as error:

                st.warning(
                    f"Unable to render regional revenue chart: {error}"
                )

        else:

            st.info(
                "Region data unavailable."
            )

    # ======================================================
    # REGIONAL PROFIT
    # ======================================================

    with right:

        st.markdown(
            "#### 📈 Profit by Region"
        )

        if "Region" in data.columns:

            try:

                fig_profit = region_profit_chart(
                    data
                )

                st.plotly_chart(
                    fig_profit,
                    use_container_width=True,
                )

            except Exception as error:

                st.warning(
                    f"Unable to render regional profit chart: {error}"
                )

        else:

            st.info(
                "Region data unavailable."
            )

    st.divider()

    # ======================================================
    # STATE PERFORMANCE + REGIONAL MARGIN
    # ======================================================

    st.subheader("📍 State & Margin Analysis")

    left, right = st.columns(2)

    # ======================================================
    # STATE SALES
    # ======================================================

    with left:

        st.markdown(
            "#### 📍 State-Level Sales"
        )

        if "State/Province" in data.columns:

            try:

                fig_state = state_sales_chart(
                    data
                )

                st.plotly_chart(
                    fig_state,
                    use_container_width=True,
                )

            except Exception as error:

                st.warning(
                    f"Unable to render state sales chart: {error}"
                )

        else:

            st.info(
                "State/Province data unavailable."
            )

    # ======================================================
    # REGIONAL MARGIN
    # ======================================================

    with right:

        st.markdown(
            "#### 🎯 Regional Profit Margin"
        )

        if not regional_summary.empty:

            try:

                fig_margin = region_margin_chart(
                    data
                )

                st.plotly_chart(
                    fig_margin,
                    use_container_width=True,
                )

            except Exception as error:

                st.warning(
                    f"Unable to render regional margin chart: {error}"
                )

        else:

            st.info(
                "Regional profitability data unavailable."
            )

    st.divider()

    # ======================================================
    # GEOGRAPHIC MAP
    # ======================================================

    st.subheader("🗺️ Geographic Sales Distribution")

    st.markdown(
        """
        Explore how revenue is distributed geographically
        across the available states and provinces.
        """
    )

    if "State/Province" in data.columns:

        try:

            fig_map = state_map_chart(
                data
            )

            st.plotly_chart(
                fig_map,
                use_container_width=True,
            )

        except Exception as error:

            st.warning(
                f"Unable to render geographic map: {error}"
            )

    else:

        st.info(
            "State/Province information is unavailable."
        )

    st.divider()

    # ======================================================
    # REGIONAL PERFORMANCE TABLE
    # ======================================================

    st.subheader("📋 Regional Performance Table")

    if not regional_summary.empty:

        regional_table = (
            regional_summary
            .sort_values(
                "Sales",
                ascending=False,
            )
            .copy()
        )

        regional_table["Revenue Share"] = (
            regional_table["Sales"]
            / regional_table["Sales"].sum()
            * 100
        )

        st.dataframe(
            regional_table.style.format(
                {
                    "Sales": "${:,.0f}",
                    "Profit": "${:,.0f}",
                    "Margin": "{:.2f}%",
                    "Revenue Share": "{:.2f}%",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "Regional performance data unavailable."
        )

    st.divider()

    # ======================================================
    # STATE PERFORMANCE TABLE
    # ======================================================

    st.subheader("📍 Top States by Revenue")

    if not state_sales.empty:

        state_table = (
            state_sales
            .reset_index()
            .rename(
                columns={
                    "Sales": "Revenue"
                }
            )
            .head(15)
        )

        state_table["Revenue Share"] = (
            state_table["Revenue"]
            / state_sales.sum()
            * 100
        )

        st.dataframe(
            state_table.style.format(
                {
                    "Revenue": "${:,.0f}",
                    "Revenue Share": "{:.2f}%",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "State-level sales data unavailable."
        )

    st.divider()

    # ======================================================
    # REGIONAL CONCENTRATION
    # ======================================================

    st.subheader("🎯 Regional Revenue Concentration")

    if not region_sales.empty:

        total_regional_revenue = (
            region_sales.sum()
        )

        top_region_revenue = (
            region_sales.head(1).sum()
        )

        top_two_revenue = (
            region_sales.head(2).sum()
        )

        top_region_share = (
            top_region_revenue
            / total_regional_revenue
            * 100
            if total_regional_revenue != 0
            else 0
        )

        top_two_share = (
            top_two_revenue
            / total_regional_revenue
            * 100
            if total_regional_revenue != 0
            else 0
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "🏆 Top Region Share",
                f"{top_region_share:.1f}%",
            )

        with c2:

            st.metric(
                "🌍 Top 2 Regions Share",
                f"{top_two_share:.1f}%",
            )

        with c3:

            st.metric(
                "📊 Total Regions",
                f"{total_regions:,}",
            )

        if top_region_share >= 50:

            st.warning(
                "⚠️ Revenue is highly concentrated in the "
                "leading region. Geographic diversification "
                "may reduce concentration risk."
            )

        elif top_region_share >= 35:

            st.info(
                "🟡 The leading region contributes a significant "
                f"{top_region_share:.1f}% of total revenue."
            )

        else:

            st.success(
                "🟢 Revenue is relatively diversified across "
                "the regional footprint."
            )

    st.divider()

    # ======================================================
    # REGIONAL INSIGHTS
    # ======================================================

    st.subheader("🧠 Regional Intelligence")

    try:

        regional_insights(data)

    except Exception as error:

        st.warning(
            f"Unable to generate regional insights: {error}"
        )

    st.divider()

    # ======================================================
    # MANAGEMENT TAKEAWAYS
    # ======================================================

    st.subheader("🎯 Management Takeaways")

    takeaways = []

    # ------------------------------------------------------
    # Top region
    # ------------------------------------------------------

    if top_region != "N/A":

        takeaways.append(
            f"🏆 **{top_region}** is the leading region with "
            f"approximately **${top_region_sales:,.0f}** in revenue."
        )

    # ------------------------------------------------------
    # Weakest region
    # ------------------------------------------------------

    if weakest_region != "N/A":

        takeaways.append(
            f"📉 **{weakest_region}** is currently the lowest "
            f"revenue-generating region at approximately "
            f"**${weakest_region_sales:,.0f}**."
        )

    # ------------------------------------------------------
    # Profit leader
    # ------------------------------------------------------

    if highest_profit_region != "N/A":

        takeaways.append(
            f"💰 **{highest_profit_region}** generates the highest "
            f"regional profit at approximately "
            f"**${highest_profit_value:,.0f}**."
        )

    # ------------------------------------------------------
    # Lowest profit
    # ------------------------------------------------------

    if lowest_profit_region != "N/A":

        if lowest_profit_value < 0:

            takeaways.append(
                f"🔴 **{lowest_profit_region}** is generating a "
                f"regional loss of approximately "
                f"**${abs(lowest_profit_value):,.0f}** and "
                "requires profitability investigation."
            )

        else:

            takeaways.append(
                f"🟡 **{lowest_profit_region}** has the lowest "
                f"regional profit at approximately "
                f"**${lowest_profit_value:,.0f}**."
            )

    # ------------------------------------------------------
    # Top state
    # ------------------------------------------------------

    if top_state != "N/A":

        takeaways.append(
            f"📍 **{top_state}** is the highest-performing state "
            f"with approximately **${top_state_sales:,.0f}** in revenue."
        )

    # ------------------------------------------------------
    # Margin
    # ------------------------------------------------------

    if overall_margin >= 20:

        takeaways.append(
            "🟢 Overall geographic profitability is strong."
        )

    elif overall_margin >= 10:

        takeaways.append(
            "🔵 Overall regional profitability is healthy, "
            "although individual regions should be compared for "
            "margin optimization."
        )

    elif overall_margin >= 0:

        takeaways.append(
            "🟡 Overall margins are relatively low. "
            "Regional cost and pricing differences should be investigated."
        )

    else:

        takeaways.append(
            "🔴 Overall regional profitability is negative. "
            "Management should investigate loss-making markets."
        )

    # ======================================================
    # DISPLAY TAKEAWAYS
    # ======================================================

    for takeaway in takeaways:

        st.info(takeaway)

    # ======================================================
    # FOOTER
    # ======================================================

    st.caption(
        "InsightFlow AI • Regional Analytics • "
        "All metrics and visualizations respond to the "
        "global filters selected in the sidebar."
    )