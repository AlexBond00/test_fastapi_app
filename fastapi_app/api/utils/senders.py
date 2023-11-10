import uuid

import aiogram
from aiogram.types import BufferedInputFile
from fastapi import UploadFile

from ..config import __TYPES
from ..utils.file_saver import save_file
from ..utils.message_saver import save_message


async def send_according_to_message_type(
        filename, content, aio_bot, chat_id: int, message_type: str = "text"
) -> None:
    """Refactoring."""
    message = await getattr(aio_bot, __TYPES[message_type])(
        chat_id,
        BufferedInputFile(content, filename)
    )
    message_id = await save_message(message)
    await save_file(content, filename, message_id)


async def message_sender(
        filename, content, _type, aio_bot: aiogram.Bot, chat_id: int
):
    """Matches file types to tg send methods."""
    async with aio_bot.context():
        if _type in __TYPES:
            await send_according_to_message_type(
                filename, content, aio_bot, chat_id, _type)
        else:
            await send_according_to_message_type(
                filename, content, aio_bot, chat_id)


async def file_sender(aio_bot, chat_id, files: list[UploadFile]) -> None:
    for file in files:
        salt = uuid.uuid4().hex
        filename = salt + "_" + file.filename
        _type = file.content_type.split('/')[0]
        content = await file.read()
        await message_sender(filename, content, _type, aio_bot, chat_id)
    # try:
    #     done, pending = await asyncio.wait(
    #         tasks, return_when=asyncio.FIRST_EXCEPTION)
    #     file_names_to_revoke_tasks: list[str] = []
    #
    #     for task in done:
    #         exception = task.exception()
    #         print(task.get_name(), exception)
    #         if isinstance(
    #                 exception,
    #                 (TelegramNetworkError, TelegramBadRequest, ClientOSError)
    #         ):
    #             file_names_to_revoke_tasks.append(task.get_name())
    #             for task_pend in pending:
    #                 file_names_to_revoke_tasks.append(task_pend.get_name())
    #                 task_pend.cancel()
    #             for name in file_names_to_revoke_tasks:
    #
    #             await asyncio.sleep(1)
    #
    #             await file_sender(
    #                 aio_bot, chat_id,
    #                 contents=collect_contents
    #             )
    #             break
    #
    # except Exception as e:
    #     pass
