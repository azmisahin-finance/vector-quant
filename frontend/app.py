import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# --- 1. SAYFA KONFIGURASYONU (EN BAŞTA OLMALI) ---
st.set_page_config(
    page_title="VektorQuant Terminal",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded"
)

# --- 2. CSS INJECTION (HACKING THE UI) ---
# Beyaz barları, gereksiz boşlukları ve "Deploy" butonunu yok eder.
st.markdown("""
    <style>
        /* Ana Arka Plan */
        .stApp {
            background-color: #000000;
        }
        
        /* Sidebar Arka Plan */
        section[data-testid="stSidebar"] {
            background-color: #111111;
            border-right: 1px solid #333;
        }
        
        /* Streamlit Header'ı Gizle (En önemli kısım) */
        header[data-testid="stHeader"] {
            visibility: hidden;
            height: 0px;
        }
        
        /* Üst boşluğu yok et */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        
        /* Footer'ı Gizle */
        footer {
            visibility: hidden;
        }
        
        /* Metrik Kartları */
        div[data-testid="metric-container"] {
            background-color: #1a1a1a;
            border: 1px solid #333;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        div[data-testid="metric-container"] label {
            color: #888 !important;
        }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #fff !important;
        }
        
        /* Buton Stili */
        div.stButton > button {
            background-color: #00CC96;
            color: black;
            font-weight: bold;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #00FFBB;
            box-shadow: 0 0 10px #00CC96;
        }
        
        /* Hata Kutuları */
        .stAlert {
            background-color: #330000;
            border: 1px solid #ff0000;
            color: #ffcccc;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. BACKEND BAĞLANTISI ---
# Docker içinde "backend", localde "localhost"
BACKEND_URLS = ["http://backend:8000", "http://localhost:8000"]

def check_connection():
    """Backend'i bulana kadar URL'leri dener."""
    for url in BACKEND_URLS:
        try:
            r = requests.get(f"{url}/markets", timeout=2)
            if r.status_code == 200:
                return url
        except:
            continue
    return None

# Session State Init
if 'backend_url' not in st.session_state:
    with st.spinner("Sistem Başlatılıyor & Backend Aranıyor..."):
        found_url = check_connection()
        if found_url:
            st.session_state['backend_url'] = found_url
        else:
            st.session_state['backend_url'] = None

# --- 4. SIDEBAR (COMMAND CENTER) ---
with st.sidebar:
    st.markdown("### 🛰️ VQ TERMINAL `v2.4`")
    st.markdown("---")
    
    # Connection Status Indicator
    if st.session_state['backend_url']:
        st.success(f"LINK ESTABLISHED")
    else:
        st.error("OFFLINE - RETRYING...")
        if st.button("Reconnect"):
            st.rerun()
    
    # Market Seçimi
    market_list = ["US"] # Default fallback
    if st.session_state['backend_url']:
        try:
            res = requests.get(f"{st.session_state['backend_url']}/markets", timeout=3).json()
            market_list = res.get("markets", ["US"])
        except:
            pass
            
    selected_market = st.selectbox("MARKET ACCESS", market_list)
    
    # Sembol Seçimi
    symbol_list = []
    if st.session_state['backend_url']:
        try:
            res = requests.get(f"{st.session_state['backend_url']}/symbols", params={"market": selected_market}, timeout=3).json()
            symbol_list = res.get("symbols", [])
        except:
            symbol_list = ["HATA"]
            
    selected_symbol = st.selectbox("INSTRUMENT", symbol_list)
    
    # Periyot
    st.markdown("---")
    selected_period = st.select_slider("TIME HORIZON", options=["1mo", "3mo", "6mo", "1y", "2y", "5y"], value="1y")
    
    # Action Button
    st.markdown("---")
    run_analysis = st.button("RUN ALGORITHM", use_container_width=True)

# --- 5. ANA EKRAN (DASHBOARD) ---

# Başlık yerine Custom Header
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
    <h1 style='margin:0; font-size: 24px; color: #00CC96;'>{selected_symbol if selected_symbol else 'NO DATA'} <span style='color: #666; font-size: 16px;'>// {selected_market}</span></h1>
    <div style='text-align: right; color: #888; font-size: 12px;'>INSTITUTIONAL GRADE ANALYTICS<br>POWERED BY OMNISCIENT ARCHITECT</div>
</div>
""", unsafe_allow_html=True)

