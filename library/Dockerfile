FROM python:3.11-slim

WORKDIR /app

COPY library/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY library/app ./app

COPY proto /proto

RUN mkdir -p /app/proto

RUN touch /app/proto/__init__.py

RUN python -m grpc_tools.protoc -I/proto --python_out=/app/proto --grpc_python_out=/app/proto /proto/library.proto

ENV PYTHONPATH=/app/proto

EXPOSE 50051

CMD ["python", "-m", "app.server"]
