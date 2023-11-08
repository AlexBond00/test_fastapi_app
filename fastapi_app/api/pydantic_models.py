from datetime import datetime

from pydantic import BaseModel


class Dialogue(BaseModel):
    chat_id: int
    bot_id: int
    updated_at: datetime


class Message(BaseModel):
    message_id: int
    bot_id: int
    chat_id: int
    json: dict
    created_at: datetime


class SendMessage(BaseModel):
    message_text: str


class Bot(BaseModel):
    uid: int
    token: str
