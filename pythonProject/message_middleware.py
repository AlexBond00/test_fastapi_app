import datetime
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from dialogue_model import DialogueModel
from message_model import MessageModel


class SaveMiddleware(BaseMiddleware):
    """Custom middleware to save messages in db."""
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        dialogue, _ = await DialogueModel.get_or_create(
            chat_id=event.chat.id,
            bot_id=event.bot.id
        )
        await dialogue.update_from_dict(
            {"updated_at": datetime.datetime.now()}
        )
        await dialogue.save()
        json_str = event.model_dump_json()
        await MessageModel.create(
            chat_id=event.chat.id,
            bot_id=event.bot.id,
            json=json_str,
            message_id=event.message_id
        )
        return await handler(event, data)
