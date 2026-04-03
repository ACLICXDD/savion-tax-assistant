"""
savion.report

Generate a styled HTML report with tax utilization, missed opportunities,
and AI-generated recommendations.
"""

from jinja2 import Environment, FileSystemLoader
import pandas as pd
import os
from datetime import datetime


def generate_html_report(
    analysis: dict,
    recommendations: list,
    qualifying_transactions: pd.DataFrame,
    output_path: str = "report.html"
) -> None:
    """
    Render a styled HTML report summarizing tax savings and recommendations.

    Args:
        analysis: Dictionary with 80C/80D usage and tax saved.
        recommendations: List of AI-recommended instruments.
        qualifying_transactions: DataFrame of matched transactions.
        output_path: Path to save the HTML file.
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")

    html_output = template.render(
        summary=analysis,
        recommendations=recommendations,
        qualifying_transactions=qualifying_transactions.to_dict(orient="records"),
        today=datetime.now().strftime("%Y-%m-%d")
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    abs_path = os.path.abspath(output_path)
    print(f"\n? Report generated at: {abs_path}")
    return abs_path

