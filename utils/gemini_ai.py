import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)


def ask_gemini(question, df):

    # ======================================================
    # BUSINESS OVERVIEW
    # ======================================================

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()

    total_orders = df["Order ID"].nunique()
    total_customers = df["Customer Name"].nunique()

    margin = (total_profit / total_sales) * 100

    top_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    top_category = (
        df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    top_product = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .idxmax()
    )

    # ======================================================
    # REGIONAL SALES
    # ======================================================

    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
        .to_string()
    )

    # ======================================================
    # CATEGORY SALES
    # ======================================================

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
        .to_string()
    )

    # ======================================================
    # SEGMENT SALES
    # ======================================================

    segment_sales = (
        df.groupby("Segment")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
        .to_string()
    )

    # ======================================================
    # TOP PRODUCTS
    # ======================================================

    top_products = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .round(2)
        .to_string()
    )

    # ======================================================
    # TOP CUSTOMERS
    # ======================================================

    top_customers = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .round(2)
        .to_string()
    )

    # ======================================================
    # MONTHLY SALES
    # ======================================================

    monthly_sales = (
        df.groupby(
            df["Order Date"].dt.to_period("M")
        )["Sales"]
        .sum()
    )

    monthly_sales.index = monthly_sales.index.astype(str)

    monthly_sales = (
        monthly_sales
        .round(2)
        .to_string()
    )

    # ======================================================
    # PROMPT
    # ======================================================

    prompt = f"""
You are a Senior Business Intelligence Consultant.

Your task is to analyze the following business data and answer the user's question like an experienced executive consultant.

==================================================
BUSINESS OVERVIEW
==================================================

Total Revenue:
${total_sales:,.2f}

Total Profit:
${total_profit:,.2f}

Profit Margin:
{margin:.2f}%

Total Orders:
{total_orders}

Total Customers:
{total_customers}

Top Region:
{top_region}

Top Category:
{top_category}

Top Product:
{top_product}

==================================================
REGIONAL SALES
==================================================

{region_sales}

==================================================
CATEGORY SALES
==================================================

{category_sales}

==================================================
CUSTOMER SEGMENTS
==================================================

{segment_sales}

==================================================
TOP 10 PRODUCTS
==================================================

{top_products}

==================================================
TOP 10 CUSTOMERS
==================================================

{top_customers}

==================================================
MONTHLY SALES TREND
==================================================

{monthly_sales}

==================================================
USER QUESTION
==================================================

{question}

==================================================
INSTRUCTIONS
==================================================

Return your answer in professional Markdown.

Structure your answer like this:

# Executive Summary

## Key Findings

## Business Risks

## Growth Opportunities

## Actionable Recommendations

## CEO Action Plan

Rules:

- Keep the answer under 400 words.
- Never invent numbers.
- Use only the provided data.
- Explain your reasoning clearly.
- Use bullet points wherever appropriate.
- Think like a McKinsey / Deloitte Business Consultant.
"""

    # ======================================================
    # GEMINI RESPONSE
    # ======================================================

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )

    return response.text