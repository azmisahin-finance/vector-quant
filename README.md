# 🛰️ VektorQuant

**Institutional Grade Quantitative Analytics & Trading Terminal**

![Main Dashboard](docs/assets/screenshots/dashboard-main.png)

> **"Kör Sinyal Yok, Sadece Matematik Var."**

VektorQuant; **BIST, Kripto, Forex ve ABD Borsalarını** analiz eden, yapay zeka destekli (Vector Similarity) ve risk odaklı (Sharpe/Drawdown) profesyonel bir analiz terminalidir.

---

## ⚡ Neden VektorQuant?

*   **🌍 Evrensel Erişim:** Tek bir arayüzden `THYAO.IS` (BIST), `BTC-USD` (Kripto), `EURUSD` (Forex) ve `AAPL` (Nasdaq) analizi.
*   **🧠 Vector AI:** "Bugünkü piyasa hareketi tarihte en çok hangi güne benziyor?" sorusunu FAISS vektör veritabanı ile yanıtlar.
*   **🛡️ Risk Engine:** Sadece "Al/Sat" sinyali üretmez; işlemin **Sharpe Oranını** ve **Win Rate** başarısını hesaplar.
*   **⏳ Multi-Timeframe:** Günlük (1d) analizden, gün içi (15m, 1h) skalping analizlerine kadar esnek zaman dilimleri.

## 🚀 Kurulum

```bash
# 1. Repoyu klonla
git clone https://github.com/your-username/VektorQuant.git
cd VektorQuant

# 2. Sistemi başlat
docker-compose up --build
```
Tarayıcıda aç: **[http://localhost:8501](http://localhost:8501)**

---

## 📸 Proof of Work (Kanıtlar)

Sistemin farklı piyasalardaki çalışma kanıtları için [Dokümantasyon Sayfamıza](docs/index.md) göz atın.
```

#### 2. Dosya: `docs/index.md`
*(Detaylı dokümantasyon sayfasına "Galeri" ekliyoruz)*

```markdown
# VektorQuant Terminal

**Professional Quantitative Analysis Platform**

VektorQuant, perakende yatırımcılar için kurumsal düzeyde analiz yetenekleri sunan Docker tabanlı bir finansal teknolojidir.

---

## 📸 Gallery & Proof of Work

Sistemin farklı varlık sınıfları (Asset Classes) üzerindeki başarısı aşağıda test edilmiştir.

### 1. Borsa İstanbul (BIST 100)
Yerel para birimi (`₺`) desteği ve BIST veri entegrasyonu.
![BIST Analysis](assets/screenshots/dashboard-bist.png)

### 2. Kripto Para Piyasaları (24/7)
Yüksek volatilite içeren varlıklarda Bollinger ve RSI uyumu.
![Crypto Analysis](assets/screenshots/dashboard-crypto.png)

### 3. Forex & Pariteler
Global pariteler (`€`, `$`) ve makro analiz yeteneği.
![Forex Analysis](assets/screenshots/dashboard-forex.png)

### 4. Emtialar (Altın/Gümüş)
Emtia piyasalarındaki trend takibi ve risk analizi.
![Commodities Analysis](assets/screenshots/dashboard-commodities.png)

---

## 🏗️ Mimari Özellikler

| Bileşen | Teknoloji | Açıklama |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Bloomberg Terminal esintili, CSS ile güçlendirilmiş arayüz. |
| **Backend** | FastAPI | Asenkron, yüksek performanslı API Gateway. |
| **AI Engine** | FAISS | Vektör tabanlı tarihsel benzerlik arama motoru. |
| **Data Feed** | Yahoo Finance | User-Agent korumalı, çoklu zaman dilimi destekli veri motoru. |
```
