import aiogram
# from ..config import __TYPES
from aiogram.types import BufferedInputFile
from fastapi import UploadFile
from ..config import __TYPES


async def message_sender(file: UploadFile, aio_bot: aiogram.Bot, chat_id: int):
    """Matches file types to tg send methods."""
    _type = file.content_type.split('/')[0]

    async with aio_bot.context():
        if _type in __TYPES:
            message = await getattr(aio_bot, __TYPES[_type])(
                chat_id,
                BufferedInputFile(file.file.read(), file.filename)
            )
            return message

        message = await getattr(aio_bot, __TYPES["text"])(
            chat_id,
            BufferedInputFile(file.file.read(), file.filename))
        return message
