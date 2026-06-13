from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .publisher import connect_rabbitmq, publish_message, close_rabbitmq


class NotificationRequest(BaseModel):
    user_id: str
    message: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_rabbitmq()
    yield
    await close_rabbitmq()


app = FastAPI(title="Gateway Service", lifespan=lifespan)


@app.post("/send")
async def send_notification(req: NotificationRequest):
    if not req.user_id or not req.message:
        raise HTTPException(status_code=400, detail="user_id and message required")
    await publish_message(req.user_id, req.message)
    return {"status": "queued", "user_id": req.user_id}

@app.get("/health")
async def health():
    return {"status": "healthy"}    