from backend.services.transport_cost_service import calculate_transport_cost
from backend.services.storage_loss_service import calculate_storage_loss
from backend.data.market_distances import MARKET_DISTANCE_MAP


def analyze_markets(
    crop: str,
    quantity_kg: float,
    days_delay: int,
    farmer_district: str,
    market_prices: list
):
    results = []

    distance_info = MARKET_DISTANCE_MAP.get(farmer_district, {})

    for market in market_prices:
        market_name = market["market"]
        distance_km = distance_info.get(market_name, 50)  # fallback

        storage = calculate_storage_loss(crop, quantity_kg, days_delay)
        effective_qty = storage["effective_quantity_kg"]

        transport_cost = calculate_transport_cost(
            distance_km=distance_km,
            quantity_kg=effective_qty
        )

        gross = effective_qty * market["price_per_kg"]
        net = gross - transport_cost

        results.append({
            "market": market_name,
            "distance_km": distance_km,
            "price_per_kg": market["price_per_kg"],
            "net_revenue": round(net, 2),
            "loss_kg": round(storage["loss_quantity_kg"], 2),
            "risk": storage["risk_note"]
        })

    # Sort by best net revenue
    results.sort(key=lambda x: x["net_revenue"], reverse=True)
    return results