if not st.session_state['backend_url']:
    st.warning("⚠️ Backend servisine ulaşılamıyor. Lütfen Docker konteynerlarının çalıştığından emin olun.")
    st.code("docker-compose ps", language="bash")
    st.stop()

if run_analysis:
    try:
        with st.status("Processing Data Blocks...", expanded=True) as status:
            status.write("Fetching OHLCV Data...")
            # Analiz İsteği
            res = requests.get(
                f"{st.session_state['backend_url']}/analyze", 
                params={"symbol": selected_symbol, "market": selected_market, "period": selected_period},
                timeout=20
            )
            
            if res.status_code != 200:
                status.update(label="Analysis Failed!", state="error")
                st.error(f"Server Error: {res.text}")
            else:
                data = res.json()
                status.update(label="Calculation Complete", state="complete")
                
                # --- VERİ HAZIRLIĞI ---
                metrics = data["metrics"]
                chart = data["chart_data"]
                
                # --- KPI ROW ---
                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Current Price", f"${data['last_close']}", delta_color="off")
                
                signal = data['last_signal']
                k2.metric("AI Recommendation", signal, delta=None)
                
                sharpe = metrics.get('sharpe_ratio', 0)
                k3.metric("Risk (Sharpe)", sharpe, delta_color="normal" if sharpe > 1 else "inverse")
                
                winrate = metrics.get('winrate', 0)
                k4.metric("Win Rate", f"%{winrate}")
                
                # --- ADVANCED CHART ---
                df_c = pd.DataFrame({
                    'Date': pd.to_datetime(chart['dates']),
                    'Open': chart['open'], 'High': chart['high'], 'Low': chart['low'], 'Close': chart['close'],
                    'Volume': chart['volume'], 'RSI': chart['rsi'], 
                    'BBU': chart['bb_upper'], 'BBL': chart['bb_lower'],
                    'Signal': chart['signals']
                })
                
                # Plotly Chart
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.7, 0.3])
                
                # 1. Fiyat & Bollinger
                fig.add_trace(go.Candlestick(x=df_c['Date'], open=df_c['Open'], high=df_c['High'], low=df_c['Low'], close=df_c['Close'], name='Price'), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_c['Date'], y=df_c['BBU'], line=dict(color='rgba(255, 255, 255, 0.3)', width=1), name='Upper BB'), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_c['Date'], y=df_c['BBL'], line=dict(color='rgba(255, 255, 255, 0.3)', width=1), name='Lower BB', fill='tonexty'), row=1, col=1)
                
                # Sinyaller
                buys = df_c[df_c['Signal'] == 'BUY']
                sells = df_c[df_c['Signal'] == 'SELL']
                fig.add_trace(go.Scatter(x=buys['Date'], y=buys['Low']*0.99, mode='markers', marker=dict(symbol='triangle-up', size=12, color='#00FF7F'), name='BUY'), row=1, col=1)
                fig.add_trace(go.Scatter(x=sells['Date'], y=sells['High']*1.01, mode='markers', marker=dict(symbol='triangle-down', size=12, color='#FF4444'), name='SELL'), row=1, col=1)
                
                # 2. RSI
                fig.add_trace(go.Scatter(x=df_c['Date'], y=df_c['RSI'], line=dict(color='#A020F0'), name='RSI'), row=2, col=1)
                fig.add_hline(y=70, line_dash="dot", row=2, col=1, line_color="red")
                fig.add_hline(y=30, line_dash="dot", row=2, col=1, line_color="green")
                
                fig.update_layout(
                    height=600, 
                    template="plotly_dark", 
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=30, b=0),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # --- AI SIMILARITY ---
                st.markdown("### 🧬 Vector Similarity Analysis")
                if data['ai_analysis']:
                    cols = st.columns(len(data['ai_analysis']))
                    for i, day in enumerate(data['ai_analysis']):
                        with cols[i]:
                            ret = day['return']
                            color = "#00FF7F" if ret > 0 else "#FF4444"
                            st.markdown(f"""
                            <div style="border:1px solid #333; padding:10px; border-radius:5px; text-align:center;">
                                <div style="font-size:12px; color:#888;">{day['date']}</div>
                                <div style="font-size:18px; color:{color}; font-weight:bold;">%{ret}</div>
                            </div>
                            """, unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:
        st.error("🚨 Critical Error: Backend connection lost during analysis.")
    except Exception as e:
        st.error(f"🚨 System Error: {str(e)}")

else:
    # Landing Screen
    st.info("👈 Select market and instrument from the Command Center to begin.")