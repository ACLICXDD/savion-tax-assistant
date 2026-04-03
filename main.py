# savion/main.py

import typer
from pathlib import Path
from savion.parser import load_statement
from savion.rules import load_tax_rules
from savion.analysis import compute_eligible_savings
from savion.report import generate_html_report
import webbrowser
import sys


app = typer.Typer()


@app.command()
def analyze(
    csv: Path = typer.Option(..., "--csv", help="Path to bank statement CSV."),
    output: str = typer.Option("report.html", "--output", "-o", help="Output HTML filename.")
):
    """
    Analyze your bank statement and generate a tax-saving report.
    """
    try:
        typer.echo("🚀 Loading bank statement...")
        df = load_statement(str(csv))

        typer.echo("📚 Loading tax rules...")
        rules = load_tax_rules()

        typer.echo("📊 Calculating tax savings...")
        result = compute_eligible_savings(df, rules)

        # Get qualifying transactions for report
        c_keywords = rules["sections"]["80C"]["instruments"]
        d_keywords = rules["sections"]["80D"]["instruments"]
        all_keywords = c_keywords + d_keywords
        filtered_df = df[df["Description"].str.contains("|".join(all_keywords), case=False, na=False)]

        typer.echo("📄 Generating HTML report...")
        recommendations = ["Consider investing in ELSS for higher returns.", "Max out your PPF contribution."]
        report_path = generate_html_report(result, recommendations, filtered_df, output_path=output)

        typer.secho(f"✅ Done! Opening report...", fg=typer.colors.GREEN)
        # Handle backslashes on Windows for URL file:// formatting
        webbrowser.open(f"file:///{report_path.replace(chr(92), '/')}")

    except Exception as e:
        typer.secho(f"❌ Error: {str(e)}", fg=typer.colors.RED)
        sys.exit(1)


if __name__ == "__main__":
    app()
