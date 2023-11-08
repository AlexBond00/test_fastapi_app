import datetime
from http import HTTPStatus

import aiogram
import pytz
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRouter

from .config import __DEFAULT_LIMIT, __DEFAULT_OFFSET
from .pydantic_models import Dialogue, SendMessage, Message, Bot
from .tortoise_models.bot_model import BotModel
from .tortoise_models.dialogue_model import DialogueModel
from .tortoise_models.message_model import MessageModel

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
    ).all().offset(offset).limit(limit)

    if messages:
        return messages

    return Response(status_code=HTTPStatus.NO_CONTENT)


@api_router.post(
    "/bots/{bot_id}/dialogues/{chat_id}/SendMessage/",
    response_model=SendMessage)
async def send_message(
        bot_id: int,
        chat_id: int,
        message_text: SendMessage
) -> SendMessage | JSONResponse:
    bot_db = await BotModel.get_or_none(uid=bot_id)
    dialogue = await DialogueModel.get_or_none(
        chat_id=chat_id,
        bot_id=bot_id
    )
    if not bot_db or not dialogue:
        data = {
            "error_message": f"There is no bot with id {bot_id} or "
                             f"bot chat with id {chat_id}"
        }
        return JSONResponse(
            content=data,
            status_code=HTTPStatus.NOT_FOUND
        )

    aio_bot = aiogram.Bot(token=bot_db.token)
    async with aio_bot.context():
        await aio_bot.send_message(
            chat_id=chat_id,
            text=message_text.message_text
        )
    await dialogue.update_from_dict(
        {"updated_at": datetime.datetime.now(tz=pytz.UTC)}
    )
    await dialogue.save()

    return message_text
