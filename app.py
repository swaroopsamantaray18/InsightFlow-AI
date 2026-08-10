# ==========================================================
# AI BUSINESS ANALYTICS PLATFORM
# Version 2.0
# Developed by Swaroop Samantaray
# ==========================================================

import streamlit as st

# ==========================================================
# Utilities
# ==========================================================

from utils.load_data import load_data

# ==========================================================
# Views
# ==========================================================

from views.home import show_home
from views.executive_dashboard import show_executive_dashboard
from views.sales_analytics import show_sales_analytics
from views.product_analytics import show_product_analytics
from views.customer_analytics import show_customer_analytics
from views.regional_analytics import show_regional_analytics
from views.ai_insights import show_ai_insights
from views.forecast_analytics import show_forecast_analytics


# ==========================================================
# Load Global CSS
# ==========================================================

def load_css():

    with open("assets/style.css") as css:

        st.markdown(

            f"<style>{css.read()}</style>",

            unsafe_allow_html=True

        )


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(

    page_title="InsightFlow AI",

    page_icon="🚀",

    layout="wide",

    initial_sidebar_state="expanded"

)

load_css()

# ==========================================================
# Load Dataset
# ==========================================================

df = load_data()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    # ------------------------------------------------------
    # Branding
    # ------------------------------------------------------

    st.markdown("""
# 🚀 InsightFlow AI

### Enterprise BI Platform
""")

    st.success("🟢 System Online")

    st.caption("Version 2.0")

    st.divider()

    # ------------------------------------------------------
    # Filters
    # ------------------------------------------------------

    with st.expander("🔍 Global Filters", expanded=True):

        region = st.selectbox(

            "🌍 Region",

            ["All"] + sorted(df["Region"].unique())

        )

        category = st.selectbox(

            "📦 Category",

            ["All"] + sorted(df["Category"].unique())

        )

        segment = st.selectbox(

            "👥 Segment",

            ["All"] + sorted(df["Segment"].unique())

        )
    # ==========================================================
# APPLY GLOBAL FILTERS
# ==========================================================

filtered_df = df.copy()

if region != "All":

    filtered_df = filtered_df[
        filtered_df["Region"] == region
    ]

if category != "All":

    filtered_df = filtered_df[
        filtered_df["Category"] == category
    ]

if segment != "All":

    filtered_df = filtered_df[
        filtered_df["Segment"] == segment
    ]


# ==========================================================
# CONTINUE SIDEBAR
# ==========================================================

with st.sidebar:

    # ------------------------------------------------------
    # Dataset Overview
    # ------------------------------------------------------

    with st.expander("📊 Dataset Overview", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Orders",
                f"{len(filtered_df):,}"
            )

        with col2:

            st.metric(
                "Customers",
                f"{filtered_df['Customer ID'].nunique():,}"
            )

        st.metric(
            "Revenue",
            f"${filtered_df['Sales'].sum():,.0f}"
        )

        st.metric(
            "Profit",
            f"${filtered_df['Profit'].sum():,.0f}"
        )

    # ------------------------------------------------------
    # Navigation
    # ------------------------------------------------------

    with st.expander("📌 Navigation", expanded=True):

        page = st.radio(

            "",

            [

                "🏠 Home",

                "🏢 Executive Dashboard",

                "📈 Sales Analytics",

                "📦 Product Analytics",

                "👥 Customer Analytics",

                "🌍 Regional Analytics",

                "🔮 Sales Forecast",

                "🤖 AI Insights"

            ]

        )

    # ------------------------------------------------------
    # Platform Information
    # ------------------------------------------------------

    with st.expander("⚙ Platform", expanded=False):

        st.success("🤖 Gemini AI")

        st.success("📈 Machine Learning")

        st.success("🔮 Forecasting")

        st.success("📄 Executive PDF Reports")

        st.success("📊 Interactive Dashboards")

        st.success("📈 Plotly Visualizations")

    # ------------------------------------------------------
    # About Developer
    # ------------------------------------------------------

    with st.expander("👨‍💻 About Developer", expanded=False):

        st.markdown("""
### Swaroop K Samantaray

🎓 **Data Science Engineer**

🤖 Artificial Intelligence

📊 Business Intelligence

📈 Machine Learning

🇮🇳 Bhubaneswar, India

---

**Project**

InsightFlow AI

Enterprise Business Intelligence Platform

Version **2.0**

© 2026
""")
# ==========================================================
# MAIN CONTENT
# ==========================================================

if page == "🏠 Home":

    show_home()

elif page == "🏢 Executive Dashboard":

    show_executive_dashboard(filtered_df)

elif page == "📈 Sales Analytics":

    show_sales_analytics(filtered_df)

elif page == "📦 Product Analytics":

    show_product_analytics(filtered_df)

elif page == "👥 Customer Analytics":

    show_customer_analytics(filtered_df)

elif page == "🌍 Regional Analytics":

    show_regional_analytics(filtered_df)

elif page == "🔮 Sales Forecast":

    show_forecast_analytics(filtered_df)

elif page == "🤖 AI Insights":

    show_ai_insights(filtered_df)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

col1, col2, col3 = st.columns([2, 3, 2])

with col1:

    st.caption("🚀 InsightFlow AI")

with col2:

    st.caption(
        "Enterprise Business Intelligence Platform | Powered by Streamlit, Plotly, Gemini AI & Machine Learning"
    )

with col3:

    st.caption("© 2026 Swaroop K Samantaray")