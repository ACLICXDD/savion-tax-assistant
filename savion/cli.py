"""
savion.cli

Command-line interface for Savion.

Commands:
- load: Validate and summarize a statement.
- analyze: Show utilization of 80C/80D.
- recommend: Show AI-powered suggestions.
- report: Generate an HTML report.
"""

import typer
from pathlib import Path
from savion.parser import load_statement
from savion.rules import load_tax_rules
from savion.analysis import compute_eligible_savings
from savion.recommendation import generate_recommendations
from savion.report import generate_html_report
import webbrowser
import sys


app = typer.Typer()


@app.command()
def load(statement: Path = typer.Option(..., "--statement", "-s")):
    """Validate and summarize a bank statement."""
    try:
        df = load_statement(str(statement))
        typer.echo(f"? Loaded {len(df)} transactions from {statement.name}")
        typer.echo(df.head())
    except Exception as e:
        typer.secho(f"? Error: {e}", fg=typer.colors.RED)
        sys.exit(1)


@app.command()
def analyze(statement: Path = typer.Option(..., "--statement", "-s")):
    """Analyze utilization of 80C and 80D."""
    try:
        df = load_statement(str(statement))
        rules = load_tax_rules()
        result = compute_eligible_savings(df, rules)
        typer.echo("?? Tax Utilization Summary:")
        typer.echo(f"  80C Used: ?{result['80C_used']:,.2f}")
        typer.echo(f"  80C Remaining: ?{result['80C_remaining']:,.2f}")
        typer.echo(f"  80D Used: ?{result['80D_used']:,.2f}")
        typer.echo(f"  80D Remaining: ?{result['80D_remaining']:,.2f}")
        typer.echo(f"  Total Tax Saved: ?{result['total_tax_saved']:,.2f}")
    except Exception as e:
        typer.secho(f"? Error: {e}", fg=typer.colors.RED)
        sys.exit(1)


@app.command()
def recommend(statement: Path = typer.Option(..., "--statement", "-s")):
    """Recommend tax-saving instruments."""
    try:
        df = load_statement(str(statement))
        rules = load_tax_rules()
        result = compute_eligible_savings(df, rules)
        recommendations = generate_recommendations(
            result["80C_remaining"], result["80D_remaining"]
        )
        typer.echo("?? Recommended Instruments:")
        for rec in recommendations:
            typer.echo(f"- {rec['instrument']} ({rec['category']})")
            typer.echo(f"  Suggested Amount: ?{rec['suggested_amount']:,.2f}")
            typer.echo(f"  Rationale: {rec['rationale']}\n")
    except Exception as e:
        typer.secho(f"? Error: {e}", fg=typer.colors.RED)
        sys.exit(1)


@app.command()
def report(
    statement: Path = typer.Option(..., "--statement", "-s"),
    output: str = typer.Option("report.html", "--output", "-o")
):
    """Generate an HTML report."""
    try:
        df = load_statement(str(statement))
        rules = load_tax_rules()
        result = compute_eligible_savings(df, rules)

        # Get qualifying transactions
        c_keywords = rules["sections"]["80C"]["instruments"]
        d_keywords = rules["sections"]["80D"]["instruments"]
        all_keywords = c_keywords + d_keywords
        filtered_df = df[df["Description"].str.contains("|".join(all_keywords), case=False, na=False)]

        # Generate recommendations
        recommendations = generate_recommendations(
            result["80C_remaining"], result["80D_remaining"]
        )

        # Generate report
        generate_html_report(result, recommendations, filtered_df, output_path=output)
        webbrowser.open(f"file://{Path(output).resolve()}")
    except Exception as e:
        typer.secho(f"? Error: {e}", fg=typer.colors.RED)
        sys.exit(1)


if __name__ == "__main__":
    app()
