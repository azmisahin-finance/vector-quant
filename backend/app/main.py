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
    return {"markets": get_market_names()}

@app.get("/symbols")
def symbols(market: str = "US_TECH_GIANTS"):
    try:
        return {"symbols": get_symbols(market)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyze")
def analyze(symbol: str, period: str = "1y", interval: str = "1d"):
    try:
        # 1. Data Loading (Interval parametresi ile)
        df = load_symbol(symbol, period, interval)
        
        # 2. Feature Engineering
        df, X = build_features(df)
        
        if df.empty or len(df) < 2:
            raise ValueError("Insufficient data bars for analysis. Try increasing period.")

        # 3. Signals
        signals = []
        for index, row in df.iterrows():
            try:
                if pd.isna(row['rsi']) or pd.isna(row['bb_upper']):
                    signals.append("HOLD")
                else:
                    signals.append(generate_signal(row))
            except:
                signals.append("HOLD")
        
        # 4. Backtest
        bt_results = backtest(df, signals)
        
        # 5. Vector AI (Similar Days)
        similar_days_info = []
        if len(X) > 10:
            try:
                index = build_faiss(X)
                search_vector = X[-1:].reshape(1, -1)
                k = min(6, len(X))
                D, I = index.search(search_vector, k)
                for idx in I[0]:
                    if idx < len(df) and idx != len(df) - 1:
                        date_str = df.index[idx].strftime("%Y-%m-%d %H:%M") # Saat detayı eklendi
                        ret = df.iloc[idx]["return"]
                        similar_days_info.append({"date": date_str, "return": round(ret*100, 2)})
            except: pass

        # JSON Prep
        # Datetime formatını interval'e göre ayarla (Intraday ise saat önemli)
        date_format = "%Y-%m-%d %H:%M" if interval in ["15m", "30m", "1h", "90m"] else "%Y-%m-%d"
        
        rsi_clean = df["rsi"].fillna(50).tolist()
        bb_upper_clean = df["bb_upper"].bfill().ffill().fillna(df["Close"]).tolist()
        bb_lower_clean = df["bb_lower"].bfill().ffill().fillna(df["Close"]).tolist()

        chart_data = {
            "dates": df.index.strftime(date_format).tolist(),
            "open": df["Open"].tolist(),
            "high": df["High"].tolist(),
            "low": df["Low"].tolist(),
            "close": df["Close"].tolist(),
            "volume": df["Volume"].fillna(0).tolist(),
            "rsi": rsi_clean,
            "bb_upper": bb_upper_clean,
            "bb_lower": bb_lower_clean,
            "signals": signals
        }

        return {
            "meta": {"symbol": symbol, "period": period, "interval": interval},
            "last_close": round(df["Close"].iloc[-1], 2),
            "last_signal": signals[-1] if signals else "HOLD",
            "metrics": bt_results,
            "ai_analysis": similar_days_info,
            "chart_data": chart_data
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))