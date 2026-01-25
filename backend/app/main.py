from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.data_sources import get_symbols, load_symbol
from app.features import build_features
from app.signals import generate_signal
from app.backtest import backtest
from app.vector_db import build_faiss

app = FastAPI(title="VektorQuant API")

# CORS frontend için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/markets")
def list_markets():
    return {"markets": list(get_symbols("").keys())}

@app.get("/symbols")
def symbols(market: str = "US"):
    return {"symbols": get_symbols(market)}

@app.get("/analyze")
def analyze(symbol: str, market: str = "US", period: str = "1y"):
    df = load_symbol(symbol, period)
    df, X = build_features(df)

    signals = [generate_signal(v) for v in X]
    bt = backtest(df, signals)

    index = build_faiss(X)
    D, I = index.search(X[-1:].reshape(1, -1), 5)

    # Son tarihi gösterelim
    last_date = df.index[-1].strftime("%Y-%m-%d")

    return {
        "symbol": symbol,
        "market": market,
        "last_signal": signals[-1],
        "winrate": bt["winrate"],
        "equity": bt["equity"],
        "similar_days": I.tolist(),
        "last_date": last_date
    }
