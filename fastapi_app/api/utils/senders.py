import asyncio
import uuid

import aiogram
from aiogram.types import BufferedInputFile
from fastapi import UploadFile
from ..config import __TYPES
from ..utils.file_saver import save_file
from ..utils.message_saver import save_message
from aiogram.exceptions import TelegramNetworkError

async def task_generator(function: callable, container: list, *args, **kwargs):
    """
    Creates a task based on the passed function and its arguments.
    Adds a task to the passed list

    :param function: Function to execute
    :param container: The list where the tasks will be stored
    :param args: Positional arguments for the function
    :param kwargs: Named arguments for the function
    :return:
    """
    coroutine = function(*args)
    task = asyncio.create_task(coroutine, **kwargs)
    container.append(task)


async def send_according_to_message_type(
        file: UploadFile, aio_bot, chat_id: int, message_type: str = "text"
) -> None:
    """Choose aiogram method to send file depending on its content type."""
    salt = uuid.uuid4().hex
    await file.seek(0)
    content = await file.read()
    filename = salt + "_" + file.filename
    message = await getattr(aio_bot, __TYPES[message_type])(
        chat_id,
        BufferedInputFile(content, filename)
    )
    message_id = await save_message(message)
    await save_file(content, filename, message_id)


async def message_sender(
        file: UploadFile, aio_bot: aiogram.Bot, chat_id: int
):
    """Matches file types to tg send methods."""
    file_content_type = file.content_type.split('/')[0]
    async with aio_bot.context():
        if file_content_type in __TYPES:
            await send_according_to_message_type(
                file, aio_bot, chat_id, file_content_type)
        else:
            await send_according_to_message_type(
                file, aio_bot, chat_id)


async def file_sender(aio_bot, chat_id, files: list[UploadFile]) -> None:
    for file in files:
        try:
            await message_sender(file, aio_bot, chat_id)
        except Exception as e:
            raise e
