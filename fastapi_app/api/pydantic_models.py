from datetime import datetime

from pydantic import BaseModel


class Dialogue(BaseModel):
    bot_id: int
    chat_id: int
    updated_at: datetime


class Message(BaseModel):
    id: int
    bot_id: int
    chat_id: int
    message_id: int
    json: dict
    is_edited: bool | None
    created_at: datetime



class Bot(BaseModel):
    title: str
    token: str
    uid: int
