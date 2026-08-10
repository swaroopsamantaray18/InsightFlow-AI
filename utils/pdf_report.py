from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


def generate_pdf(
    filename,
    score,
    revenue,
    profit,
    margin,
    region,
    category,
    product,
    recommendations,
    risks,
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    story = []

    story.append(
        Paragraph(
            "AI Business Analytics Executive Report",
            title,
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Business Health Score:</b> {score}/100",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Total Revenue:</b> ${revenue:,.2f}",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Total Profit:</b> ${profit:,.2f}",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Profit Margin:</b> {margin:.2f}%",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Top Region:</b> {region}",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Top Category:</b> {category}",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Top Product:</b> {product}",
            styles["BodyText"],
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "AI Recommendations",
            styles["Heading2"],
        )
    )

    for rec in recommendations:
        story.append(
            Paragraph(
                f"• {rec}",
                styles["BodyText"],
            )
        )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "Business Risks",
            styles["Heading2"],
        )
    )

    for risk in risks:
        story.append(
            Paragraph(
                f"• {risk}",
                styles["BodyText"],
            )
        )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Generated using AI Business Analytics Assistant",
            styles["Italic"],
        )
    )

    doc.build(story)