from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.data_sources import get_market_names, get_symbols, load_symbol
from app.features import build_features
from app.signals import generate_signal
from app.backtest import backtest
from app.vector_db import build_faiss
import pandas as pd
import numpy as np

app = FastAPI(title="VektorQuant Pro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/markets")
def list_markets():
    # HATA DÜZELTİLDİ: Artık listeden .keys() çağırmıyoruz. 
    # Doğrudan keys listesini dönen fonksiyonu kullanıyoruz.
    return {"markets": get_market_names()}

@app.get("/symbols")
def symbols(market: str = "US_TECH_GIANTS"):
    try:
        return {"symbols": get_symbols(market)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyze")
def analyze(symbol: str, market: str = "", period: str = "1y"):
    try:
        # 1. Data Loading
        df = load_symbol(symbol, period)
        
        # 2. Feature Engineering
        df, X = build_features(df)
        
        # 3. Signals (Apply to all rows for charting)
        signals = df.apply(generate_signal, axis=1).tolist()
        
        # 4. Backtest
        bt_results = backtest(df, signals)
        
        # 5. Vector AI (Similar Days)
        # Yeterli veri varsa çalıştır
        similar_days_info = []
        if len(X) > 10:
            index = build_faiss(X)
            # Search logic
            search_vector = X[-1:].reshape(1, -1)
            # Kendisi (0) ve en yakın 5 komşu
            k = min(6, len(X))
            D, I = index.search(search_vector, k)
            
            for idx in I[0]:
                if idx != len(df) - 1 and idx < len(df): # Kendisi değilse
                    date_str = df.index[idx].strftime("%Y-%m-%d")
                    ret = df.iloc[idx]["return"]
                    similar_days_info.append({"date": date_str, "return": round(ret*100, 2)})

        # Chart Data Prep
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
            "meta": {"symbol": symbol, "period": period},
            "last_close": round(df["Close"].iloc[-1], 2),
            "last_signal": signals[-1],
            "metrics": bt_results,
            "ai_analysis": similar_days_info,
            "chart_data": chart_data
        }

    except ValueError as ve:
        # Bilinen veri hataları (404 döner)
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        # Bilinmeyen sunucu hataları
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))