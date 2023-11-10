import datetime
from http import HTTPStatus
from typing import Annotated

import aiogram
import pytz
from fastapi import File
from fastapi import Form
from fastapi import UploadFile
from fastapi.responses import Response, RedirectResponse
from fastapi.routing import APIRouter

from .config import __DEFAULT_LIMIT, __DEFAULT_OFFSET
from .pydantic_models import Dialogue, Message, Bot
from .tortoise_models.bot_model import BotModel
from .tortoise_models.dialogue_model import DialogueModel
from .tortoise_models.message_model import MessageModel
from .utils.message_sender import message_sender
from fastapi.responses import JSONResponse
api_router = APIRouter()


@api_router.get("/bots/", response_model=list[Bot])
async def get_bots(
        offset: int = __DEFAULT_OFFSET,
        limit: int = __DEFAULT_LIMIT
) -> list[BotModel] | Response:
    bots: list[BotModel] = await BotModel.all().offset(offset).limit(limit)

    if bots:
        return bots

    return Response(status_code=HTTPStatus.NO_CONTENT)


@api_router.get("/bots/{bot_id}/dialogues/", response_model=list[Dialogue])
async def get_dialogue_list(
        bot_id: int,
        offset: int = __DEFAULT_OFFSET,
        limit: int = __DEFAULT_LIMIT
) -> list[DialogueModel] | Response:
    dialogues: list[DialogueModel] = await DialogueModel.filter(
        bot_id=bot_id
    ).all().offset(offset).limit(limit)

    if dialogues:
        return dialogues

    return Response(status_code=HTTPStatus.NO_CONTENT)


@api_router.get(
    "/bots/{bot_id}/dialogues/{chat_id}", response_model=list[Message]
)
async def get_messages(
        chat_id: int,
        bot_id: int,
        offset: int = __DEFAULT_OFFSET,
        limit: int = __DEFAULT_LIMIT
) -> list[MessageModel] | Response:
    messages: list[MessageModel] = await MessageModel.filter(
        chat_id=chat_id,
        bot_id=bot_id
    ).all()

    if messages:
        return messages

    return Response(status_code=HTTPStatus.NO_CONTENT)


@api_router.post("/bots/{bot_id}/dialogues/{chat_id}/sendMessage/")
async def send_message(
        bot_id: int,
        chat_id: int,
        text: Annotated[str | None, Form()] = None,
        files: Annotated[list[UploadFile], File()] = None,
):
    bot_db = await BotModel.filter(uid=bot_id).first()
    if not bot_db:
        data = {
            "error_message": f"There is no bot with id {bot_id}"
        }
        return JSONResponse(
            content=data,
            status_code=HTTPStatus.NOT_FOUND
        )
    dialogue = await DialogueModel.get_or_none(
        chat_id=chat_id,
        bot_id=bot_id
    )
    if not dialogue:
        data = {
            "error_message": f"There is no bot chat with user id {chat_id}"
        }
        return JSONResponse(
            content=data,
            status_code=HTTPStatus.NOT_FOUND
        )
    aio_bot = aiogram.Bot(token=bot_db.token)
    sent_messages = []

    if text:
        sent_messages.append(await aio_bot.send_message(
            chat_id=chat_id,
            text=text
        )
                             )
    if files:
        sent_messages.extend(
            [
                await message_sender(file, aio_bot, chat_id) for file in files
            ]
        )
    for sent_message in sent_messages:
        json_str = sent_message.model_dump_json()
        await MessageModel.create(
            chat_id=sent_message.chat.id,
            bot_id=sent_message.bot.id,
            json=json_str,
            message_id=sent_message.message_id
        )

    await dialogue.update_from_dict(
            {"updated_at": datetime.datetime.now(tz=pytz.UTC)}
        )
    await dialogue.save()
    return RedirectResponse(f"/{bot_id}/{chat_id}/")

