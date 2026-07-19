from backend.app.calculate import evaluate_income
from backend.app.rules_engine import get_income_limit_rule

result = evaluate_income(65000, 2)
rule = get_income_limit_rule(2)
print(result)
print(rule)
