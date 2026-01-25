import yfinance as yf
from app.market_data import MARKET_INDICES

def get_market_names():
    return list(MARKET_INDICES.keys())

def get_symbols(market_key):
    if not market_key or market_key not in MARKET_INDICES:
        return MARKET_INDICES["US_TECH_GIANTS"]
    return MARKET_INDICES[market_key]

def load_symbol(symbol, period="1y", interval="1d"):
    """
    yfinance üzerinden veri çeker.
    Artık 'interval' parametresi alıyor (1d, 1h, 15m, 1wk, 1mo).
    """
    try:
        # Ticker objesi
        ticker = yf.Ticker(symbol)
        
        # Veriyi çek (interval eklendi)
        df = ticker.history(period=period, interval=interval)
        
        # Fallback
        if df is None or df.empty:
            df = yf.download(symbol, period=period, interval=interval, progress=False)
        
        if df.empty:
            raise ValueError(f"No data found for {symbol} with interval {interval}")

        # Timezone temizliği
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        
        return df

    except Exception as e:
        print(f"Data Source Error ({symbol}): {e}")
        raise ValueError(f"Yahoo Finance Error: {str(e)}")