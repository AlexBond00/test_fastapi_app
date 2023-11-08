from fastapi.routing import APIRouter

from tortoise_models.dialogue_model import DialogueModel
from tortoise_models.message_model import MessageModel
from .pydantic_models import Dialogue, SendMessage, Message
import aiogram
api_router = APIRouter()


@api_router.get("/dialogue/", response_model=list[Dialogue])
async def get_dialogue_list():
    dialogues: list[DialogueModel] = await DialogueModel.all()
    return dialogues


@api_router.get("/dialogue/{bot_id}_{chat_id}/", response_model=list[Message])
async def get_messages(chat_id: int, bot_id: int) -> list[MessageModel]:
    messages: list[MessageModel] = await MessageModel.filter(
        chat_id=chat_id,
        bot_id=bot_id
    ).all()
    return messages


@api_router.post("/dialogue/{bot_id}_{chat_id}/")
async def send_message(bot_id: int, chat_id: int, message_text: SendMessage):
    return message_text
