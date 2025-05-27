import requests
from config import API_KEY as FMP_API_KEY

def fetch_stock(symbol: str):
    if not FMP_API_KEY:
        print("❌ API_KEY is missing")
    print(f"🔍 Fetching stock for symbol: {symbol} using key: {FMP_API_KEY[:4]}...")

    url = f"https://financialmodelingprep.com/stable/quote?symbol={symbol}&&apikey={FMP_API_KEY}"
    response = requests.get(url)
    try:
        response.raise_for_status()
        data = response.json()
        print("✅ FMP response:", data)
        return data
    except requests.exceptions.RequestException as e:
        print("❌ FMP request failed:", response.status_code, response.text)
        raise
