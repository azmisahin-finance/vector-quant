# Bu dosya statik sembol listelerini içerir.
# yfinance screener API'si olmadığı için majör endeksleri buraya tanımlıyoruz.

MARKET_INDICES = {

    "US_TECH_GIANTS": [
        # =========================
        # 🚀 BUYUME / BIG TECH
        # =========================
        "AAPL", "MSFT", "GOOGL", "AMZN", "META",

        # =========================
        # 🤖 AI / YUKSEK BUYUME
        # =========================
        "NVDA", "AMD",

        # =========================
        # ⚡ HIGH BETA / VOLATIL
        # =========================
        "TSLA",

        # =========================
        # 📺 DIJITAL / ICERIK
        # =========================
        "NFLX",

        # =========================
        # 💳 FINTECH / ODEME
        # =========================
        "PYPL",

        # =========================
        # 🚕 PLATFORM EKONOMISI
        # =========================
        "UBER",

        # =========================
        # 🏢 KURUMSAL / YAZILIM
        # =========================
        "CRM", "ADBE", "ORCL",

        # =========================
        # 🧱 YARI ILETKEN / DONANIM
        # =========================
        "INTC", "QCOM", "TXN", "AVGO", "CSCO",

        # =========================
        # 🏛️ LEGACY TECH
        # =========================
        "IBM"
    ],

    "US_DOW30": [
        # =========================
        # 🏦 FINANS
        # =========================
        "JPM", "GS", "AXP", "TRV", "V",

        # =========================
        # 💊 SAGLIK / DEFANSIF
        # =========================
        "JNJ", "MRK", "UNH", "AMGN",

        # =========================
        # 🛒 TUKETIM / DEFANSIF
        # =========================
        "KO", "PG", "WMT", "MCD",

        # =========================
        # 🛍️ MARKA / PERAKENDE
        # =========================
        "NKE", "HD",

        # =========================
        # ⚙️ SANAYI / URETIM
        # =========================
        "CAT", "HON", "MMM",

        # =========================
        # ✈️ HAVACILIK / SAVUNMA
        # =========================
        "BA",

        # =========================
        # 🛢️ ENERJI
        # =========================
        "CVX",

        # =========================
        # 📡 TELEKOM
        # =========================
        "VZ",

        # =========================
        # 💻 TEKNOLOJI
        # =========================
        "AAPL", "MSFT", "CRM", "IBM", "INTC", "CSCO",

        # =========================
        # 🎬 MEDYA / EGLENCE
        # =========================
        "DIS",

        # =========================
        # 🧪 KIMYA / MALZEME
        # =========================
        "DOW"
    ],

    "BIST_100_SELECT": [
        # =========================
        # ✈️ BUYUME / GLOBAL GELIR
        # =========================
        "THYAO.IS", "PGSUS.IS", "TAVHL.IS",
        "FROTO.IS", "TOASO.IS",
        "EREGL.IS",

        # =========================
        # 🏦 FAIZ / FINANS
        # =========================
        "GARAN.IS", "AKBNK.IS", "ISCTR.IS", "YKBNK.IS", "VAKBN.IS", "HALKB.IS",

        # =========================
        # ⚡ ENERJI / EMTIA
        # =========================
        "TUPRS.IS", "PETKM.IS", "GUBRF.IS", "ODAS.IS",

        # =========================
        # 🛒 DEFANSIF / IC TUKETIM
        # =========================
        "BIMAS.IS", "MGROS.IS", "SOKM.IS",

        # =========================
        # 📡 TELEKOM / NAKIT AKISI
        # =========================
        "TCELL.IS", "TTKOM.IS",

        # =========================
        # 🏗️ HOLDING
        # =========================
        "KCHOL.IS", "SAHOL.IS", "ALARK.IS", "DOHOL.IS",

        # =========================
        # 🧪 SANAYI / KIMYA
        # =========================
        "SASA.IS", "HEKTS.IS", "SISE.IS",

        # --- OTOMOTIV YAN SANAYI ---
        # # min hacim filtresiiyle eklenebilir
        "BALAT.IS",        

        # =========================
        # 🛡️ SAVUNMA / TEKNOLOJI
        # =========================
        "ASELS.IS",

        # =========================
        # 🏠 GAYRIMENKUL
        # =========================
        "EKGYO.IS",

        # =========================
        # 🏗️ ALTYAPI
        # =========================
        "ENKAI.IS",

        # =========================
        # 🥇 ALTIN / HEDGE
        # =========================
        "KOZAL.IS",

        # =========================
        # 🏭 CIMENTO
        # =========================
        "OYAKC.IS",

        # =========================
        # 🏠 DAYANIKLI TUKETIM
        # =========================
        "ARCLK.IS"
    ],

    "CRYPTO_TOP_50": [
        # =========================
        # 🥇 STORE OF VALUE
        # =========================
        "BTC-USD",

        # =========================
        # 🧠 SMART CONTRACT / L1
        # =========================
        "ETH-USD", "SOL-USD", "ADA-USD", "AVAX-USD", "DOT-USD", "NEAR-USD", "APT-USD",

        # =========================
        # 💸 PAYMENT / TRANSFER
        # =========================
        "XRP-USD", "XLM-USD", "TRX-USD",

        # =========================
        # 🐶 MEME / HIGH RISK
        # =========================
        "DOGE-USD", "SHIB-USD",

        # =========================
        # 🏗️ DEFI
        # =========================
        "UNI-USD", "AAVE-USD",

        # =========================
        # 🔗 ORACLE / INFRA
        # =========================
        "LINK-USD",

        # =========================
        # 🧩 ECOSYSTEM / PLATFORM
        # =========================
        "BNB-USD",

        # =========================
        # ⛏️ STORE / PRIVACY
        # =========================
        "XMR-USD",

        # =========================
        # ⚙️ DIGER ALTCOINLER
        # =========================
        "MATIC-USD", "LTC-USD", "BCH-USD", "ETC-USD", "FIL-USD", "ICP-USD",
        "HBAR-USD", "VET-USD", "QNT-USD", "ALGO-USD", "GRT-USD", "FTM-USD",
        "EOS-USD", "SAND-USD", "EGLD-USD", "MANA-USD"
    ],

    "FOREX_MAJORS": [
        # =========================
        # 💵 MAJOR PARITELER
        # =========================
        "EURUSD=X", "GBPUSD=X", "AUDUSD=X", "NZDUSD=X",

        # =========================
        # 💴 YEN CROSS
        # =========================
        "JPY=X", "EURJPY=X", "GBPJPY=X",

        # =========================
        # 🔄 CROSS PARITELER
        # =========================
        "EURGBP=X", "EURCAD=X",

        # =========================
        # 🌏 GELISEN PIYASA
        # =========================
        "USDTRY=X", "EURTRY=X", "USDCNY=X"
    ],

    "COMMODITIES": [
        # =========================
        # 🥇 DEGERLI METAL
        # =========================
        "GC=F", "SI=F",

        # =========================
        # 🛢️ ENERJI
        # =========================
        "CL=F", "NG=F",

        # =========================
        # 🏭 SANAYI METAL
        # =========================
        "HG=F",

        # =========================
        # 🌾 TARIM
        # =========================
        "KC=F", "CC=F", "ZS=F", "ZC=F"
    ]
}