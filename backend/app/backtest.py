import pandas as pd
import numpy as np

def backtest(df, signals):
    df = df.copy()
    df["signal"] = signals
    
    # Shift returns to simulate execution on NEXT Open/Close
    df["next_ret"] = df["Close"].pct_change().shift(-1)
    
    # Sadece BUY sinyallerini değerlendir (Long Only Strategy)
    # Realistik olması için transaction cost (komisyon) eklenebilir ama şimdilik pas geçiyoruz.
    
    strategy_returns = df["next_ret"].where(df["signal"] == "BUY", 0)
    
    # Equity Curve
    equity = (1 + strategy_returns).cumprod()
    
    # Metrics
    total_trades = len(df[df["signal"] == "BUY"])
    wins = len(df[(df["signal"] == "BUY") & (df["next_ret"] > 0)])
    
    winrate = wins / total_trades if total_trades > 0 else 0
    
    # Sharpe Ratio (Yıllıklandırılmış, risksiz faiz 0 kabul edildi)
    mean_ret = strategy_returns.mean()
    std_ret = strategy_returns.std()
    sharpe = (mean_ret / std_ret) * np.sqrt(252) if std_ret > 0 else 0
    
    # Max Drawdown
    rolling_max = equity.cummax()
    drawdown = (equity - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    
    return {
        "winrate": round(winrate * 100, 2),
        "total_trades": total_trades,
        "sharpe_ratio": round(sharpe, 2),
        "max_drawdown": round(max_drawdown * 100, 2),
        "final_return": round((equity.iloc[-1] - 1) * 100, 2) if len(equity) > 0 else 0,
        "equity": equity.fillna(1).tolist(), # JSON serileştirme için NaN temizliği
        "drawdown": drawdown.fillna(0).tolist()
    }