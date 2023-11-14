import datetime
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from dialogue_model import DialogueModel
from message_model import MessageModel
from utils.download_file import download_file


class SaveMiddleware(BaseMiddleware):
    """Custom middleware to save messages in db."""
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        # TODO: check if event.bot exists
        dialogue, _ = await DialogueModel.get_or_create(
            bot_id=event.bot.id,
            chat_id=event.chat.id
        )
        await dialogue.update_from_dict(
            {"updated_at": datetime.datetime.now()}
        )
        await dialogue.save()

        json_str = event.model_dump_json()
        message = await MessageModel.create(
            chat_id=event.chat.id,
            bot_id=event.bot.id,
            json=json_str,
            message_id=event.message_id
        )
        # Check if there are files in update
        # and download them on server if succeeded
        await download_file(event, message)
        return await handler(event, data)
