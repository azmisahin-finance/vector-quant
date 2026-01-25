import numpy as np

def generate_signal(row):
    """
    row: Pandas Series (tek bir satır)
    """
    # Strateji 1: RSI + Bollinger Reversal
    # Fiyat alt bandın altındaysa ve RSI < 30 ise AL (Oversold)
    if row["Close"] < row["bb_lower"] and row["rsi"] < 30:
        return "BUY"
    
    # Fiyat üst bandın üzerindeyse ve RSI > 70 ise SAT (Overbought)
    if row["Close"] > row["bb_upper"] and row["rsi"] > 70:
        return "SELL"
    
    # Strateji 2: Trend Following (MACD Crossover)
    # Basit bir MACD mantığı ekleyelim (Feature olarak varsa)
    if row["macd"] > row["macd_signal"] and row["macd"] > 0:
        # Eğer zaten pozisyonda değilsek AL diyebiliriz ama burada basit tutuyoruz
        # Mevcut logic sadece tekil sinyal üretiyor, state tutmuyor.
        pass 

    return "HOLD"