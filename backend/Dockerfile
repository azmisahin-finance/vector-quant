FROM python:3.11-slim
WORKDIR /app
COPY app/ app/
# scipy eklendi (advanced stats için gerekebilir)
RUN pip install --no-cache-dir fastapi uvicorn yfinance pandas numpy scikit-learn faiss-cpu requests scipy
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]