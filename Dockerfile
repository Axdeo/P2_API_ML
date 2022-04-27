FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip3 install joblib pandas sklearn
COPY ./app /app

