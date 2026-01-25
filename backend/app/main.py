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
def analyze(symbol: str, period: str = "1y"):
    try:
        # 1. Data Loading
        df = load_symbol(symbol, period)
        
        # 2. Feature Engineering (Artık satır silmiyor)
        df, X = build_features(df)
        
        # GÜVENLİK KONTROLÜ: Eğer dataframe boşsa veya çok kısaysa
        if df.empty or len(df) < 2:
            raise ValueError("Insufficient data for this period (try a longer timeframe)")

        # 3. Signals (Apply to all rows)
        # Sinyal fonksiyonu NaN değerlerde hata vermemeli, "HOLD" dönmeli
        signals = []
        for index, row in df.iterrows():
            try:
                # NaN kontrolü: Eğer kritik veriler yoksa HOLD
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
        # AI için en az 10 bar gerekli, yoksa boş dön
        if len(X) > 10:
            try:
                index = build_faiss(X)
                search_vector = X[-1:].reshape(1, -1)
                k = min(6, len(X))
                D, I = index.search(search_vector, k)
                
                for idx in I[0]:
                    # Index bounds check
                    if idx < len(df) and idx != len(df) - 1:
                        date_str = df.index[idx].strftime("%Y-%m-%d")
                        ret = df.iloc[idx]["return"]
                        similar_days_info.append({"date": date_str, "return": round(ret*100, 2)})
            except Exception as ai_err:
                print(f"AI Error: {ai_err}")

        # JSON Data Preparation (Pandas 2.0 Safe)
        # NaN değerleri grafik kütüphanesi için temizle
        # bfill() ve ffill() veri boşluklarını doldurur, kalanı 0 yapar.
        rsi_clean = df["rsi"].fillna(50).tolist()
        bb_upper_clean = df["bb_upper"].bfill().ffill().fillna(df["Close"]).tolist() # BB yoksa Fiyatı bas
        bb_lower_clean = df["bb_lower"].bfill().ffill().fillna(df["Close"]).tolist()

        chart_data = {
            "dates": df.index.strftime("%Y-%m-%d").tolist(),
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

        # Son veriler (Güvenli erişim)
        last_close = df["Close"].iloc[-1]
        last_signal = signals[-1] if signals else "HOLD"

        return {
            "meta": {"symbol": symbol, "period": period},
            "last_close": round(last_close, 2),
            "last_signal": last_signal,
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