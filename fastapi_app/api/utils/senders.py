import uuid

import aiogram
from aiogram.exceptions import TelegramBadRequest, TelegramServerError
from aiogram.types import BufferedInputFile, InputMediaDocument
from fastapi import UploadFile

from ..config import __TYPE_ACTIONS
from ..utils.file_saver import save_file, bulk_save_file
from ..utils.message_saver import save_message, bulk_save_message


async def send_media_as_group(
        group: list[UploadFile],
        aio_bot: aiogram.Bot,
        chat_id: int,
        builder=InputMediaDocument,
        text: str = None
) -> list[aiogram.types.Message]:
    """Build media group and send it."""
    media_group = []
    for file in group:
        media_group.append(builder(media=BufferedInputFile(
                    await file.read(), file.filename), caption=text
        )
        )
        if text:
            text = None
    async with aio_bot.context():
        messages = await aio_bot.send_media_group(chat_id, media=media_group)
        return messages


async def build_media_groups(files: list[UploadFile]) -> dict:
    """Media groups builder."""
    build_media_groups.video = []
    build_media_groups.image = []
    build_media_groups.text = []
    build_media_groups.audio = []

    for file in files:
        actions = await get_type_actions(file)
        container_name = actions.get("container")
        container: list = getattr(build_media_groups, container_name)
        container.append(file)

    return vars(build_media_groups)


async def get_type_actions(file: UploadFile) -> dict:
    """Get action depends in content type."""
    _type = file.content_type.split('/')[0]
    actions = __TYPE_ACTIONS.get(_type)
    if actions:
        return actions
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
    message = await getattr(aio_bot, method)(
        chat_id,
        BufferedInputFile(content, filename),
        caption=text
    )
    message_id = await save_message(message)
    await save_file(content, filename, message_id)


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
    except AttributeError:
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
    if not files:
        async with aio_bot.context():
            message = await aio_bot.send_message(
                chat_id=chat_id,
                text=text
            )
            await save_message(message)

    if files:
        file_groups = await build_media_groups(files)

        for group_name, group_values in file_groups.items():
            if len(group_values) > 1:
                builder = __TYPE_ACTIONS.get(
                    group_name).get("aio_file_builder")
                try:
                    async with aio_bot.context():
                        messages = await send_media_as_group(
                            group_values, aio_bot, chat_id, builder, text
                        )
                        msg_list = await bulk_save_message(messages)
                        zipped = dict(zip(msg_list, group_values))
                        await bulk_save_file(zipped)
                except (TelegramBadRequest, TelegramServerError) as e:
                    print(e)
                    continue
                finally:
                    text = None

            elif len(group_values) == 1:
                try:
                    file = group_values[0]
                    await file_sender(file, aio_bot, chat_id, text)
                except Exception as e:
                    raise e
                finally:
                    text = None
            else:
                continue
