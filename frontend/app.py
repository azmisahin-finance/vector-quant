import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- HELPER FUNCTIONS ---
def get_currency_symbol(ticker):
    """
    Sembole göre para birimi simgesi belirler.
    """
    ticker = ticker.upper()
    if ticker.endswith(".IS"):
        return "₺"
    if "=X" in ticker and "EUR" in ticker and "USD" not in ticker:
        return "€"
    if "BTC" in ticker or "ETH" in ticker or "-USD" in ticker:
        return "$"
    # Default
    return "$"

# --- 1. CONFIG & STYLE ---
st.set_page_config(
    page_title="VektorQuant Terminal",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .stApp { background-color: #000000; }
        section[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #333; }
        header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
        .block-container { padding-top: 1rem; padding-bottom: 0rem; }
        div[data-testid="metric-container"] { background-color: #1a1a1a; border: 1px solid #333; padding: 15px; border-radius: 8px; }
        div[data-testid="metric-container"] label { color: #888 !important; }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #fff !important; }
        div.stButton > button { background-color: #00CC96; color: black; font-weight: bold; border: none; padding: 10px 20px; border-radius: 5px; width: 100%; }
        div.stButton > button:hover { background-color: #00FFBB; }
        .stAlert { background-color: #220000; border: 1px solid #550000; color: #ffaaaa; }
    </style>
""", unsafe_allow_html=True)

# --- 2. NETWORK ---
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

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🛰️ VQ TERMINAL `v2.6`")
    st.markdown("---")
    
    if st.session_state['backend_url']:
        st.success("SYSTEM ONLINE")
    else:
        st.error("OFFLINE")
        if st.button("Reconnect"): st.rerun()

    # Market Logic
    market_list = ["US_TECH_GIANTS"]
    if st.session_state['backend_url']:
        try:
            market_list = requests.get(f"{st.session_state['backend_url']}/markets", timeout=2).json().get("markets", [])
        except: pass
            
    selected_market = st.selectbox("MARKET", market_list)
    
    # Custom Symbol Logic
    use_custom = st.toggle("Manual Entry Mode", value=False)
    
    if use_custom:
        selected_symbol = st.text_input("ENTER TICKER", value="AAPL", help="Examples: TSLA, THYAO.IS, BTC-USD").strip().upper()
    else:
        symbol_list = []
        if st.session_state['backend_url']:
            try:
                res = requests.get(f"{st.session_state['backend_url']}/symbols", params={"market": selected_market}, timeout=2)
                if res.status_code == 200:
                    symbol_list = res.json().get("symbols", [])
                else:
                    symbol_list = ["ERROR"]
            except: symbol_list = ["ERROR"]
        selected_symbol = st.selectbox("INSTRUMENT", symbol_list)

    st.markdown("---")
    # Periyot seçenekleri
    selected_period = st.select_slider("PERIOD", options=["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"], value="1y")
    st.markdown("---")
    run_btn = st.button("EXECUTE ANALYSIS")

# --- 4. MAIN DASHBOARD ---
currency_symbol = get_currency_symbol(selected_symbol)
st.markdown(f"<h2 style='color:#00CC96; margin:0;'>{selected_symbol} <span style='color:#555; font-size:16px;'>// {selected_market if not use_custom else 'CUSTOM'}</span></h2>", unsafe_allow_html=True)

if run_btn and st.session_state['backend_url']:
    try:
        with st.spinner(f"Processing Data Blocks [{selected_period}]..."):
            res = requests.get(
                f"{st.session_state['backend_url']}/analyze", 
                params={"symbol": selected_symbol, "period": selected_period},
                timeout=25
            )
            
            if res.status_code == 200:
                data = res.json()
                metrics = data["metrics"]
                chart = data["chart_data"]
                
                # --- METRICS ROW ---
                c1, c2, c3, c4 = st.columns(4)
                
                # Dinamik Para Birimi Kullanımı
                c1.metric("Last Price", f"{currency_symbol}{data['last_close']}")
                
                # Sinyal Renklendirme
                sig = data['last_signal']
                sig_color = "normal" 
                if sig == "BUY": sig_color = "normal" # Streamlit doesn't allow green text easily in metric without hacks
                c2.metric("Signal", sig)
                
                c3.metric("Sharpe", metrics.get('sharpe_ratio', 'N/A'))
                
                # Winrate Format
                wr = metrics.get('winrate', 0)
                c4.metric("Win Rate", f"%{wr}")
                
                # --- CHART ROW ---
                df_c = pd.DataFrame({
                    'Date': pd.to_datetime(chart['dates']),
                    'Open': chart['open'], 'High': chart['high'], 'Low': chart['low'], 'Close': chart['close'],
                    'BBU': chart['bb_upper'], 'BBL': chart['bb_lower'], 'RSI': chart['rsi'], 'Signal': chart['signals']
                })
                
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.05)
                
                # Candlestick
                fig.add_trace(go.Candlestick(x=df_c['Date'], open=df_c['Open'], high=df_c['High'], low=df_c['Low'], close=df_c['Close'], name='Price'), row=1, col=1)
                
                # BB (Sadece veri varsa çiz)
                if not df_c['BBU'].isnull().all():
                    fig.add_trace(go.Scatter(x=df_c['Date'], y=df_c['BBU'], line=dict(color='gray', width=1, dash='dot'), name='BB'), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df_c['Date'], y=df_c['BBL'], line=dict(color='gray', width=1, dash='dot'), name='BB', fill='tonexty'), row=1, col=1)
                
                # Signals
                buys = df_c[df_c['Signal'] == 'BUY']
                sells = df_c[df_c['Signal'] == 'SELL']
                if not buys.empty:
                    fig.add_trace(go.Scatter(x=buys['Date'], y=buys['Low']*0.99, mode='markers', marker=dict(symbol='triangle-up', size=12, color='#00FF7F'), name='BUY'), row=1, col=1)
                if not sells.empty:
                    fig.add_trace(go.Scatter(x=sells['Date'], y=sells['High']*1.01, mode='markers', marker=dict(symbol='triangle-down', size=12, color='#FF4444'), name='SELL'), row=1, col=1)

                # RSI
                fig.add_trace(go.Scatter(x=df_c['Date'], y=df_c['RSI'], line=dict(color='#A020F0'), name='RSI'), row=2, col=1)
                fig.add_hline(y=70, line_dash="dot", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dot", line_color="green", row=2, col=1)
                
                fig.update_layout(template="plotly_dark", height=600, margin=dict(l=0,r=0,t=20,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # --- AI ANALYSIS ---
                if data['ai_analysis']:
                    st.write("### 🧬 Historical Similarity")
                    cols = st.columns(len(data['ai_analysis']))
                    for i, d in enumerate(data['ai_analysis']):
                        ret_val = d['return']
                        color_hex = "#00FF7F" if ret_val > 0 else "#FF4444"
                        cols[i].markdown(f"""
                        <div style="border:1px solid #333; border-radius:5px; text-align:center; padding:5px;">
                            <div style="color:#888; font-size:11px;">{d['date']}</div>
                            <div style="color:{color_hex}; font-size:16px; font-weight:bold;">%{ret_val}</div>
                        </div>
                        """, unsafe_allow_html=True)
            elif res.status_code == 400:
                st.warning(f"⚠️ {res.json().get('detail', 'Insufficient Data')}")
            else:
                st.error(f"Server Error: {res.status_code}")
    except Exception as e:
        st.error(f"System Error: {str(e)}")