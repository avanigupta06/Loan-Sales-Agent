"""Financial utility functions."""


def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    """
    EMI = P * r * (1+r)^n / ((1+r)^n - 1)
    where r = monthly interest rate, n = tenure in months
    """
    if tenure_months <= 0 or principal <= 0:
        return 0.0
    r = annual_rate / (12 * 100)
    if r == 0:
        return principal / tenure_months
    factor = (1 + r) ** tenure_months
    emi = (principal * r * factor) / (factor - 1)
    return round(emi, 2)


def format_currency(amount: float) -> str:
    """Format amount in Indian Rupees."""
    if amount >= 10_00_000:
        return f"₹{amount / 10_00_000:.2f} Lakh"
    elif amount >= 1_000:
        return f"₹{amount:,.0f}"
    return f"₹{amount:.2f}"


def parse_amount(text: str) -> float | None:
    """Parse loan amount from user text, supporting lakh/cr notation."""
    import re
    text = text.lower().strip()
    text = text.replace(",", "").replace("₹", "").replace("rs", "").strip()

    lakh_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:lakh|lac|l\b)", text)
    if lakh_match:
        return float(lakh_match.group(1)) * 1_00_000

    cr_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:crore|cr\b)", text)
    if cr_match:
        return float(cr_match.group(1)) * 1_00_00_000

    num_match = re.search(r"(\d+(?:\.\d+)?)", text)
    if num_match:
        val = float(num_match.group(1))
        if val < 1000:
            return val * 1_00_000  # treat small numbers as lakh
        return val
    return None


def parse_tenure(text: str) -> int | None:
    """Parse tenure in months from user text."""
    import re
    text = text.lower().strip()

    year_match = re.search(r"(\d+)\s*(?:year|yr|years|yrs)", text)
    if year_match:
        return int(year_match.group(1)) * 12

    month_match = re.search(r"(\d+)\s*(?:month|months|mo)", text)
    if month_match:
        val = int(month_match.group(1))
        return val

    num_match = re.search(r"(\d+)", text)
    if num_match:
        val = int(num_match.group(1))
        if val <= 30:
            return val * 12  # assume years
        return val  # assume months
    return None
