# savion/rules.py

import yaml
from pathlib import Path


def load_tax_rules(yaml_path: str = "tax_rules.yaml") -> dict:
    """
    Load tax rules from a YAML file.

    Returns:
        A dictionary containing section limits and eligible instruments.
    """
    path = Path(yaml_path)
    if not path.exists():
        raise FileNotFoundError(f"Tax rules file not found: {yaml_path}")

    with open(path, "r") as f:
        rules = yaml.safe_load(f)

    return rules
    