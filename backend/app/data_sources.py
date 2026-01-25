import yfinance as yf
import requests
import pandas as pd
from app.market_data import MARKET_INDICES

def get_market_names():
    """Mevcut market kategorilerini döner."""
    return list(MARKET_INDICES.keys())

def get_symbols(market_key):
    """Seçilen marketin sembol listesini döner."""
    # Eğer market key yoksa veya boşsa default olarak US_TECH_GIANTS dön
    if not market_key or market_key not in MARKET_INDICES:
        return MARKET_INDICES["US_TECH_GIANTS"]
    return MARKET_INDICES[market_key]

def load_symbol(symbol, period="1y"):
    """
    yfinance üzerinden veri çeker.
    """
    try:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

        ticker = yf.Ticker(symbol, session=session)
        df = ticker.history(period=period)
        
        if df is None or df.empty:
            # Fallback
            df = yf.download(symbol, period=period, progress=False)
        
        if df.empty:
            raise ValueError(f"No data found for {symbol}")

        # Timezone temizliği
        df.index = df.index.tz_localize(None)
        
        return df

    except Exception as e:
        print(f"Data Source Error ({symbol}): {e}")
        raise ValueError(f"Data load failed: {e}")