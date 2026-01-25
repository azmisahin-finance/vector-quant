import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="VektorQuant Dashboard", layout="wide")
st.title("📊 VektorQuant Dashboard")

symbol = st.text_input("Sembol", "AAPL")
market = st.selectbox("Piyasa", ["US", "BIST", "Crypto"])

if st.button("Analiz Et"):
    res = requests.get("http://backend:8000/analyze", params={"symbol": symbol, "market": market}).json()

    st.metric("Son Sinyal", res["last_signal"])
    st.metric("Win Rate %", res["winrate"])

    # Equity Curve
    equity = pd.Series(res["equity"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=equity, mode="lines", name="Equity"))
    st.plotly_chart(fig, use_container_width=True)

    # Benzer Günler
    st.subheader("Benzer Gün Indexleri")
    st.write(res["similar_days"])
