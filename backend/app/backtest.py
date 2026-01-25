import pandas as pd

def backtest(df, signals):
    df = df.copy()
    df["signal"] = signals
    df["next_ret"] = df["Close"].pct_change().shift(-1)
    wins = df[(df["signal"]=="BUY") & (df["next_ret"]>0)]
    losses = df[(df["signal"]=="BUY") & (df["next_ret"]<=0)]
    winrate = len(wins)/max(1,(len(wins)+len(losses)))
    equity = (1 + df["next_ret"].where(df["signal"]=="BUY",0)).cumprod()
    return {"winrate": round(winrate*100,2), "equity": equity.tolist()}
