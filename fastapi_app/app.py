import asyncio
import json
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from tortoise import Tortoise

from models.dialogue_model import DialogueModel
from models.message_model import MessageModel
from frontend.front_api import router



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


async def init_tortoise():
    with open("db_config.json") as f:
        json_data = json.load(f)

    await Tortoise.init(
        config=json_data,
        use_tz=True
    )
    await Tortoise.generate_schemas(safe=True)


app = FastAPI()

app.include_router(router)


@app.get("/dialogue/", response_model=list[Dialogue])
async def get_dialogue_list():
    dialogues: list[DialogueModel] = await DialogueModel.all()
    return dialogues


@app.get("/dialogue/{bot_id}_{chat_id}/", response_model=list[Message])
async def get_messages(chat_id: int, bot_id: int):
    messages = await MessageModel.filter(chat_id=chat_id, bot_id=bot_id).all()
    return messages


async def main():
    await init_tortoise()
    config = uvicorn.Config("app:app", port=8080)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
