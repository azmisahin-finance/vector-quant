import yfinance as yf
from app.market_data import MARKET_INDICES

def get_market_names():
    """Mevcut market kategorilerini döner."""
    return list(MARKET_INDICES.keys())

def get_symbols(market_key):
    """Seçilen marketin sembol listesini döner."""
    if not market_key or market_key not in MARKET_INDICES:
        return MARKET_INDICES["US_TECH_GIANTS"]
    return MARKET_INDICES[market_key]

def load_symbol(symbol, period="1y"):
    """
    yfinance üzerinden veri çeker.
    Session injection KALDIRILDI (Hata sebebi buydu).
    yfinance'in kendi iç mekanizmasına bırakıyoruz.
    """
    try:
        # 1. Ticker objesi oluştur (Session parametresi YOK)
        ticker = yf.Ticker(symbol)
        
        # 2. Veriyi çek
        df = ticker.history(period=period)
        
        # 3. Veri boşsa alternatif yöntem dene
        if df is None or df.empty:
            df = yf.download(symbol, period=period, progress=False)
        
        # 4. Hala boşsa hata fırlat
        if df.empty:
            raise ValueError(f"No data found for symbol: {symbol}")

        # 5. Timezone temizliği (Grafiklerin çökmemesi için şart)
        df.index = df.index.tz_localize(None)
        
        return df

    except Exception as e:
        print(f"Data Source Error ({symbol}): {e}")
        raise ValueError(f"Yahoo Finance Error: {str(e)}")