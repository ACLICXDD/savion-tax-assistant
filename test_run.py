from savion.parser import load_statement
from savion.rules import load_tax_rules
from savion.analysis import compute_eligible_savings


if __name__ == "__main__":
    print("?? Loading sample statement...")
    df = load_statement("data/sample_statement.csv")
    print(df.head())

    print("\n?? Loading tax rules...")
    rules = load_tax_rules("tax_rules.yaml")
    print(rules.keys())

    print("\n?? Computing savings...")
    result = compute_eligible_savings(df, rules)
    print(result)
