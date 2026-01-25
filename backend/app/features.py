import numpy as np
import pandas as pd

def build_features(df):
    df["ret"] = df["Close"].pct_change()
    df["vol_power"] = df["Volume"] / df["Volume"].rolling(20).mean()
    df["ma_fast"] = df["Close"].rolling(5).mean()
    df["ma_slow"] = df["Close"].rolling(20).mean()
    df["momentum"] = df["ma_fast"] - df["ma_slow"]
    df = df.dropna()

    X = df[["ret", "vol_power", "momentum"]].values.astype("float32")
    return df, X
