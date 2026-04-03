# savion/parser.py

import pandas as pd
from pathlib import Path


def load_statement(csv_path: str) -> pd.DataFrame:
    """
    Load and clean a bank statement CSV file.

    Expected Columns:
        Date, Description, Amount, Type

    Returns:
        A cleaned pandas DataFrame with parsed dates and numeric amounts.
    """
    # Resolve the path
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {csv_path}")

    # Read the CSV
    df = pd.read_csv(path)

    # Check for required columns
    required_columns = {"Date", "Description", "Amount", "Type"}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    # Parse Date column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Convert Amount to float
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # Drop rows where Date or Amount could not be parsed
    df.dropna(subset=["Date", "Amount"], inplace=True)

    return df
