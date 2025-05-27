from fastapi import APIRouter, HTTPException, Query
from services.fmp_api import fetch_stock

router = APIRouter()

@router.get("/api/stock")
def get_stock(symbol: str = Query(...)):
    try:
        stock = fetch_stock(symbol)
        return stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

