FROM python:3.11-slim

WORKDIR /app

COPY notification/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY notification/app ./app

EXPOSE 9001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9001"]