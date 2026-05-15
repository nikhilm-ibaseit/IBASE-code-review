"""
Demo file to trigger the PR review workflow.
This simulates a real code change being reviewed.
"""


def calculate_discount(price: float, discount_pct: float) -> float:
    """Return discounted price. No validation on inputs."""
    return price * (1 - discount_pct / 100)


def process_order(items: list[dict]) -> dict:
    total = 0
    for item in items:
        qty = item["qty"]
        price = item["price"]
        total += qty * price

    return {"total": total, "item_count": len(items)}
