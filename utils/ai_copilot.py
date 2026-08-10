def ask_business_ai(question, df):

    question = question.lower().strip()

    # ---------------------------
    # Top Region
    # ---------------------------

    if "region" in question and (
        "best" in question or
        "highest" in question or
        "top" in question
    ):

        region = (
            df.groupby("Region")["Sales"]
            .sum()
            .idxmax()
        )

        value = (
            df.groupby("Region")["Sales"]
            .sum()
            .max()
        )

        return (
            f"🌍 The highest-performing region is **{region}**, "
            f"with total sales of **${value:,.0f}**."
        )

    # ---------------------------
    # Top Category
    # ---------------------------

    elif "category" in question:

        category = (
            df.groupby("Category")["Sales"]
            .sum()
            .idxmax()
        )

        value = (
            df.groupby("Category")["Sales"]
            .sum()
            .max()
        )

        return (
            f"📦 The strongest category is **{category}**, "
            f"generating **${value:,.0f}** in sales."
        )

    # ---------------------------
    # Top Product
    # ---------------------------

    elif "product" in question:

        product = (
            df.groupby("Product Name")["Sales"]
            .sum()
            .idxmax()
        )

        return (
            f"🏆 The best-selling product is **{product}**."
        )

    # ---------------------------
    # Profit Margin
    # ---------------------------

    elif "profit" in question:

        margin = (
            df["Profit"].sum() /
            df["Sales"].sum()
        ) * 100

        return (
            f"💰 Current profit margin is **{margin:.2f}%**."
        )

    # ---------------------------
    # Recommendations
    # ---------------------------

    elif (
        "recommend" in question or
        "recommendation" in question
    ):

        return (
            "📈 Recommendation:\n\n"
            "• Increase investment in the highest-performing category.\n"
            "• Reduce excessive discounts.\n"
            "• Expand marketing in weaker regions.\n"
            "• Focus on high-value customers."
        )

    # ---------------------------
    # Dashboard Summary
    # ---------------------------

    elif (
        "summary" in question or
        "summarize" in question
    ):

        revenue = df["Sales"].sum()
        profit = df["Profit"].sum()

        return (
            f"📊 Dashboard Summary\n\n"
            f"Revenue: **${revenue:,.0f}**\n\n"
            f"Profit: **${profit:,.0f}**\n\n"
            "Business performance is healthy overall."
        )

    # ---------------------------
    # Default
    # ---------------------------

    return (
        "🤖 I couldn't understand that question.\n\n"
        "Try asking:\n"
        "• Which region performs best?\n"
        "• What is the top category?\n"
        "• Show recommendations.\n"
        "• Summarize the dashboard."
    )