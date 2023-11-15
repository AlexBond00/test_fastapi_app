import logging
import uuid

import aiogram
from aiogram.exceptions import TelegramBadRequest, TelegramServerError
from aiogram.types import BufferedInputFile, InputMedia, InputMediaDocument
from fastapi import UploadFile

from .logger import logger
from ..config import __TYPE_ACTIONS, __TG_MEDIA_TYPES
from ..utils.file_saver import save_file, bulk_save_file
from ..utils.get_file_type import get_file_type
from ..utils.message_saver import save_message, bulk_save_message


async def get_builder(file: UploadFile):
    """Get telegram media file builder."""
    type_ = await get_file_type(file)
    if type_ in __TG_MEDIA_TYPES:
        return __TYPE_ACTIONS.get(type_).get("aio_file_builder")
    return InputMediaDocument


async def send_media_as_group(
        group: list[UploadFile],
        aio_bot: aiogram.Bot,
        chat_id: int,
        text: str = None
) -> list[aiogram.types.Message]:
    """Build media group and send it."""
    media_group = []
    for file in group:
        builder: InputMedia = await get_builder(file)
        if builder:
            media_group.append(
                builder(
                    media=BufferedInputFile(await file.read(), file.filename),
                    caption=text
                )
            )
        if text:
            # set text to None after usage to not caption each file further
            text = None
    async with aio_bot.context():
        messages = await aio_bot.send_media_group(chat_id, media=media_group)
        return messages


async def build_media_groups(files: list[UploadFile]) -> dict:
    """Media groups builder."""

    # Initialized containers to fill with specific media types if exist
    build_media_groups.visual = []
    build_media_groups.text = []
    build_media_groups.audio = []

    for file in files:
        actions = await get_type_actions(file)
        # get container name from config that depends on file content type
        container_name = actions.get("container")
        # get container set above
        container: list = getattr(build_media_groups, container_name)
        container.append(file)

    return vars(build_media_groups)


async def get_type_actions(file: UploadFile) -> dict:
    """Get action depends on content type."""
    _type = await get_file_type(file)
    actions = __TYPE_ACTIONS.get(_type)
    if actions:
        return actions
    # if there is no type matched we use default "text" type to handle file
    return __TYPE_ACTIONS.get("text")


async def send_according_to_message_type(
        file: UploadFile,
        aio_bot: aiogram.Bot,
        chat_id: int,
        text: str | None,
        method: str
) -> None:
    """Choose aiogram method to send file depending on its content type."""
    salt = uuid.uuid4().hex
    content = await file.read()
    filename = salt + "_" + file.filename
    content_type = await get_file_type(file)
    message = await getattr(aio_bot, method)(
        chat_id,
        BufferedInputFile(content, filename),
        caption=text
    )
    message_model = await save_message(message)
    await save_file(
        content, filename, message_model, content_type)


async def file_sender(
        file: UploadFile,
        aio_bot: aiogram.Bot,
        chat_id: int,
        text: str | None
):
    """Matches file types to tg send methods."""
    actions = await get_type_actions(file)
    try:
        method = actions.get("method")
    except AttributeError as e:
        logger.log(level=logging.ERROR, msg=e)
        method = "send_document"
    async with aio_bot.context():
        await send_according_to_message_type(
            file, aio_bot, chat_id, text, method
        )


async def message_sender(
        aio_bot: aiogram.Bot,
        chat_id: int,
        text: str | None = None,
        files: list[UploadFile] | None = None,

) -> None:
    """Handler to send messages."""
    if not files:
        async with aio_bot.context():
            message = await aio_bot.send_message(
                chat_id=chat_id,
                text=text
            )
            await save_message(message)

    else:
        # If there are text and files in one request
        # we try to caption some file or file groups (media group)
        # with sent text
        if len(files) == 1:
            try:
                file = files[0]
                await file_sender(file, aio_bot, chat_id, text)
            except Exception as e:
                logger.log(level=logging.ERROR, msg=e)
        # if there are more than one file we try to send them as media group
        else:
            file_groups = await build_media_groups(files)

            for group_name, group_values in file_groups.items():
                try:
                    async with aio_bot.context():
                        messages = await send_media_as_group(
                            group_values, aio_bot, chat_id, text
                        )
                    # get list with saved messages' ids
                    msg_list = await bulk_save_message(messages)
                    # make dict with ids compare to file
                    zipped = dict(zip(msg_list, group_values))
                    # use dict to save each file in DB
                    await bulk_save_file(zipped)
                except (TelegramBadRequest, TelegramServerError) as e:
                    logger.log(level=logging.ERROR, msg=e)
                    continue
                finally:
                    text = None
