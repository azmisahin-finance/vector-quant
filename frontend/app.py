import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="VektorQuant Dashboard", layout="wide")
st.title("📊 VektorQuant Dashboard")

backend_url = "http://backend:8000"

# Market selection
markets = ["US","BIST","CRYPTO"]
market = st.selectbox("Piyasa Seçin", markets)

# Symbols dynamically from backend
try:
    symbols = requests.get(f"{backend_url}/symbols", params={"market":market}, timeout=5).json().get("symbols",[])
except:
    symbols = []
    st.error("Sembol listesi yüklenemedi")

symbol = st.selectbox("Sembol Seçin", symbols)
period = st.selectbox("Periyot", ["1mo","3mo","6mo","1y","2y"])

if st.button("Analiz Et"):
    try:
        res = requests.get(f"{backend_url}/analyze", params={"symbol":symbol,"market":market,"period":period}, timeout=10).json()
        if "error" in res:
            st.error(f"Backend hatası: {res['error']}")
        else:
            st.metric("Son Sinyal", res["last_signal"])
            st.metric("Win Rate %", res["winrate"])
            st.metric("Son Tarih", res["last_date"])

            # Equity Curve
            equity = pd.Series(res["equity"])
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=equity, mode="lines", name="Equity", line=dict(color='blue')))
            st.plotly_chart(fig, use_container_width=True)

            # Candlestick + Buy/Sell overlay
            st.subheader("Candlestick ve Buy/Sell Overlay")
            df_candle = equity.reset_index()
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(y=df_candle["equity"], mode="lines", name="Equity", line=dict(color='blue')))
            for i,s in enumerate([res["last_signal"]]*len(df_candle)):
                if s=="BUY":
                    fig2.add_trace(go.Scatter(x=[i], y=[df_candle["equity"].iloc[i]], mode="markers",
                        marker=dict(color='green', size=10, symbol="triangle-up"), name="BUY"))
                elif s=="SELL":
                    fig2.add_trace(go.Scatter(x=[i], y=[df_candle["equity"].iloc[i]], mode="markers",
                        marker=dict(color='red', size=10, symbol="triangle-down"), name="SELL"))
            st.plotly_chart(fig2, use_container_width=True)

            # FAISS Benzer Günler
            st.subheader("Benzer Gün Indexleri (FAISS)")
            st.write(res["similar_days"])

    except Exception as e:
        st.error(f"Analiz sırasında hata oluştu: {e}")
