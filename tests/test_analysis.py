import pytest
import pandas as pd
from savion.analysis import compute_eligible_savings


@pytest.fixture
def mock_rules():
    return {
        "sections": {
            "80C": {
                "limit": 150000,
                "instruments": ["epf", "lic", "ppf"]
            },
            "80D": {
                "self_limit": 25000,
                "parents_limit": 25000,
                "senior_citizen_extra": 5000,
                "instruments": ["health"]
            }
        }
    }


def test_compute_eligible_savings(mock_rules):
    data = {
        "Date": ["2023-01-01", "2023-02-01"],
        "Description": ["LIC Premium", "Health Insurance"],
        "Amount": [50000, 8000],
        "Type": ["Debit", "Debit"]
    }
    df = pd.DataFrame(data)
    result = compute_eligible_savings(df, mock_rules)

    assert result["80C_used"] == 50000
    assert result["80C_remaining"] == 100000
    assert result["80D_used"] == 8000
    assert result["80D_remaining"] == 17000
    assert result["total_tax_saved"] == pytest.approx(17400.0, 0.1)
