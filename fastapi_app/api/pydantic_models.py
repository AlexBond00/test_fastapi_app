from datetime import datetime

from pydantic import BaseModel


class Dialogue(BaseModel):
    id: int
    chat_id: int
    bot_id: int
    updated_at: datetime


class Message(BaseModel):
    id: int
    message_id: int
    bot_id: int
    chat_id: int
    json: dict
    is_recieved: bool
    created_at: datetime


class SendMessage(BaseModel):
    message_text: str


class Bot(BaseModel):
    id: int
    token: str
    tg_bot_id: int
