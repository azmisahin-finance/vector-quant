# VektorQuant

📊 **Vector-Based Quantitative Trading Platform**

## Genel Bakış

VektorQuant, hisse senetleri, BIST ve kripto piyasalarını analiz eden, vektör tabanlı sinyaller üreten, equity curve ve backtest raporları sunan profesyonel bir platformdur.

### Özellikler

- Dinamik piyasa ve sembol seçimi
- Candlestick + AL/SAT overlay + RSI + Momentum
- Equity curve ve drawdown görselleştirmesi
- FAISS ile benzer gün analizi
- Screener: Çoklu sembol tarama
- Parametreli backend, frontend ile global kullanım
- Docker ile tek komut çalıştırma

### Mimari

```

VektorQuant
│
├── Data Engine: US, BIST, Crypto
├── Feature Engine: Indicators, Vector Builder
├── Strategy Engine: Rule-based, FAISS
├── Risk Engine: Position sizing, Drawdown
├── Backtest Engine: Equity curve, Winrate
└── UI: Streamlit Dashboard

````

### Kurulum

```bash
git clone <repo-url>
cd VektorQuant
docker-compose up --build
````

* Backend: [http://localhost:8000/docs](http://localhost:8000/docs)
* Frontend: [http://localhost:8501](http://localhost:8501)

### Geliştirme

* Yeni indikatör eklemek: `backend/app/features.py`
* Yeni sinyal kuralı: `backend/app/signals.py`
* Ek veri kaynağı: `backend/app/data_sources.py`
* UI iyileştirmeleri: `frontend/app.py`

````

---
