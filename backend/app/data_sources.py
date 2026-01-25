import yfinance as yf
import requests

def load_us_stock(symbol="AAPL", period="1y"):
    df = yf.download(symbol, period=period)
    df.dropna(inplace=True)
    return df

def load_crypto(symbol="BTC-USD", period="1y"):
    df = yf.download(symbol, period=period)
    df.dropna(inplace=True)
    return df

def load_bist(symbol="THYAO.IS", period="1y"):
    # Finnhub / Investing / başka API olabilir
    # Şimdilik Yahoo Finance ile örnek
    df = yf.download(symbol, period=period)
    df.dropna(inplace=True)
    return df
