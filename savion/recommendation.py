"""
savion.recommendation

Generates a ranked list of tax-saving investment suggestions.

- Based on remaining 80C and 80D allowances.
- Uses llm_client to provide short AI explanations.
"""

from typing import List, Dict
from savion.llm_client import get_rationale


# Define instruments per section with max allowed amounts
INSTRUMENTS = {
    "80C": [
        {"name": "ELSS (Mutual Fund)", "max": 150000},
        {"name": "PPF", "max": 150000},
        {"name": "NSC", "max": 150000},
        {"name": "Sukanya Samriddhi Yojana", "max": 150000},
        {"name": "Senior Citizen Savings Scheme", "max": 150000},
        {"name": "Tax Saving FD", "max": 150000},
        {"name": "ULIP", "max": 150000},
        {"name": "NPS (Tier I)", "max": 150000},
    ],
    "80D": [
        {"name": "Health Insurance - Self", "max": 25000},
        {"name": "Health Insurance - Parents", "max": 25000},
        {"name": "Preventive Health Checkup", "max": 5000},
    ]
}


def generate_recommendations(remaining_80c: float, remaining_80d: float) -> List[Dict]:
    """
    Generate a list of recommended instruments based on unused 80C/80D limits.

    Args:
        remaining_80c: Unused 80C allowance.
        remaining_80d: Unused 80D allowance.

    Returns:
        A list of suggestion dictionaries with rationale.
    """
    suggestions = []

    # Recommend 80C instruments
    if remaining_80c > 0:
        for inst in INSTRUMENTS["80C"]:
            suggested_amount = min(inst["max"], remaining_80c)
            rationale_prompt = (
                f"You are recommending investing ?{suggested_amount:,.2f} "
                f"in {inst['name']} under Section 80C. Give a short reason why."
            )
            rationale = get_rationale(rationale_prompt)
            suggestions.append({
                "instrument": inst["name"],
                "category": "80C",
                "max_allowed": inst["max"],
                "suggested_amount": suggested_amount,
                "rationale": rationale,
                "link": ""  # Optional – can be filled later
            })

    # Recommend 80D instruments
    if remaining_80d > 0:
        for inst in INSTRUMENTS["80D"]:
            suggested_amount = min(inst["max"], remaining_80d)
            rationale_prompt = (
                f"You are recommending spending ?{suggested_amount:,.2f} "
                f"on {inst['name']} under Section 80D. Give a short reason why."
            )
            rationale = get_rationale(rationale_prompt)
            suggestions.append({
                "instrument": inst["name"],
                "category": "80D",
                "max_allowed": inst["max"],
                "suggested_amount": suggested_amount,
                "rationale": rationale,
                "link": ""
            })

    return suggestions
