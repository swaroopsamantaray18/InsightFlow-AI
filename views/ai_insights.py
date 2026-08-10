# ==========================================================
# INSIGHTFLOW AI
# AI BUSINESS INTELLIGENCE
# Version 2.0
# Developed by Swaroop K Samantaray
# ==========================================================

import os

import streamlit as st
import pandas as pd

from utils.ai_engine import (
    business_health_score,
    generate_recommendations,
    business_risks,
)

from utils.ai_copilot import ask_business_ai
from utils.gemini_ai import ask_gemini
from utils.pdf_report import generate_pdf


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def show_ai_insights(df):

    # ======================================================
    # EMPTY DATA PROTECTION
    # ======================================================

    if df is None or df.empty:

        st.warning(
            "⚠️ No business data available for AI analysis "
            "under the selected filters."
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
                🤖 &nbsp; ARTIFICIAL INTELLIGENCE BUSINESS CENTER
            </div>

            <h1>
                AI Business <span>Insights</span>
            </h1>

            <p>
                Transform business data into strategic decisions
                using business intelligence, risk analysis,
                AI recommendations and an interactive business copilot.
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

    margin = (
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
    # BUSINESS HEALTH SCORE
    # ======================================================

    try:

        score = business_health_score(data)

    except Exception:

        score = 0

    # ------------------------------------------------------
    # Ensure score remains within valid range
    # ------------------------------------------------------

    try:

        score = float(score)

    except Exception:

        score = 0

    score = max(
        0,
        min(
            100,
            score,
        ),
    )

    # ======================================================
    # BUSINESS STATUS
    # ======================================================

    if score >= 85:

        status = "🟢 Excellent"

        status_text = "Excellent"

    elif score >= 70:

        status = "🟡 Good"

        status_text = "Good"

    elif score >= 50:

        status = "🟠 Moderate"

        status_text = "Moderate"

    else:

        status = "🔴 Needs Improvement"

        status_text = "Needs Improvement"

    # ======================================================
    # AI RECOMMENDATIONS
    # ======================================================

    try:

        recommendations = generate_recommendations(
            data
        )

    except Exception as error:

        recommendations = [
            f"Unable to generate recommendations: {error}"
        ]

    if recommendations is None:

        recommendations = []

    # ======================================================
    # BUSINESS RISKS
    # ======================================================

    try:

        risks = business_risks(
            data
        )

    except Exception as error:

        risks = [
            f"Unable to identify business risks: {error}"
        ]

    if risks is None:

        risks = []

    # ======================================================
    # TOP BUSINESS DIMENSIONS
    # ======================================================

    # ------------------------------------------------------
    # Top Region
    # ------------------------------------------------------

    top_region = "N/A"

    top_region_sales = 0

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

        if not region_sales.empty:

            top_region = str(
                region_sales.index[0]
            )

            top_region_sales = (
                region_sales.iloc[0]
            )

    # ------------------------------------------------------
    # Top Category
    # ------------------------------------------------------

    top_category = "N/A"

    top_category_sales = 0

    if (
        "Category" in data.columns
        and "Sales" in data.columns
    ):

        category_sales = (
            data.groupby("Category")["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        if not category_sales.empty:

            top_category = str(
                category_sales.index[0]
            )

            top_category_sales = (
                category_sales.iloc[0]
            )

    # ------------------------------------------------------
    # Top Product
    # ------------------------------------------------------

    top_product = "N/A"

    top_product_sales = 0

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

        if not product_sales.empty:

            top_product = str(
                product_sales.index[0]
            )

            top_product_sales = (
                product_sales.iloc[0]
            )

    # ------------------------------------------------------
    # Top Segment
    # ------------------------------------------------------

    top_segment = "N/A"

    top_segment_sales = 0

    if (
        "Segment" in data.columns
        and "Sales" in data.columns
    ):

        segment_sales = (
            data.groupby("Segment")["Sales"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        if not segment_sales.empty:

            top_segment = str(
                segment_sales.index[0]
            )

            top_segment_sales = (
                segment_sales.iloc[0]
            )

    # ======================================================
    # AI OVERVIEW
    # ======================================================

    st.subheader("🧠 AI Business Overview")

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:

        st.metric(
            "🤖 Health Score",
            f"{score:.0f}/100",
        )

    with k2:

        st.metric(
            "💰 Revenue",
            f"${total_sales:,.0f}",
        )

    with k3:

        st.metric(
            "📈 Profit",
            f"${total_profit:,.0f}",
        )

    with k4:

        st.metric(
            "🎯 Margin",
            f"{margin:.2f}%",
        )

    with k5:

        st.metric(
            "❤️ Status",
            status,
        )

    # ======================================================
    # HEALTH PROGRESS
    # ======================================================

    st.progress(
        score / 100
    )

    st.caption(
        f"Current business health classification: "
        f"**{status_text}**"
    )

    st.divider()

    # ======================================================
    # BUSINESS SNAPSHOT
    # ======================================================

    st.subheader("📊 Business Snapshot")

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.metric(
            "🌍 Leading Region",
            top_region,
        )

        st.caption(
            f"${top_region_sales:,.0f} revenue"
        )

    with s2:

        st.metric(
            "📦 Leading Category",
            top_category,
        )

        st.caption(
            f"${top_category_sales:,.0f} revenue"
        )

    with s3:

        st.metric(
            "🏆 Leading Product",
            top_product[:25],
        )

        st.caption(
            f"${top_product_sales:,.0f} revenue"
        )

    with s4:

        st.metric(
            "👥 Leading Segment",
            top_segment,
        )

        st.caption(
            f"${top_segment_sales:,.0f} revenue"
        )

    st.divider()

    # ======================================================
    # EXECUTIVE AI SUMMARY
    # ======================================================

    st.subheader("📈 Executive AI Summary")

    summary_text = f"""
### Executive Summary

**Business Health:** {status_text}  
**Health Score:** {score:.0f}/100

---

💰 **Total Revenue**

**${total_sales:,.0f}**

---

📈 **Total Profit**

**${total_profit:,.0f}**

---

🎯 **Profit Margin**

**{margin:.2f}%**

---

🧾 **Average Order Value**

**${average_order_value:,.0f}**

---

🌍 **Strongest Region**

**{top_region}**

---

📦 **Highest Revenue Category**

**{top_category}**

---

🏆 **Highest Revenue Product**

**{top_product}**

---

👥 **Best Customer Segment**

**{top_segment}**

---

### AI Interpretation

The business currently demonstrates **{status_text}**
overall performance based on the calculated business health
score.

Strategic attention should focus on maintaining the strongest
performing regions, categories and customer segments while
addressing identified business risks and improving weaker
areas of the portfolio.
"""

    st.info(
        summary_text
    )

    st.divider()

    # ======================================================
    # AI STRATEGIC RECOMMENDATIONS
    # ======================================================

    st.subheader("🚀 AI Strategic Recommendations")

    if recommendations:

        for index, recommendation in enumerate(
            recommendations,
            start=1,
        ):

            st.success(
                f"**{index}.** {recommendation}"
            )

    else:

        st.info(
            "No strategic recommendations were generated."
        )

    st.divider()

    # ======================================================
    # BUSINESS RISKS
    # ======================================================

    st.subheader("⚠️ Business Risk Monitor")

    if risks:

        for risk in risks:

            st.warning(
                risk
            )

    else:

        st.success(
            "🟢 No major business risks were detected "
            "by the current rules engine."
        )

    st.divider()

    # ======================================================
    # AI DECISION CENTER
    # ======================================================

    st.subheader("🎯 AI Decision Center")

    decision1, decision2, decision3 = st.columns(3)

    # ------------------------------------------------------
    # Growth
    # ------------------------------------------------------

    with decision1:

        st.markdown(
            "#### 🚀 Growth Opportunity"
        )

        if top_category != "N/A":

            st.success(
                f"Prioritize **{top_category}** and "
                f"**{top_region}** based on current revenue leadership."
            )

        else:

            st.info(
                "Insufficient data to determine the strongest "
                "growth area."
            )

    # ------------------------------------------------------
    # Profitability
    # ------------------------------------------------------

    with decision2:

        st.markdown(
            "#### 💹 Profitability Focus"
        )

        if margin >= 20:

            st.success(
                "Profitability is strong. Focus on scaling "
                "high-performing business areas."
            )

        elif margin >= 10:

            st.info(
                "Profitability is healthy. Optimize product "
                "mix and pricing to improve margins."
            )

        elif margin >= 0:

            st.warning(
                "Margins require attention. Review discounting, "
                "pricing and low-profit products."
            )

        else:

            st.error(
                "The business is operating at a loss. "
                "Immediate profitability analysis is required."
            )

    # ------------------------------------------------------
    # Risk
    # ------------------------------------------------------

    with decision3:

        st.markdown(
            "#### ⚠️ Risk Focus"
        )

        if len(risks) == 0:

            st.success(
                "No major risks detected."
            )

        elif len(risks) <= 2:

            st.warning(
                "A small number of business risks "
                "require management attention."
            )

        else:

            st.error(
                f"{len(risks)} business risks require "
                "management attention."
            )

    st.divider()

    # ======================================================
    # AI BUSINESS COPILOT
    # ======================================================

    st.subheader("🤖 AI Business Copilot")

    st.markdown(
        """
        Ask questions about the currently selected business
        data and receive answers from the available AI engine.
        """
    )

    # ======================================================
    # AI MODE
    # ======================================================

    ai_mode = st.radio(
        "Choose AI Engine",
        [
            "Business Rules",
            "Gemini AI",
        ],
        horizontal=True,
        key="ai_engine_mode",
    )

    # ======================================================
    # SESSION STATE
    # ======================================================

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    # ======================================================
    # QUESTION INPUT
    # ======================================================

    question = st.text_input(
        "Ask your business question",
        placeholder=(
            "Example: Which region performs best "
            "and why?"
        ),
        key="business_ai_question",
    )

    # ======================================================
    # ASK BUTTON
    # ======================================================

    ask_button = st.button(
        "🚀 Ask AI",
        use_container_width=False,
    )

    if ask_button:

        if not question.strip():

            st.warning(
                "Please enter a business question."
            )

        else:

            try:

                if ai_mode == "Business Rules":

                    with st.spinner(
                        "🔎 Analyzing your business data..."
                    ):

                        answer = ask_business_ai(
                            question,
                            data,
                        )

                else:

                    with st.spinner(
                        "🤖 Gemini is analyzing your business..."
                    ):

                        answer = ask_gemini(
                            question,
                            data,
                        )

                # --------------------------------------------------
                # Store conversation
                # --------------------------------------------------

                st.session_state.chat_history.append(
                    (
                        "🧑 You",
                        question,
                    )
                )

                st.session_state.chat_history.append(
                    (
                        "🤖 AI",
                        answer,
                    )
                )

            except Exception as error:

                st.session_state.chat_history.append(
                    (
                        "🧑 You",
                        question,
                    )
                )

                st.session_state.chat_history.append(
                    (
                        "⚠️ AI Error",
                        str(error),
                    )
                )

    # ======================================================
    # CONVERSATION
    # ======================================================

    if st.session_state.chat_history:

        st.markdown(
            "### 💬 Conversation"
        )

        for role, message in (
            st.session_state.chat_history
        ):

            if role == "🧑 You":

                st.info(
                    f"**{role}**\n\n{message}"
                )

            elif role == "⚠️ AI Error":

                st.error(
                    f"**{role}**\n\n{message}"
                )

            else:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 🤖 AI"
                    )

                    st.markdown(
                        message
                    )

        # --------------------------------------------------
        # Clear conversation
        # --------------------------------------------------

        if st.button(
            "🗑 Clear Conversation"
        ):

            st.session_state.chat_history = []

            st.rerun()

    st.divider()

    # ======================================================
    # EXECUTIVE PDF REPORT
    # ======================================================

    st.subheader("📄 Executive Intelligence Report")

    st.markdown(
        """
        Generate a management-ready PDF containing the
        current business health, financial performance,
        leading business dimensions, AI recommendations
        and identified risks.
        """
    )

    report_col1, report_col2 = st.columns(
        [2, 1]
    )

    with report_col1:

        st.info(
            "The report will use the currently selected "
            "global filters."
        )

    with report_col2:

        generate_report = st.button(
            "📄 Generate Report",
            use_container_width=True,
        )

    if generate_report:

        filename = (
            "Executive_Report.pdf"
        )

        try:

            generate_pdf(
                filename=filename,
                score=score,
                revenue=total_sales,
                profit=total_profit,
                margin=margin,
                region=top_region,
                category=top_category,
                product=top_product,
                recommendations=recommendations,
                risks=risks,
            )

            if os.path.exists(filename):

                with open(
                    filename,
                    "rb",
                ) as pdf_file:

                    pdf_bytes = (
                        pdf_file.read()
                    )

                st.download_button(
                    label="⬇️ Download Executive Report",
                    data=pdf_bytes,
                    file_name=(
                        "AI_Business_Analytics_Report.pdf"
                    ),
                    mime="application/pdf",
                    use_container_width=True,
                )

                st.success(
                    "✅ Executive Intelligence Report "
                    "generated successfully."
                )

            else:

                st.error(
                    "❌ The PDF file could not be created."
                )

        except Exception as error:

            st.error(
                f"❌ Unable to generate the executive report: "
                f"{error}"
            )

    # ======================================================
    # FOOTER
    # ======================================================

    st.caption(
        "InsightFlow AI • AI Business Intelligence Center • "
        "AI responses depend on the selected AI engine and "
        "the currently filtered business dataset."
    )
