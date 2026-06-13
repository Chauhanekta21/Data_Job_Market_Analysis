def format_number(value: int | float) -> str:
    return f"{value:,.0f}"


def format_currency(value: int | float) -> str:
    return f"${value / 1000:,.0f}K"
