import numpy as np

def build_features(df):
    df["return"] = df["Close"].pct_change()
    df["ma_fast"] = df["Close"].rolling(5).mean()
    df["ma_slow"] = df["Close"].rolling(20).mean()
    df["momentum"] = df["ma_fast"] - df["ma_slow"]
    df["vol_power"] = df["Volume"] / df["Volume"].rolling(20).mean()
    df = df.dropna()
    X = df[["return", "vol_power", "momentum"]].values.astype("float32")
    return df, X
