import csv
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "mtsp_2026_boston_cambridge_quincy.csv"
_LIMITS_CACHE = None


def _load_income_limits():
    global _LIMITS_CACHE
    if _LIMITS_CACHE is None:
        rows = {}
        with DATA_FILE.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                household_size = int(row["household_size"])
                rows[household_size] = {
                    "household_size": household_size,
                    "threshold": float(row["core_challenge_threshold"]),
                    "effective_date": row["effective_date"],
                }
        _LIMITS_CACHE = rows
    return _LIMITS_CACHE


def evaluate_income(annualized_income: float, household_size: int):
    """Compare annualized income to the HUD 2026 core challenge threshold."""
    if annualized_income < 0:
        raise ValueError("annualized_income must be non-negative")
    if not 1 <= household_size <= 8:
        raise ValueError("household_size must be between 1 and 8")

    limits = _load_income_limits()
    limit_row = limits.get(household_size)
    if limit_row is None:
        raise ValueError("No official HUD income limit row was found for the requested household size")

    comparison = "below_or_equal" if annualized_income <= limit_row["threshold"] else "above"
    return {
        "annualized_income": float(annualized_income),
        "household_size": household_size,
        "threshold": limit_row["threshold"],
        "comparison": comparison,
        "effective_date": limit_row["effective_date"],
    }
