from fastapi import APIRouter, Query
from backend.services.market_price_service import get_market_prices


router = APIRouter(prefix="/api/market-prices", tags=["Market Prices"])

@router.get("/")
def fetch_market_prices(
    crop: str = Query(...),
    district: str | None = Query(None)
):
    prices = get_market_prices(crop, district)

    if not prices:
        return {"status": "no_data"}

    return {
        "status": "success",
        "count": len(prices),
        "data": prices
    }
