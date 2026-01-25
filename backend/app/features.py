import pandas as pd
import numpy as np

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
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
    df = df.copy()
    
    # 1. Price Changes
    df["return"] = df["Close"].pct_change()
    df["log_return"] = np.log(df["Close"]/df["Close"].shift(1))
    
    # 2. Moving Averages
    df["ma_50"] = df["Close"].rolling(50).mean()
    df["ma_200"] = df["Close"].rolling(200).mean()
    
    # 3. RSI
    df["rsi"] = calculate_rsi(df["Close"])
    
    # 4. MACD
    df["macd"], df["macd_signal"] = calculate_macd(df["Close"])
    
    # 5. Bollinger Bands
    df["bb_upper"], df["bb_lower"] = calculate_bollinger(df["Close"])
    
    # 6. Volume Power
    df["vol_power"] = df["Volume"] / (df["Volume"].rolling(20).mean() + 1e-9) # Zero div protection
    
    # 7. Momentum
    df["momentum"] = df["Close"] - df["Close"].shift(4)

    # Temizlik
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    
    # Vector DB için Features (Normalize edilmiş)
    # Scale features for better FAISS performance
    feature_cols = ["return", "rsi", "vol_power", "momentum"]
    X = df[feature_cols].values.astype("float32")
    
    # Normalizasyon (Basit Z-Score benzeri)
    if len(X) > 0:
        mean = np.mean(X, axis=0)
        std = np.std(X, axis=0) + 1e-9
        X = (X - mean) / std

    return df, X