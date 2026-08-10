# ==========================================================
# INSIGHTFLOW AI
# SALES FORECAST
# Version 2.0
# Developed by Swaroop K Samantaray
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.forecasting import sales_forecast


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def show_forecast_analytics(df):

    # ======================================================
    # EMPTY DATA PROTECTION
    # ======================================================

    if df is None or df.empty:

        st.warning(
            "⚠️ No data available for the selected filters."
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

        </style>

        <section class="if-page-header">

            <div class="if-page-badge">
                🔮 &nbsp; PREDICTIVE BUSINESS INTELLIGENCE
            </div>

            <h1>
                Sales <span>Forecast</span>
            </h1>

            <p>
                Predict future business performance using historical sales
                patterns, machine learning and predictive analytics to support
                proactive business planning and decision-making.
            </p>

        </section>
        """
    )

    # ======================================================
    # FORECAST SETTINGS
    # ======================================================

    st.subheader("⚙️ Forecast Settings")

    settings_col1, settings_col2 = st.columns([1, 3])

    with settings_col1:

        periods = st.selectbox(
            "Forecast Horizon",
            [3, 6, 12],
            index=1
        )

    with settings_col2:

        st.info(
            f"🔮 The model will forecast the next "
            f"**{periods} months** using historical monthly sales."
        )

    st.divider()

    # ======================================================
    # FORECAST GENERATION
    # ======================================================

    try:

        historical, forecast, accuracy = sales_forecast(
            df,
            periods
        )

    except Exception as e:

        st.error(
            f"❌ Unable to generate the sales forecast.\n\n"
            f"Error: {e}"
        )

        return

    # ======================================================
    # EMPTY FORECAST PROTECTION
    # ======================================================

    if (
        historical is None
        or forecast is None
        or historical.empty
        or forecast.empty
    ):

        st.warning(
            "⚠️ Not enough historical data is available to generate "
            "a forecast."
        )

        return

    # ======================================================
    # DATA PREPARATION
    # ======================================================

    historical = historical.copy()
    forecast = forecast.copy()

    if "Order Date" in historical.columns:

        historical["Order Date"] = pd.to_datetime(
            historical["Order Date"],
            errors="coerce"
        )

    if "Order Date" in forecast.columns:

        forecast["Order Date"] = pd.to_datetime(
            forecast["Order Date"],
            errors="coerce"
        )

    # ======================================================
    # CORE FORECAST METRICS
    # ======================================================

    next_month_sales = float(
        forecast.iloc[0]["Forecast Sales"]
    )

    last_month_sales = float(
        historical.iloc[-1]["Sales"]
    )

    if last_month_sales != 0:

        growth = (
            (next_month_sales - last_month_sales)
            / last_month_sales
        ) * 100

    else:

        growth = 0

    # ======================================================
    # FORECAST CONFIDENCE
    # ======================================================

    if accuracy >= 0.85:

        confidence = "High"

    elif accuracy >= 0.65:

        confidence = "Moderate"

    else:

        confidence = "Low"

    # ======================================================
    # FORECAST TREND
    # ======================================================

    if growth > 0:

        trend = "Increasing"
        trend_icon = "📈"

    elif growth < 0:

        trend = "Decreasing"
        trend_icon = "📉"

    else:

        trend = "Stable"
        trend_icon = "➡️"

    # ======================================================
    # FORECAST KPIs
    # ======================================================

    st.subheader("📊 Forecast Performance")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📅 Next Month Forecast",
            f"${next_month_sales:,.0f}"
        )

    with col2:

        st.metric(
            "📈 Expected Growth",
            f"{growth:+.2f}%"
        )

    with col3:

        st.metric(
            "🎯 R² Score",
            f"{accuracy:.2f}"
        )

    with col4:

        st.metric(
            "🤖 Forecast Confidence",
            confidence
        )

    st.divider()

    # ======================================================
    # FORECAST CHART
    # ======================================================

    st.subheader("📈 Historical vs Forecast Sales")

    fig = go.Figure()

    # ------------------------------------------------------
    # Historical Sales
    # ------------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=historical["Order Date"],
            y=historical["Sales"],
            mode="lines+markers",
            name="Historical Sales",

            line=dict(
                width=3
            ),

            marker=dict(
                size=7
            )
        )
    )

    # ------------------------------------------------------
    # Forecast
    # ------------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=forecast["Order Date"],
            y=forecast["Forecast Sales"],
            mode="lines+markers",
            name="Forecast",

            line=dict(
                dash="dash",
                width=4
            ),

            marker=dict(
                size=8
            )
        )
    )

    fig.update_layout(

        height=600,

        template="plotly_dark",

        xaxis_title="Month",

        yaxis_title="Sales",

        hovermode="x unified",

        legend_title="Series",

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

    st.divider()

    # ======================================================
    # FORECAST VALUES
    # ======================================================

    st.subheader("📊 Forecast Values")

    table = forecast.copy()

    if "Forecast Sales" in table.columns:

        table["Forecast Sales"] = table[
            "Forecast Sales"
        ].map(
            lambda x: f"${x:,.0f}"
        )

    if "Order Date" in table.columns:

        table["Order Date"] = pd.to_datetime(
            table["Order Date"],
            errors="coerce"
        ).dt.strftime("%b %Y")

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ======================================================
    # FORECAST SUMMARY
    # ======================================================

    st.subheader("🔍 Forecast Summary")

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    # ------------------------------------------------------
    # Trend
    # ------------------------------------------------------

    with summary_col1:

        st.markdown(
            f"""
            ### {trend_icon} Sales Trend

            **{trend}**

            The model expects sales to be
            **{growth:+.2f}%** relative to the latest
            historical month.
            """
        )

    # ------------------------------------------------------
    # Confidence
    # ------------------------------------------------------

    with summary_col2:

        st.markdown(
            f"""
            ### 🎯 Model Confidence

            **{confidence}**

            The forecasting model achieved an
            **R² score of {accuracy:.2f}**.
            """
        )

    # ------------------------------------------------------
    # Horizon
    # ------------------------------------------------------

    with summary_col3:

        st.markdown(
            f"""
            ### 📅 Planning Horizon

            **{periods} Months**

            Use the forecast to support inventory,
            pricing and operational planning.
            """
        )

    st.divider()

    # ======================================================
    # AI FORECAST COMMENTARY
    # ======================================================

    st.subheader("🤖 Forecast Commentary")

    if growth > 10:

        recommendation = (
            "The forecast indicates strong positive momentum. "
            "Management should evaluate inventory capacity, "
            "operational readiness and opportunities to scale "
            "high-performing products and regions."
        )

    elif growth > 0:

        recommendation = (
            "The forecast indicates moderate positive growth. "
            "The business should maintain current momentum while "
            "monitoring demand, inventory and customer behavior."
        )

    elif growth < -10:

        recommendation = (
            "The forecast indicates a significant decline in sales. "
            "Management should investigate declining products, "
            "regions, pricing strategy and customer demand before "
            "committing additional growth-related spending."
        )

    elif growth < 0:

        recommendation = (
            "The forecast indicates a moderate decline in sales. "
            "Management should closely monitor sales momentum and "
            "identify the categories, products or regions contributing "
            "to the decline."
        )

    else:

        recommendation = (
            "The forecast indicates relatively stable sales. "
            "Management should focus on maintaining profitability "
            "while identifying opportunities for incremental growth."
        )

    st.info(
        f"""
        ### 🔮 Forecast Trend

        The model predicts an **{trend.lower()}** sales trend
        over the next **{periods} months**.

        ---

        ### 📌 Key Insights

        - 📅 Next Month Forecast: **${next_month_sales:,.0f}**
        - 📈 Expected Growth: **{growth:+.2f}%**
        - 🎯 Model R² Score: **{accuracy:.2f}**
        - 🤖 Forecast Confidence: **{confidence}**
        - 📊 Forecast Horizon: **{periods} months**

        ---

        ### 🎯 Business Recommendation

        {recommendation}
        """
    )

    st.divider()

    # ======================================================
    # FORECAST ACTION PLAN
    # ======================================================

    st.subheader("🎯 Recommended Action Plan")

    action_col1, action_col2 = st.columns(2)

    with action_col1:

        st.markdown(
            """
            **📦 Demand & Inventory**

            - Monitor upcoming demand closely.
            - Adjust inventory according to forecasted demand.
            - Protect availability of high-performing products.
            - Avoid excessive inventory where demand is weakening.
            """
        )

    with action_col2:

        st.markdown(
            """
            **💼 Business Strategy**

            - Review pricing strategy when demand changes.
            - Focus resources on high-performing products.
            - Monitor regional performance.
            - Re-train the forecasting model as new data arrives.
            """
        )

    st.divider()

    # ======================================================
    # FORECAST FOOTNOTE
    # ======================================================

    st.caption(
        "InsightFlow AI • Sales Forecast • "
        "Forecast results respond to the global filters selected "
        "in the sidebar."
    )