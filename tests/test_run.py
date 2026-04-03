# test_run.py

from savion.parser import load_statement
from savion.rules import load_tax_rules
from savion.analysis import compute_eligible_savings
from savion.report import generate_html_report


if __name__ == "__main__":
    print("🚀 Loading sample statement...")
    df = load_statement("data/sample_statement.csv")

    print("\n📚 Loading tax rules...")
    rules = load_tax_rules("tax_rules.yaml")

    print("\n📊 Computing savings...")
    result = compute_eligible_savings(df, rules)

    # Filter qualifying transactions for display
    c_keywords = rules["sections"]["80C"]["instruments"]
    d_keywords = rules["sections"]["80D"]["instruments"]
    all_keywords = c_keywords + d_keywords
    filtered_df = df[df["Description"].str.contains("|".join(all_keywords), case=False, na=False)]

    print("\n📄 Generating HTML report...")
    generate_html_report(result, filtered_df)
