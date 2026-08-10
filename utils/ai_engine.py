import pandas as pd


def business_health_score(df):

    score = 0

    # Profit Margin (25)
    margin = (df["Profit"].sum() / df["Sales"].sum()) * 100

    if margin > 15:
        score += 25
    elif margin > 10:
        score += 20
    elif margin > 5:
        score += 15
    else:
        score += 5

    # Regional Balance (20)
    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
    )

    share = region_sales.max() / region_sales.sum()

    if share < 0.35:
        score += 20
    elif share < 0.45:
        score += 15
    else:
        score += 10

    # Customer Diversity (20)
    segments = df["Segment"].nunique()

    if segments >= 3:
        score += 20
    else:
        score += 10

    # Product Diversity (15)
    categories = df["Category"].nunique()

    if categories >= 3:
        score += 15
    else:
        score += 8

    # Revenue Size (20)
    sales = df["Sales"].sum()

    if sales > 2_000_000:
        score += 20
    elif sales > 1_000_000:
        score += 15
    else:
        score += 10

    return score
def generate_recommendations(df):

    recommendations = []

    # Top Category
    top_category = (
        df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    recommendations.append(
        f"Increase inventory for {top_category}."
    )

    # Weak Region
    weak_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmin()
    )

    recommendations.append(
        f"Launch marketing campaigns in {weak_region} region."
    )

    # Discount Check
    if df["Discount"].mean() > 0.15:
        recommendations.append(
            "Review high discount strategy to improve profitability."
        )

    # Customer Segment
    segment = (
        df.groupby("Segment")["Sales"]
        .sum()
        .idxmax()
    )

    recommendations.append(
        f"Focus on expanding the {segment} customer segment."
    )

    # Product Focus
    recommendations.append(
        "Prioritize the top 20% of products that generate most revenue."
    )

    return recommendations
def business_risks(df):

    risks = []

    if df["Discount"].mean() > 0.15:
        risks.append("High average discount may reduce profitability.")

    margin = (
        df["Profit"].sum() /
        df["Sales"].sum()
    ) * 100

    if margin < 12:
        risks.append("Profit margin is below the ideal level.")

    weak_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmin()
    )

    risks.append(
        f"{weak_region} region requires strategic attention."
    )

    risks.append(
        "Revenue is concentrated among a limited number of products."
    )

    return risks