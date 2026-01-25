import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="VektorQuant Dashboard", layout="wide")
st.title("📊 VektorQuant Dashboard")

# Dinamik piyasa seçimi
markets = ["US", "BIST", "CRYPTO"]
market = st.selectbox("Piyasa Seçin", markets)

# Backend’den semboller
backend_url = "http://backend:8000"
symbols = requests.get(f"{backend_url}/symbols", params={"market": market}).json()["symbols"]

symbol = st.selectbox("Sembol Seçin", symbols)
period = st.selectbox("Periyot", ["1mo","3mo","6mo","1y","2y"])

if st.button("Analiz Et"):
    res = requests.get(f"{backend_url}/analyze", params={"symbol": symbol, "market": market, "period": period}).json()

    st.metric("Son Sinyal", res["last_signal"])
    st.metric("Win Rate %", res["winrate"])
    st.metric("Son Tarih", res["last_date"])

    # Equity Curve
    equity = pd.Series(res["equity"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=equity, mode="lines", name="Equity", line=dict(color='blue')))
    st.plotly_chart(fig, use_container_width=True)

    # Screener / Benzer Günler
    st.subheader("Benzer Gün Indexleri (FAISS)")
    st.write(res["similar_days"])

    # AL/SAT overlay (örnek renk)
    st.subheader("Grafik Üzerinde AL/SAT Görselleştirme")
    df = pd.DataFrame(equity, columns=["Equity"])
    df["signal"] = [res["last_signal"]] * len(df)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=df["Equity"], mode="lines", name="Equity", line=dict(color='blue')))
    # AL/SAT işaretleme
    for i, s in enumerate(df["signal"]):
        if s == "AL":
            fig2.add_trace(go.Scatter(x=[i], y=[df["Equity"].iloc[i]], mode="markers", marker=dict(color='green', size=10, symbol="triangle-up"), name="AL"))
        elif s == "SAT":
            fig2.add_trace(go.Scatter(x=[i], y=[df["Equity"].iloc[i]], mode="markers", marker=dict(color='red', size=10, symbol="triangle-down"), name="SAT"))
    st.plotly_chart(fig2, use_container_width=True)
