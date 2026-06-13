import json
import aio_pika
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


async def connect_rabbitmq():
    global connection, channel
    connection = await aio_pika.connect_robust(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        login=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD,
    )
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    exchange = await channel.declare_exchange(
        EXCHANGE_NAME,
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.bind(exchange, routing_key=ROUTING_KEY)
    return queue


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode())
        print(f"[NOTIFICATION] User: {data['user_id']} | Message: {data['message']}")


async def start_consumer(queue):
    await queue.consume(process_message)


async def close_rabbitmq():
    global connection
    if connection:
        await connection.close()