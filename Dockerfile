FROM amancevice/pandas

COPY requirements.txt .
COPY main.py .
COPY features.json .
COPY model_knn.joblib .
COPY model_logistic.joblib .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port 8000


