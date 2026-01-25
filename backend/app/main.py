from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.data_sources import get_symbols, load_symbol
from app.features import build_features
from app.signals import generate_signal
from app.backtest import backtest
from app.vector_db import build_faiss
import pandas as pd
import numpy as np

app = FastAPI(title="VektorQuant Professional API")

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
    try:
        return {"symbols": get_symbols(market)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyze")
def analyze(symbol: str, market: str = "US", period: str = "1y"):
    try:
        # 1. Data Loading
        df = load_symbol(symbol, period)
        if df.empty:
            raise HTTPException(status_code=404, detail="Symbol data not found")

        # 2. Feature Engineering
        df, X = build_features(df)
        
        # 3. Signal Generation
        # Vektör tabanlı değil, satır bazlı logic kullanıyoruz daha kesin sonuç için
        signals = df.apply(generate_signal, axis=1).tolist()
        
        # 4. Backtesting
        bt_results = backtest(df, signals)
        
        # 5. Vector Similarity (AI Analysis)
        index = build_faiss(X)
        # Son günün vektörü ile benzer geçmiş günleri bul
        D, I = index.search(X[-1:].reshape(1, -1), 6) # Kendisi dahil 6
        similar_indices = I[0][1:] # Kendisini (0. indeks) çıkar
        
        # Benzer günlerin tarihleri ve getirileri
        similar_days_info = []
        for idx in similar_indices:
            if idx < len(df):
                date_str = df.index[idx].strftime("%Y-%m-%d")
                ret = df.iloc[idx]["return"]
                similar_days_info.append({"date": date_str, "return": round(ret*100, 2)})

        # Prepare Chart Data (JSON friendly)
        chart_data = {
            "dates": df.index.strftime("%Y-%m-%d").tolist(),
            "open": df["Open"].tolist(),
            "high": df["High"].tolist(),
            "low": df["Low"].tolist(),
            "close": df["Close"].tolist(),
            "volume": df["Volume"].tolist(),
            "rsi": df["rsi"].fillna(50).tolist(),
            "bb_upper": df["bb_upper"].fillna(method='bfill').tolist(),
            "bb_lower": df["bb_lower"].fillna(method='bfill').tolist(),
            "signals": signals
        }

        return {
            "meta": {"symbol": symbol, "market": market, "period": period},
            "last_close": round(df["Close"].iloc[-1], 2),
            "last_signal": signals[-1],
            "metrics": bt_results,
            "ai_analysis": similar_days_info,
            "chart_data": chart_data
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))