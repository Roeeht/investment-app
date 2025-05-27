from fastapi import APIRouter, HTTPException, Query
from services.fmp_api import fetch_stock_quote

router = APIRouter()

@router.get("/api/stock")
def get_stock(symbol: str = Query(...)):
    try:
        stock = fetch_stock_quote(symbol)
        return stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))