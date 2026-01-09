from backend.services.transport_cost_service import calculate_transport_cost
from backend.services.storage_loss_service import calculate_storage_loss


def compute_scenario(
    crop: str,
    quantity_kg: float,
    days_delay: int,
    market: dict,
    distance_km: float
):
    storage = calculate_storage_loss(crop, quantity_kg, days_delay)
    effective_qty = storage["effective_quantity_kg"]

    transport_cost = calculate_transport_cost(
        distance_km=distance_km,
        quantity_kg=effective_qty
    )

    gross = effective_qty * market["price_per_kg"]
    net = gross - transport_cost

    return {
        "days_delay": days_delay,
        "effective_quantity_kg": effective_qty,
        "loss_quantity_kg": storage["loss_quantity_kg"],
        "gross_revenue": round(gross, 2),
        "transport_cost": transport_cost,
        "net_revenue": round(net, 2),
        "risk_note": storage["risk_note"]
    }


def compare_sell_now_vs_later(
    crop: str,
    quantity_kg: float,
    sell_after_days: int,
    market: dict,
    distance_km: float
):
    sell_now = compute_scenario(
        crop, quantity_kg, 0, market, distance_km
    )

    sell_later = compute_scenario(
        crop, quantity_kg, sell_after_days, market, distance_km
    )

    better = "later" if sell_later["net_revenue"] > sell_now["net_revenue"] else "now"

    return {
        "sell_now": sell_now,
        "sell_later": sell_later,
        "better_option": better
    }
