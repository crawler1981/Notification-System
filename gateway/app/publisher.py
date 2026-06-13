import json
import aio_pika
from aio_pika import Message, DeliveryMode
from .config import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
    QUEUE_NAME,
    EXCHANGE_NAME,
    ROUTING_KEY,
)

connection = None
channel = None
exchange = None


async def connect_rabbitmq():
    global connection, channel, exchange
    connection = await aio_pika.connect_robust(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        login=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD,
    )
    channel = await connection.channel()
    exchange = await channel.declare_exchange(
        EXCHANGE_NAME,
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.bind(exchange, routing_key=ROUTING_KEY)


async def publish_message(user_id: str, message: str):
    global exchange
    payload = json.dumps({"user_id": user_id, "message": message})
    msg = Message(
        body=payload.encode(),
        delivery_mode=DeliveryMode.PERSISTENT,
        content_type="application/json",
    )
    await exchange.publish(msg, routing_key=ROUTING_KEY)


async def close_rabbitmq():
    global connection
    if connection:
        await connection.close()