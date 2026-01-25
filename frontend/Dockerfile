FROM python:3.11-slim
WORKDIR /app

# Gerekli klasörü oluştur
RUN mkdir -p .streamlit

# Config dosyasını kopyala (Eğer lokalde yoksa hata vermez, varsa kopyalar)
# NOT: Bu adım için kullanıcının manuel olarak .streamlit/config.toml oluşturması en sağlıklısıdır.
# Biz yine de default'ları kod içinde belirttik ama buraya da ekleyelim.

COPY app.py .
# config.toml frontend klasöründe ise:
COPY .streamlit/config.toml .streamlit/config.toml 

RUN pip install --no-cache-dir streamlit requests plotly pandas
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]