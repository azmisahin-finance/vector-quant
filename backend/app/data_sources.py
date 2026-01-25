import yfinance as yf

# Dinamik semboller için backend
MARKETS = {
    "US": ["AAPL", "MSFT", "GOOGL", "TSLA"],
    "BIST": ["THYAO.IS", "ASELS.IS", "KCHOL.IS"],
    "CRYPTO": ["BTC-USD", "ETH-USD", "BNB-USD"]
}

def get_symbols(market="US"):
    return MARKETS.get(market.upper(), [])

def load_symbol(symbol, period="1y"):
    df = yf.download(symbol, period=period)
    df.dropna(inplace=True)
    return df
