def calculate_kpis(df):

    total_sales = df["Sales"].sum()

    total_profit = df["Profit"].sum()

    total_orders = df["Order ID"].nunique()

    total_customers = df["Customer ID"].nunique()

    return (
        total_sales,
        total_profit,
        total_orders,
        total_customers
    )