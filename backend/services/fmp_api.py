import requests
from config import API_KEY

def fetch_stock_quote(symbol: str):
    if not API_KEY:
        print("❌ API_KEY is missing")
    print(f"🔍 Fetching stock for symbol: {symbol} using key: {API_KEY[:4]}...")

    url = f"https://financialmodelingprep.com/stable/quote?symbol={symbol}&&apikey={API_KEY}"
    response = requests.get(url)
    try:
        response.raise_for_status()
        data = response.json()
        print("✅ FMP response:", data)
        return data
    except requests.exceptions.RequestException as e:
        print("❌ FMP request failed:", response.status_code, response.text)
        raise
