import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- HELPER: Currency Symbol ---
def get_currency_symbol(ticker):
    ticker = ticker.upper()
    if ticker.endswith(".IS"): return "₺"
    if "=X" in ticker and "EUR" in ticker: return "€"
    return "$"

# --- 1. CONFIG & CSS INJECTION (FIXED) ---
st.set_page_config(
    page_title="VektorQuant Terminal",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        /* Ana Renkler */
        .stApp { background-color: #000000; }
        section[data-testid="stSidebar"] { background-color: #0e1117; border-right: 1px solid #333; }
        
        /* HEADER DÜZELTMESİ: Gizlemek yerine transparan yapıyoruz */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }
        
        /* SIDEBAR TOGGLE BUTONU (Ok İşareti) */
        button[data-testid="stSidebarCollapsedControl"] {
            color: #00CC96 !important; /* Neon Yeşil */
            background-color: #1a1a1a !important; /* Koyu Gri Zemin */
            border: 1px solid #333;
            border-radius: 5px;
            margin-top: 10px;
            margin-left: 10px;
        }
        
        /* Üst boşluk ayarı */
        .block-container { padding-top: 3rem; padding-bottom: 2rem; }
        
        /* Metric Kartları */
        div[data-testid="metric-container"] { 
            background-color: #1a1a1a; 
            border: 1px solid #333; 
            padding: 15px; 
            border-radius: 8px; 
        }
        div[data-testid="metric-container"] label { color: #888 !important; }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #fff !important; }
        
        /* Buton */
        div.stButton > button { 
            background-color: #00CC96; 
            color: black; 
            font-weight: bold; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 5px; 
            width: 100%; 
            transition: all 0.3s;
        }
        div.stButton > button:hover { 
            background-color: #00FFBB; 
            box-shadow: 0 0 10px rgba(0, 255, 187, 0.4);
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. NETWORK CHECK ---
BACKEND_URLS = ["http://backend:8000", "http://localhost:8000"]
if 'backend_url' not in st.session_state:
    found = None
    for url in BACKEND_URLS:
        try:
            if requests.get(f"{url}/markets", timeout=1).status_code == 200:
                found = url
                break
        except: pass
    st.session_state['backend_url'] = found

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("### 🛰️ VQ TERMINAL `v3.0`")
    st.markdown("---")
    
    if st.session_state['backend_url']:
        st.success("SYSTEM ONLINE")
    else:
        st.error("OFFLINE")
        if st.button("Reconnect"): st.rerun()

    # Market & Symbol
    market_list = ["US_TECH_GIANTS"]
    if st.session_state['backend_url']:
        try:
            market_list = requests.get(f"{st.session_state['backend_url']}/markets", timeout=2).json().get("markets", [])
        except: pass
            
    selected_market = st.selectbox("MARKET", market_list)
    
    use_custom = st.toggle("Manual Entry", value=False)
    if use_custom:
        selected_symbol = st.text_input("TICKER", value="AAPL").strip().upper()
    else:
        symbol_list = []
        if st.session_state['backend_url']:
            try:
                res = requests.get(f"{st.session_state['backend_url']}/symbols", params={"market": selected_market}, timeout=2)
                symbol_list = res.json().get("symbols", []) if res.status_code == 200 else ["ERROR"]
            except: symbol_list = ["ERROR"]
        selected_symbol = st.selectbox("ASSET", symbol_list)

    st.markdown("---")
    st.markdown("**⏳ TIME SETTINGS**")
    
    # --- Interval (Mum Aralığı) & Period (Veri Uzunluğu) Mantığı ---
    # Intraday veriler (15m, 1h) sadece kısa periodlarda çalışır.
    
    interval_options = {
        "Daily (1d)": "1d",
        "Weekly (1wk)": "1wk",
        "Monthly (1mo)": "1mo",
        "Hourly (1h)": "1h",
        "15 Minutes (15m)": "15m"
    }
    
    selected_interval_label = st.selectbox("Interval (Candle)", list(interval_options.keys()), index=0)
    selected_interval = interval_options[selected_interval_label]
    
    # Period seçeneklerini interval'e göre filtrele
    if selected_interval in ["15m", "1h"]:
        # Intraday için max 60 gün - 2 yıl arası izin verilir (Yahoo kısıtlaması)
        period_opts = ["1d", "5d", "1mo", "3mo", "6mo", "1y"]
        default_period = "1mo"
        st.caption("ℹ️ Intraday data is limited to recent history.")
    else:
        # Günlük ve üzeri için uzun vadeli
        period_opts = ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"]
        default_period = "1y"

    selected_period = st.select_slider("Range (History)", options=period_opts, value=default_period)

    st.markdown("---")
    run_btn = st.button("EXECUTE ANALYSIS")

# --- 4. MAIN DISPLAY ---
currency = get_currency_symbol(selected_symbol)
header_html = f"""
<div style="display: flex; align-items: baseline; justify-content: space-between;">
    <h1 style='color:#00CC96; margin:0;'>{selected_symbol} <span style='color:#555; font-size:18px;'>// {selected_interval}</span></h1>
    <div style='color:#666; font-family:monospace;'>RANGE: {selected_period}</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

if run_btn and st.session_state['backend_url']:
    try:
        with st.spinner("Processing Quantum Data..."):
            res = requests.get(
                f"{st.session_state['backend_url']}/analyze", 
                params={"symbol": selected_symbol, "period": selected_period, "interval": selected_interval},
                timeout=30
            )
            
            if res.status_code == 200:
                data = res.json()
                metrics = data["metrics"]
                chart = data["chart_data"]
                
                # Metrics
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Close", f"{currency}{data['last_close']}")
                c2.metric("Signal", data['last_signal'])
                c3.metric("Sharpe", metrics.get('sharpe_ratio', 'N/A'))
                c4.metric("Win Rate", f"%{metrics.get('winrate', 0)}")
                
                # Chart
                df_c = pd.DataFrame({
                    'Date': pd.to_datetime(chart['dates']),
                    'Open': chart['open'], 'High': chart['high'], 'Low': chart['low'], 'Close': chart['close'],
                    'BBU': chart['bb_upper'], 'BBL': chart['bb_lower'], 'RSI': chart['rsi'], 'Signal': chart['signals']
                })
                
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.75, 0.25], vertical_spacing=0.03)
                
                # Main Price
                fig.add_trace(go.Candlestick(x=df_c['Date'], open=df_c['Open'], high=df_c['High'], low=df_c['Low'], close=df_c['Close'], name='Price'), row=1, col=1)
                
                if not df_c['BBU'].isnull().all():
                    fig.add_trace(go.Scatter(x=df_c['Date'], y=df_c['BBU'], line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot'), name='BB'), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df_c['Date'], y=df_c['BBL'], line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot'), name='BB', fill='tonexty'), row=1, col=1)
                
                # Signals Overlay
                buys = df_c[df_c['Signal'] == 'BUY']
                sells = df_c[df_c['Signal'] == 'SELL']
                if not buys.empty:
                    fig.add_trace(go.Scatter(x=buys['Date'], y=buys['Low']*0.99, mode='markers', marker=dict(symbol='triangle-up', size=14, color='#00FF7F'), name='BUY'), row=1, col=1)
                if not sells.empty:
                    fig.add_trace(go.Scatter(x=sells['Date'], y=sells['High']*1.01, mode='markers', marker=dict(symbol='triangle-down', size=14, color='#FF4444'), name='SELL'), row=1, col=1)

                # RSI Pane
                fig.add_trace(go.Scatter(x=df_c['Date'], y=df_c['RSI'], line=dict(color='#A020F0', width=2), name='RSI'), row=2, col=1)
                fig.add_hline(y=70, line_dash="dot", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dot", line_color="green", row=2, col=1)
                
                fig.update_layout(
                    template="plotly_dark", height=650, 
                    margin=dict(l=10,r=10,t=10,b=10), 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)', 
                    showlegend=False,
                    xaxis_rangeslider_visible=False
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # AI
                if data['ai_analysis']:
                    st.markdown("### 🧬 Pattern Matching (AI)")
                    cols = st.columns(len(data['ai_analysis']))
                    for i, d in enumerate(data['ai_analysis']):
                        cols[i].markdown(f"<div style='text-align:center; font-size:12px; color:#888;'>{d['date']}<br><b style='font-size:14px; color:{'#0f0' if d['return']>0 else '#f00'}'>%{d['return']}</b></div>", unsafe_allow_html=True)
            
            elif res.status_code == 400:
                st.warning(f"⚠️ {res.json().get('detail')}")
            else:
                st.error(f"Error: {res.status_code}")

    except Exception as e:
        st.error(f"Execution Failed: {e}")