from fastapi import FastAPI
from app.data_sources import load_us_stock, load_crypto, load_bist
from app.features import build_features
from app.signals import generate_signal
from app.backtest import backtest
from app.vector_db import build_faiss

app = FastAPI(title="VektorQuant API")

@app.get("/analyze")
def analyze(symbol: str = "AAPL", market: str = "US"):
    if market.lower() == "crypto":
        df = load_crypto(symbol)
    elif market.lower() == "bist":
        df = load_bist(symbol)
    else:
        df = load_us_stock(symbol)

    df, X = build_features(df)
    signals = [generate_signal(v) for v in X]

    bt = backtest(df, signals)
    index = build_faiss(X)
    D, I = index.search(X[-1:].reshape(1, -1), 5)

    return {
        "symbol": symbol,
        "market": market,
        "last_signal": signals[-1],
        "winrate": bt["winrate"],
        "equity": bt["equity"],
        "similar_days": I.tolist()
    }
