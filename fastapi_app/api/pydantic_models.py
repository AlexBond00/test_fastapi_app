from datetime import datetime

from pydantic import BaseModel
from fastapi import UploadFile
from typing import Annotated


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


class Bot(BaseModel):
    uid: int
    token: str
