def calculate_transport_cost(
    distance_km: float,
    quantity_kg: float,
    rate_per_km_per_tonne: float = 15.0
) -> float:
    """
    Calculates transport cost.
    Assumption: ₹15 per km per tonne (small agri transport)
    """
    quantity_tonnes = quantity_kg / 1000
    cost = distance_km * rate_per_km_per_tonne * quantity_tonnes
    return round(cost, 2)
