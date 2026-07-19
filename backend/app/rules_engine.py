import json
from pathlib import Path


RULES_FILE = Path(__file__).resolve().parents[2] / "rules" / "rule_corpus.jsonl"
_RULES_CACHE = None


def _load_rules():
    global _RULES_CACHE
    if _RULES_CACHE is None:
        rules = []
        with RULES_FILE.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    rules.append(json.loads(line))
        _RULES_CACHE = rules
    return _RULES_CACHE


def get_income_limit_rule(household_size: int):
    """Return the official HUD income-limit rule for the requested household size."""
    if not 1 <= household_size <= 8:
        raise ValueError("household_size must be between 1 and 8")

    for rule in _load_rules():
        if rule.get("rule_id") == "HUD-MTSP-002":
            return {
                "rule_id": rule["rule_id"],
                "authority": rule["authority"],
                "effective_date": rule["effective_date"],
                "text": rule["text"],
                "source_url": rule["source_url"],
                "source_locator": rule["source_locator"],
                "household_size": household_size,
            }

    raise ValueError("Official HUD income limit rule was not found")
