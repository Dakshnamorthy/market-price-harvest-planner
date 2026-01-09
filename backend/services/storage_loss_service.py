CROP_LOSS_RATES = {
    "tomato": 2.0,
    "onion": 1.0,
    "paddy": 0.2
}

CROP_SHELF_LIFE = {
    "tomato": 7,    # days
    "onion": 30,
    "paddy": 180
}

def calculate_storage_loss(
    crop: str,
    quantity_kg: float,
    days_stored: int
):
    crop = crop.lower()

    loss_rate = CROP_LOSS_RATES.get(crop, 1.5)
    shelf_life = CROP_SHELF_LIFE.get(crop, 7)

    effective_quantity = quantity_kg * ((1 - loss_rate / 100) ** days_stored)
    loss_quantity = quantity_kg - effective_quantity

    risk = None
    if days_stored > shelf_life:
        risk = "High spoilage risk: storage beyond safe shelf-life"

    return {
        "original_quantity_kg": quantity_kg,
        "effective_quantity_kg": round(effective_quantity, 2),
        "loss_quantity_kg": round(loss_quantity, 2),
        "loss_rate_per_day": loss_rate,
        "shelf_life_days": shelf_life,
        "risk_note": risk
    }
