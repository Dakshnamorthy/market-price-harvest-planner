import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "market_prices"

def _load(file_name: str):
    with open(DATA_DIR / file_name, "r", encoding="utf-8") as f:
        return json.load(f)

def get_market_prices(crop: str, district: str | None = None):
    crop = crop.lower()

    data = _load("tn_uzhavar_prices.json") + _load("agmarknet_prices.json")

    results = []
    for r in data:
        if r["crop"].lower() == crop:
            if district is None or r["district"].lower() == district.lower():
                results.append(r)

    return results
