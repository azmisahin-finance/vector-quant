# VektorQuant

📈 **Vector-Based Quantitative Trading Platform**

## Genel Bakış

VektorQuant, hisse senetleri, BIST ve kripto piyasalarını analiz eden, vektör tabanlı sinyaller üreten, equity curve ve backtest raporları sunan interaktif bir platformdur.

## Özellikler

- Çoklu piyasa desteği: ABD, BIST, Kripto
- Candlestick + AL/SAT overlay + RSI
- Equity curve ve drawdown görselleştirmesi
- Vektör benzer gün analizi (FAISS)
- Docker ile tek komut çalıştırma
- Özelleştirilebilir parametreler

## Mimari

```

VektorQuant
│
├── Data Engine: US Stocks, BIST, Crypto
├── Feature Engine: Indicators, Vector Builder
├── Strategy Engine: Rule-based, FAISS
├── Risk Engine: Position sizing, Drawdown
├── Backtest Engine: Equity curve, Winrate
└── UI: Streamlit Dashboard

````

## Kurulum

```bash
git clone <repo-url>
cd vektor-quant-platform
docker-compose up --build
````

* Backend: [http://localhost:8000/docs](http://localhost:8000/docs)
* Frontend: [http://localhost:8501](http://localhost:8501)

## Geliştirme

* Yeni indikatör eklemek için `backend/app/features.py`
* Yeni sinyal kuralı eklemek için `backend/app/signals.py`
* Ek veri kaynağı eklemek için `backend/app/data_sources.py`
* UI iyileştirmeleri `frontend/app.py`

````


---

Bu repo **şu anda çalışıyor**:

```bash
docker-compose up --build
```

* Streamlit UI → [http://localhost:8501](http://localhost:8501)
* FastAPI → [http://localhost:8000/docs](http://localhost:8000/docs)

