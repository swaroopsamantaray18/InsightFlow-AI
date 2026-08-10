import pandas as pd
import plotly.express as px
from utils.chart_theme import apply_chart_theme


def monthly_sales_chart(filtered_df):

    sales_trend = filtered_df.copy()

    sales_trend["Order Date"] = pd.to_datetime(
        sales_trend["Order Date"]
    )

    sales_trend["Month"] = sales_trend["Order Date"].dt.strftime("%Y-%m")

    monthly_sales = (
        sales_trend
        .groupby("Month")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )
    fig = apply_chart_theme(fig)

    return fig


def category_sales_chart(filtered_df):

    sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        sales,
        x="Category",
        y="Sales",
        color="Category",
        text_auto=".2s",
        title="Category Wise Sales"
    )
    fig = apply_chart_theme(fig)

    return fig


def region_sales_chart(filtered_df):

    sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        sales,
        names="Region",
        values="Sales",
        hole=0.5,
        title="Sales by Region"
    )
    fig = apply_chart_theme(fig)

    return fig

def top_products_chart(filtered_df):

    products = (
        filtered_df
        .groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    products["Short Name"] = (
        products["Product Name"]
        .str.slice(0, 35)
        + "..."
    )

    fig = px.bar(
        products,
        x="Sales",
        y="Short Name",
        orientation="h",
        color_discrete_sequence=["#4F8EF7"],
        title="🏆 Top Revenue Generating Products"
    )

    fig.update_traces(
        text=products["Sales"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside"
    )

    fig.update_layout(
    margin=dict(l=220, r=40, t=60, b=20),
    height=550,
    showlegend=False
)
    fig.update_yaxes(title=None)
    fig.update_xaxes(title="Revenue ($)")
    fig = apply_chart_theme(fig)
    
    return fig


def profit_by_category_chart(df):

    profit = (
        df.groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        profit,
        x="Category",
        y="Profit",
        color="Category",
        title="Profit by Category",
        text_auto=".2s"
    )
    fig = apply_chart_theme(fig)

    return fig
def segment_sales_chart(df):

    segment = (
        df.groupby("Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        segment,
        values="Sales",
        names="Segment",
        hole=.5,
        title="Sales by Segment"
    )
    fig = apply_chart_theme(fig)

    return fig
def shipmode_chart(df):

    ship = (
        df.groupby("Ship Mode")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        ship,
        x="Ship Mode",
        y="Sales",
        color="Ship Mode",
        title="Sales by Ship Mode"
    )
    fig = apply_chart_theme(fig)

    return fig
def discount_profit_chart(df):

    fig = px.scatter(
        df,
        x="Discount",
        y="Profit",
        color="Category",
        size="Sales",
        title="Discount vs Profit"
    )
    fig = apply_chart_theme(fig)

    return fig
def bottom_products_chart(df):

    products = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=True)
        .head(10)
        .reset_index()
    )

    products["Short Name"] = (
        products["Product Name"]
        .str.slice(0, 35) + "..."
    )

    fig = px.bar(
        products,
        x="Sales",
        y="Short Name",
        orientation="h",
        color_discrete_sequence=["#EF4444"],
        title="📉 Bottom 10 Revenue Generating Products"
    )

    fig.update_traces(
        text=products["Sales"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside"
    )

    fig.update_layout(
    margin=dict(l=220, r=40, t=60, b=20),
    height=550,
    showlegend=False
)

    fig.update_yaxes(title=None)
    fig = apply_chart_theme(fig)

    return fig
def profitable_products_chart(df):

    products = (
        df.groupby("Product Name")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    products["Short Name"] = (
        products["Product Name"]
        .str.slice(0, 35) + "..."
    )

    fig = px.bar(
        products,
        x="Profit",
        y="Short Name",
        orientation="h",
        color_discrete_sequence=["#22C55E"],
        title="💰 Top 10 Most Profitable Products"
    )

    fig.update_traces(
        text=products["Profit"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside"
    )

    fig.update_layout(
    margin=dict(l=220, r=40, t=60, b=20),
    height=550,
    showlegend=False
)

    fig.update_yaxes(title=None)
    fig = apply_chart_theme(fig)

    return fig
def subcategory_sales_chart(df):

    subcategory = (
        df.groupby("Sub-Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        subcategory,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        color="Sales",
        color_continuous_scale="Blues",
        title="📦 Sales by Sub-Category"
    )

    fig.update_layout(
        height=600,
        yaxis=dict(categoryorder="total ascending")
    )
    fig = apply_chart_theme(fig)

    return fig
def pareto_chart(df):

    pareto = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    pareto["Cumulative Sales"] = pareto["Sales"].cumsum()

    pareto["Cumulative %"] = (
        pareto["Cumulative Sales"]
        / pareto["Sales"].sum()
    ) * 100

    fig = px.line(
        pareto,
        x=pareto.index + 1,
        y="Cumulative %",
        markers=True,
        title="📊 Pareto Analysis (80/20 Rule)"
    )

    fig.update_layout(
        xaxis_title="Products (Ranked by Sales)",
        yaxis_title="Cumulative Sales %",
        height=500
    )

    fig.add_hline(
        y=80,
        line_dash="dash",
        line_color="red",
        annotation_text="80%"
    )
    fig = apply_chart_theme(fig)

    return fig
def top_customers_chart(df):

    customers = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    customers["Short Name"] = (
        customers["Customer Name"]
        .str.slice(0,25)
    )

    fig = px.bar(
        customers,
        x="Sales",
        y="Short Name",
        orientation="h",
        color="Sales",
        color_continuous_scale="Blues",
        title="🏆 Top 10 Customers by Revenue"
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        height=500
    )
    fig = apply_chart_theme(fig)

    return fig
def customer_segment_chart(df):

    segment = (
        df.groupby("Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        segment,
        names="Segment",
        values="Sales",
        hole=0.55,
        title="👥 Revenue by Customer Segment"
    )
    fig = apply_chart_theme(fig)

    return fig
def orders_per_customer_chart(df):

    orders = (
        df.groupby("Customer Name")
        .size()
        .reset_index(name="Orders")
    )

    fig = px.histogram(
        orders,
        x="Orders",
        color_discrete_sequence=["#4F8EF7"],
        nbins=15,
        title="📦 Orders per Customer"
    )
    fig = apply_chart_theme(fig)

    return fig
def customer_value_chart(df):

    customer = (
    df.groupby("Customer Name")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Segment=("Segment", "first")
    )
    .reset_index()
)

    fig = px.scatter(
        customer,
        x="Sales",
        y="Profit",
        color="Segment",
        hover_name="Customer Name",
        title="💰 Customer Value Distribution"
    )
    fig = apply_chart_theme(fig)

    return fig
def region_revenue_chart(df):

    region = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        region,
        x="Region",
        y="Sales",
        color="Sales",
        color_continuous_scale="Blues",
        title="🌍 Revenue by Region",
        text_auto=".2s"
    )
    fig = apply_chart_theme(fig)

    return fig
def region_profit_chart(df):

    profit = (
        df.groupby("Region")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        profit,
        x="Region",
        y="Profit",
        color="Profit",
        color_continuous_scale="Greens",
        title="💰 Profit by Region",
        text_auto=".2s"
    )
    fig = apply_chart_theme(fig)

    return fig
def state_sales_chart(df):

    state = (
        df.groupby("State/Province")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        state,
        x="Sales",
        y="State/Province",
        orientation="h",
        color="Sales",
        color_continuous_scale="Blues",
        title="📍 Top States by Revenue"
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        height=500
    )
    fig = apply_chart_theme(fig)

    return fig
def region_margin_chart(df):

    margin = (
        df.groupby("Region")
        .agg(
            Sales=("Sales","sum"),
            Profit=("Profit","sum")
        )
        .reset_index()
    )

    margin["Margin"] = (
        margin["Profit"] /
        margin["Sales"]
    ) * 100

    fig = px.bar(
        margin,
        x="Region",
        y="Margin",
        color="Margin",
        title="📈 Profit Margin by Region",
        text_auto=".1f"
    )
    fig = apply_chart_theme(fig)

    return fig
def state_map_chart(df):

    sales = (
        df.groupby("State/Province")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.choropleth(
        sales,
        locations="State/Province",
        locationmode="USA-states",
        color="Sales",
        scope="usa",
        fitbounds="locations",
        color_continuous_scale="Viridis",
        hover_name="State/Province",
        hover_data={
    "Sales": ":,.0f",
    "State/Province": False
}
    )

    # Make the map larger
    fig.update_layout(
    template="plotly_dark",
    height=700,
    margin=dict(l=0, r=0, t=40, b=0),
    coloraxis_showscale=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    
)

    fig.update_geos(
    showcountries=False,
    showlakes=False,
    coastlinecolor="white",
    subunitcolor="white",
    subunitwidth=0.8
)
    fig = apply_chart_theme(fig)


    return fig
    