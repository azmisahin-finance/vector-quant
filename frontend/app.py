import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIG & STYLES ---
st.set_page_config(
    page_title="VektorQuant Pro Terminal",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Terminal" Look
st.markdown("""
<style>
    /* Main Background color to dark grey usually handled by theme, but forcing specific elements */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Remove top padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Metric Cards Styling */
    div[data-testid="metric-container"] {
        background-color: #1c1f26;
        border: 1px solid #2d3139;
        padding: 10px;
        border-radius: 5px;
        color: #e0e0e0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #161920;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Table styling */
    thead tr th:first-child {display:none}
    tbody th {display:none}
</style>
""", unsafe_allow_html=True)

# --- 2. BACKEND CONNECTION ---
BACKEND_URL = "http://backend:8000"

def get_data(endpoint, params=None):
    try:
        r = requests.get(f"{BACKEND_URL}/{endpoint}", params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("## 📟 COMMAND CENTER")
    
    # Market & Asset Selection
    markets_data = get_data("markets")
    market_list = markets_data["markets"] if markets_data else ["US"]
    
    selected_market = st.selectbox("MARKET", market_list, index=0)
    
    symbols_data = get_data("symbols", {"market": selected_market})
    symbol_list = symbols_data["symbols"] if symbols_data else ["AAPL"]
    
    selected_symbol = st.selectbox("ASSET", symbol_list)
    selected_period = st.select_slider("TIMEFRAME", options=["1mo", "3mo", "6mo", "1y", "2y", "5y"], value="1y")
    
    st.markdown("---")
    st.markdown("### ⚙️ STRATEGY PARAMS")
    rsi_threshold = st.slider("RSI Overbought", 60, 90, 70)
    stop_loss = st.number_input("Stop Loss %", value=2.0)
    
    run_btn = st.button("🚀 EXECUTE ANALYSIS", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.info("System Status: ONLINE 🟢")

# --- 4. MAIN DASHBOARD ---

if run_btn:
    with st.spinner(f"Fetching Institutional Data for {selected_symbol}..."):
        data = get_data("analyze", {"symbol": selected_symbol, "market": selected_market, "period": selected_period})
        
    if not data or "error" in data:
        st.error("Data Fetch Failed. Check Backend Connection.")
    else:
        meta = data["meta"]
        metrics = data["metrics"]
        ai_data = data["ai_analysis"]
        chart = data["chart_data"]
        
        # --- ROW 1: KPI CARDS ---
        c1, c2, c3, c4, c5 = st.columns(5)
        
        with c1:
            st.metric("Last Price", f"${data['last_close']}", delta=None)
        with c2:
            signal_color = "normal"
            if data['last_signal'] == "BUY": signal_color = "off" # Streamlit doesn't support green text natively in metric delta easily without hack, keeping simple
            st.metric("AI Signal", data['last_signal'])
        with c3:
            st.metric("Win Rate", f"{metrics['winrate']}%")
        with c4:
            st.metric("Sharpe Ratio", metrics['sharpe_ratio'])
        with c5:
            st.metric("Max Drawdown", f"{metrics['max_drawdown']}%")

        # --- ROW 2: ADVANCED CHARTING (THE "TRADINGVIEW" PART) ---
        
        # Prepare Dataframe for Plotly
        df_chart = pd.DataFrame({
            "Date": pd.to_datetime(chart["dates"]),
            "Open": chart["open"], "High": chart["high"], "Low": chart["low"], "Close": chart["close"],
            "Volume": chart["volume"], "RSI": chart["rsi"],
            "BBU": chart["bb_upper"], "BBL": chart["bb_lower"],
            "Signal": chart["signals"]
        })
        
        # Create Subplots: Row 1 = Price/BB, Row 2 = Volume, Row 3 = RSI
        fig = make_subplots(
            rows=3, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.03, 
            row_heights=[0.6, 0.2, 0.2],
            specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]]
        )

        # 1. Candlestick
        fig.add_trace(go.Candlestick(
            x=df_chart['Date'], open=df_chart['Open'], high=df_chart['High'], low=df_chart['Low'], close=df_chart['Close'],
            name='OHLC'
        ), row=1, col=1)

        # 2. Bollinger Bands
        fig.add_trace(go.Scatter(x=df_chart['Date'], y=df_chart['BBU'], line=dict(color='gray', width=1, dash='dot'), name='BB Upper'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df_chart['Date'], y=df_chart['BBL'], line=dict(color='gray', width=1, dash='dot'), name='BB Lower', fill='tonexty'), row=1, col=1)

        # 3. Buy/Sell Markers
        buys = df_chart[df_chart["Signal"] == "BUY"]
        sells = df_chart[df_chart["Signal"] == "SELL"]
        
        fig.add_trace(go.Scatter(
            x=buys['Date'], y=buys['Low']*0.98, mode='markers', 
            marker=dict(symbol='triangle-up', size=12, color='#00ff00'), name='BUY SIGNAL'
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=sells['Date'], y=sells['High']*1.02, mode='markers', 
            marker=dict(symbol='triangle-down', size=12, color='#ff0000'), name='SELL SIGNAL'
        ), row=1, col=1)

        # 4. Volume
        fig.add_trace(go.Bar(x=df_chart['Date'], y=df_chart['Volume'], marker_color='teal', name='Volume'), row=2, col=1)

        # 5. RSI
        fig.add_trace(go.Scatter(x=df_chart['Date'], y=df_chart['RSI'], line=dict(color='purple', width=2), name='RSI'), row=3, col=1)
        # RSI Levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

        # Layout Tuning
        fig.update_layout(
            template="plotly_dark",
            height=700,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_rangeslider_visible=False,
            paper_bgcolor="#161920",
            plot_bgcolor="#161920",
            legend=dict(orientation="h", y=1.02, x=0.01)
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # --- ROW 3: DETAILED ANALYSIS & AI ---
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.markdown("### 📉 Equity Curve Simulation")
            equity_data = metrics["equity"]
            # Normalize equity date length to chart date length for plotting (simplification)
            if len(equity_data) != len(df_chart):
                equity_data = equity_data[-len(df_chart):]
            
            fig_eq = go.Figure()
            fig_eq.add_trace(go.Scatter(x=df_chart['Date'], y=equity_data, fill='tozeroy', line=dict(color='#00CC96'), name="Portfolio Value"))
            fig_eq.update_layout(template="plotly_dark", height=300, paper_bgcolor="#161920", plot_bgcolor="#161920", margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig_eq, use_container_width=True)

        with col_right:
            st.markdown("### 🤖 Vector-AI Similar Days")
            st.markdown("The AI engine found historical market conditions similar to today:")
            
            if ai_data:
                ai_df = pd.DataFrame(ai_data)
                
                # Custom styling for dataframe
                st.dataframe(
                    ai_df.style.format({"return": "{:.2f}%"}).applymap(
                        lambda x: 'color: #00ff00' if isinstance(x, float) and x > 0 else 'color: #ff0000', 
                        subset=['return']
                    ),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.write("No sufficient data for vector analysis.")

else:
    # Landing Page State
    st.markdown("<div style='text-align: center; margin-top: 100px;'>", unsafe_allow_html=True)
    st.title("VEKTOR QUANT PRO")
    st.markdown("### Institutional Grade Quantitative Analytics")
    st.markdown("Select a market and asset from the sidebar to begin.")
    st.markdown("</div>", unsafe_allow_html=True)