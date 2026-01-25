import pandas as pd
import numpy as np

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-9) # Sıfıra bölme hatası önleyici
    return 100 - (100 / (1 + rs))

def calculate_macd(series, fast=12, slow=26, signal=9):
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def calculate_bollinger(series, window=20, num_std=2):
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    upper = rolling_mean + (rolling_std * num_std)
    lower = rolling_mean - (rolling_std * num_std)
    return upper, lower

def build_features(df):
    """
    Teknik indikatörleri hesaplar.
    DİKKAT: dropna() kaldırıldı. Kısa periyotlarda veri kaybını önler.
    """
    df = df.copy()
    
    # Yetersiz veri kontrolü (En az 1 bar olmalı)
    if len(df) < 2:
        return df, np.array([])

    # 1. Price Changes
    df["return"] = df["Close"].pct_change().fillna(0)
    
    # 2. Moving Averages (Veri azsa NaN kalabilir, sorun yok)
    df["ma_50"] = df["Close"].rolling(50).mean()
    df["ma_200"] = df["Close"].rolling(200).mean()
    
    # 3. RSI
    df["rsi"] = calculate_rsi(df["Close"])
    
    # 4. Bollinger Bands
    df["bb_upper"], df["bb_lower"] = calculate_bollinger(df["Close"])
    
    # 5. Volume Power
    # Hacim 0 ise hata vermesin
    vol_mean = df["Volume"].rolling(20).mean() + 1e-9
    df["vol_power"] = df["Volume"] / vol_mean
    
    # 6. Momentum
    df["momentum"] = df["Close"] - df["Close"].shift(4)

    # Temizlik: Sonsuz değerleri temizle ama NaN'ları silme (Grafik için lazım)
    df.replace([np.inf, -np.inf], 0, inplace=True)
    
    # Vector DB için Features (Sadece dolu olan satırları alacağız, burası backtest/AI için)
    # AI analizi için NaN olmayan son verileri kullanacağız
    feature_cols = ["return", "rsi", "vol_power", "momentum"]
    
    # AI matrisi için geçici temizlik (ana df'yi bozmadan)
    df_clean = df.dropna(subset=feature_cols)
    X = df_clean[feature_cols].values.astype("float32")
    
    # Normalizasyon
    if len(X) > 0:
        mean = np.mean(X, axis=0)
        std = np.std(X, axis=0) + 1e-9
        X = (X - mean) / std

    return df, X