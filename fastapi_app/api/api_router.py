import datetime
import logging
from http import HTTPStatus
from typing import Annotated

import aiogram
import pytz
from fastapi import Depends, File, Form, UploadFile
from fastapi.responses import Response, RedirectResponse, JSONResponse
from fastapi.routing import APIRouter

from frontend.user_token_verify import validate_user_token
from .config import __DEFAULT_LIMIT, __DEFAULT_OFFSET
from .pydantic_models import Dialogue, Message, Bot
from .tortoise_models.bot_model import BotModel
from .tortoise_models.dialogue_model import DialogueModel
from .tortoise_models.message_model import MessageModel
from .utils.logger import logger
from .utils.senders import message_sender

api_router = APIRouter()


@api_router.get(
    "/bots/", response_model=list[Bot])
async def get_bots(
        user_token: Annotated[dict, Depends(validate_user_token)],
        offset: int = __DEFAULT_OFFSET,
        limit: int = __DEFAULT_LIMIT
) -> list[BotModel]:
    bots: list[BotModel] = await BotModel.all().offset(offset).limit(limit)

    return bots


@api_router.get(
    "/bots/{bot_id}/dialogues/", response_model=list[Dialogue]
)
async def get_dialogue_list(
        bot_id: int,
        offset: int = __DEFAULT_OFFSET,
        limit: int = __DEFAULT_LIMIT
) -> list[DialogueModel]:

    dialogues: list[DialogueModel] = (
        await DialogueModel.filter(bot_id=bot_id)
        .all()
        .offset(offset)
        .limit(limit)
    )

    return dialogues


@api_router.get(
    "/bots/{bot_id}/dialogues/{chat_id}/messages/",
    response_model=list[Message]
)
async def get_messages(
        chat_id: int,
        bot_id: int,
        offset: int = __DEFAULT_OFFSET,
        limit: int = __DEFAULT_LIMIT
) -> list[MessageModel]:

    messages: list[MessageModel] = (
        await MessageModel.filter(chat_id=chat_id,bot_id=bot_id)
        .all()
        .offset(offset)
        .limit(limit)
    )

    return messages


@api_router.post("/bots/{bot_id}/dialogues/{chat_id}/sendMessage/")
async def send_message(
        bot_id: int,
        chat_id: int,
        text: Annotated[str | None, Form()] = None,
        files: Annotated[list[UploadFile], File()] = None,
):

    bot_model = await BotModel.filter(uid=bot_id).first()
    if not bot_model:
        data = {
            "error_message": f"There is no bot with id {bot_id}"
        }
        return JSONResponse(
            content=data,
            status_code=HTTPStatus.NOT_FOUND,
        )

    dialogue = await DialogueModel.filter(chat_id=chat_id,bot_id=bot_id).first()
    if not dialogue:
        data = {
            "error_message": f"There is no bot chat with user id {chat_id}"
        }
        return JSONResponse(
            content=data,
            status_code=HTTPStatus.NOT_FOUND
        )

    aio_bot = aiogram.Bot(token=bot_model.token, parse_mode="HTML")
    try:
        await message_sender(aio_bot, chat_id, text, files)
    except Exception as e:
        logger.log(level=logging.ERROR, msg=e)

    dialogue.updated_at = datetime.datetime.now(tz=pytz.UTC)
    await dialogue.save()

    return RedirectResponse(f"/dialogues/{bot_id}/{chat_id}")


@api_router.post(
    "/bots/{bot_id}/dialogues/{chat_id}/messages/{message_id}/deleteMessage")
async def delete_message(
        bot_id: int,
        chat_id: int,
        message_id: int
):

    message = await MessageModel.filter(chat_id=chat_id, bot_id=bot_id, message_id=message_id).first()
    if not message:
        data = {
            "error_message": f"There is no such message you want to delete."
        }
        return JSONResponse(content=data, status_code=HTTPStatus.NOT_FOUND)

    bot_model = await BotModel.filter(uid=bot_id).first()
    if not bot_model:
        data = {
            "error_message": f"There is no such bot with "
                             f"uid {bot_id} in your DB."
        }
        return JSONResponse(content=data, status_code=HTTPStatus.BAD_REQUEST)

    aio_bot = aiogram.Bot(token=bot_model.token)
    async with aio_bot.context():
        status = await aio_bot.delete_message(
            chat_id=chat_id, message_id=message_id
        )

    if not status:
        return Response(status_code=HTTPStatus.BAD_REQUEST)

    await message.delete()

    return RedirectResponse(f"/dialogues/{bot_id}/{chat_id}")
