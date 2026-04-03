import pytest
import pandas as pd
from tempfile import NamedTemporaryFile
from savion.parser import load_statement


def test_load_statement_success():
    csv_data = """Date,Description,Amount,Type
2023-01-15,EPF Contribution,1500.00,Debit
2023-02-10,Life Insurance Premium,5000.00,Debit
2023-03-05,Invalid Date,X,Debit
"""
    with NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as f:
        f.write(csv_data)
        f.flush()
        df = load_statement(f.name)
        assert len(df) == 2
        assert df.iloc[0]["Description"] == "EPF Contribution"


def test_missing_columns_raises_error():
    csv_data = """Date,Desc,Amount
2023-01-15,Test,1000
"""
    with NamedTemporaryFile(mode="w+", suffix=".csv", delete=False) as f:
        f.write(csv_data)
        f.flush()
        with pytest.raises(ValueError):
            load_statement(f.name)
