import unittest

from backend.app.calculate import evaluate_income
from backend.app.rules_engine import get_income_limit_rule


class UnderstandPhaseTests(unittest.TestCase):
    def test_evaluate_income_uses_core_challenge_threshold(self):
        result = evaluate_income(65000, 2)
        self.assertEqual(result["annualized_income"], 65000.0)
        self.assertEqual(result["household_size"], 2)
        self.assertEqual(result["threshold"], 82320.0)
        self.assertEqual(result["comparison"], "below_or_equal")
        self.assertEqual(result["effective_date"], "2026-05-01")

    def test_rule_lookup_returns_official_hud_rule(self):
        rule = get_income_limit_rule(2)
        self.assertEqual(rule["rule_id"], "HUD-MTSP-002")
        self.assertIn("60%", rule["text"])
        self.assertEqual(rule["source_locator"], "PDF page 130")


if __name__ == "__main__":
    unittest.main()
