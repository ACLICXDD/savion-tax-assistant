# savion/analysis.py

import pandas as pd


def compute_eligible_savings(df: pd.DataFrame, rules: dict) -> dict:
    """
    Analyze transactions and compute tax-saving opportunities under 80C and 80D.

    Args:
        df: Cleaned transaction DataFrame with 'Description' and 'Amount'.
        rules: Loaded from tax_rules.yaml via load_tax_rules().

    Returns:
        Dictionary with breakdown of used, remaining, and estimated tax saved.
    """

    # Extract keywords for matching
    c_keywords = rules["sections"]["80C"]["instruments"]
    d_keywords = rules["sections"]["80D"]["instruments"]

    # Filter relevant transactions
    c_txns = df[df["Description"].str.contains("|".join(c_keywords), case=False, na=False)]
    d_txns = df[df["Description"].str.contains("|".join(d_keywords), case=False, na=False)]

    # Sum up qualifying amounts
    c_total = c_txns["Amount"].sum()
    d_total = d_txns["Amount"].sum()

    # Get limits
    c_limit = rules["sections"]["80C"]["limit"]
    d_self_limit = rules["sections"]["80D"]["self_limit"]
    d_parents_limit = rules["sections"]["80D"]["parents_limit"]
    senior_bonus = rules["sections"]["80D"]["senior_citizen_extra"]

    # Assume user claims for self only (can expand later)
    d_limit = d_self_limit  # + d_parents_limit if applicable

    # Cap actual usage at limit
    c_used = min(c_total, c_limit)
    d_used = min(d_total, d_limit)

    # Remaining unused capacity
    c_remaining = max(0, c_limit - c_used)
    d_remaining = max(0, d_limit - d_used)

    # Estimate tax saved assuming highest slab rate of 30%
    # In real-world apps, consider dynamic slab calculation
    tax_saved_80c = c_used * 0.30
    tax_saved_80d = d_used * 0.30

    total_tax_saved = tax_saved_80c + tax_saved_80d

    return {
    "80C_used": round(float(c_used), 2),
    "80C_remaining": round(float(c_remaining), 2),
    "80D_used": round(float(d_used), 2),
    "80D_remaining": round(float(d_remaining), 2),
    "total_tax_saved": round(float(total_tax_saved), 2),
}
