import re

def parse_currency(value: str) -> float:
    """Parse a currency string like '$2,000.50' into a float."""
    # Remove everything except digits and decimal point
    clean_val = re.sub(r'[^\d.]', '', value)
    if not clean_val:
        raise ValueError(f"Could not parse currency from {value}")
    return float(clean_val)

def calculate_annualized_income(gross_pay_str: str, pay_period: str) -> float:
    """
    Deterministically calculate annualized income.
    This logic MUST be separated from the AI.
    """
    gross_pay = parse_currency(gross_pay_str)
    period = pay_period.lower().strip()
    
    # Check if it's a date range like '2026-06-17 to 2026-06-23'
    import re
    from datetime import datetime
    date_match = re.search(r'(\d{4}-\d{2}-\d{2}).*?(\d{4}-\d{2}-\d{2})', period)
    if date_match:
        try:
            start_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
            end_date = datetime.strptime(date_match.group(2), "%Y-%m-%d")
            days = (end_date - start_date).days
            if 5 <= days <= 7:
                period = "weekly"
            elif 12 <= days <= 15:
                period = "bi-weekly"
            elif 28 <= days <= 31:
                period = "monthly"
        except Exception:
            pass

    # Common variations mapping
    if period in ["weekly", "week", "per week", "every week"]:
        multiplier = 52
    elif period in ["bi-weekly", "bi_weekly", "biweekly", "every two weeks", "every 2 weeks"]:
        multiplier = 26
    elif period in ["semi-monthly", "semi_monthly", "semimonthly", "twice a month"]:
        multiplier = 24
    elif period in ["monthly", "month", "per month"]:
        multiplier = 12
    elif period in ["annually", "annual", "yearly", "year", "per year"]:
        multiplier = 1
    else:
        raise ValueError(f"Unknown or unsupported pay period: '{pay_period}'. Please review and correct.")
        
    return gross_pay * multiplier
