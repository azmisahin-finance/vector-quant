# Bu dosya statik sembol listelerini içerir.
# yfinance screener API'si olmadığı için majör endeksleri buraya tanımlıyoruz.

MARKET_INDICES = {
    "US_TECH_GIANTS": [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "NFLX", "AMD", "INTC", 
        "IBM", "ORCL", "CRM", "ADBE", "CSCO", "QCOM", "TXN", "AVGO", "PYPL", "UBER"
    ],
    "US_DOW30": [
        "MMM", "AXP", "AMGN", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "DOW",
        "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE",
        "PG", "CRM", "TRV", "UNH", "VZ", "V", "WMT", "WBA"
    ],
    "BIST_100_SELECT": [
        "THYAO.IS", "ASELS.IS", "KCHOL.IS", "GARAN.IS", "AKBNK.IS", "ISCTR.IS", "YKBNK.IS",
        "SISE.IS", "BIMAS.IS", "TUPRS.IS", "EREGL.IS", "FROTO.IS", "SAHOL.IS", "PETKM.IS",
        "TCELL.IS", "TTKOM.IS", "ARCLK.IS", "ENKAI.IS", "TOASO.IS", "PGSUS.IS", "KOZAL.IS",
        "KRDMD.IS", "SASA.IS", "HEKTS.IS", "ODAS.IS", "EKGYO.IS", "VAKBN.IS", "HALKB.IS",
        "MGROS.IS", "ALARK.IS", "TAVHL.IS", "GUBRF.IS", "OYAKC.IS", "DOHOL.IS", "SOKM.IS"
    ],
    "CRYPTO_TOP_50": [
        "BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "SOL-USD", "ADA-USD", "DOGE-USD",
        "TRX-USD", "AVAX-USD", "DOT-USD", "MATIC-USD", "LTC-USD", "SHIB-USD", "BCH-USD",
        "LINK-USD", "XLM-USD", "ATOM-USD", "UNI-USD", "XMR-USD", "ETC-USD", "FIL-USD",
        "ICP-USD", "HBAR-USD", "APT-USD", "VET-USD", "NEAR-USD", "QNT-USD", "AAVE-USD",
        "ALGO-USD", "GRT-USD", "FTM-USD", "EOS-USD", "SAND-USD", "EGLD-USD", "MANA-USD"
    ],
    "FOREX_MAJORS": [
        "EURUSD=X", "JPY=X", "GBPUSD=X", "AUDUSD=X", "NZDUSD=X", "EURJPY=X", 
        "GBPJPY=X", "EURGBP=X", "EURCAD=X", "USDCNY=X", "USDTRY=X", "EURTRY=X"
    ],
    "COMMODITIES": [
        "GC=F", "SI=F", "CL=F", "NG=F", "HG=F", "KC=F", "CC=F", "ZS=F", "ZC=F"
    ]
}