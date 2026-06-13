import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .consumer import connect_rabbitmq, start_consumer, close_rabbitmq


consumer_task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global consumer_task
    queue = await connect_rabbitmq()
    consumer_task = asyncio.create_task(start_consumer(queue))
    print("[Notification Service] Started consuming...")
    yield
    consumer_task.cancel()
    await close_rabbitmq()


app = FastAPI(title="Notification Service", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "healthy"}