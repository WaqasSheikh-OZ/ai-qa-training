from decimal import Decimal


def parse_price(text: str) -> Decimal:
    return Decimal(text.strip().replace("$", "").replace(",", ""))


def format_price(amount: Decimal) -> str:
    return f"${amount:.2f}"
