import yfinance as yf

# Dinamik marketler
MARKETS = {
    "US": ["AAPL","MSFT","GOOGL","TSLA"],
    "BIST": ["THYAO.IS","ASELS.IS","KCHOL.IS"],
    "CRYPTO": ["BTC-USD","ETH-USD","BNB-USD"]
}

def get_symbols(market="US"):
    return MARKETS.get(market.upper(), [])

def load_symbol(symbol, period="1y"):
    try:
        df = yf.download(symbol, period=period)
        df.dropna(inplace=True)
        if df.empty:
            raise ValueError("Veri bulunamadı")
        return df
    except Exception as e:
        raise ValueError(f"Veri yükleme hatası: {e}")
