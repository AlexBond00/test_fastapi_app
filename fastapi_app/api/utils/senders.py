import uuid

import aiogram
from aiogram.types import BufferedInputFile
from fastapi import UploadFile

from ..config import __TYPES
from ..utils.file_saver import save_file
from ..utils.message_saver import save_message


async def build_media_groups(files: list[UploadFile]):
    """Media groups builder."""
    build_media_groups.audio_group = []
    build_media_groups.video_group = []
    build_media_groups.document_group = []
    build_media_groups.photo_group = []

    for file in files:
        actions = await get_type_actions(file)
        container_name = actions.get("container")
        container: list = getattr(build_media_groups, container_name)
        container.append(file)

    media_groups = [
        build_media_groups.audio_group,
        build_media_groups.video_group,
        build_media_groups.document_group,
        build_media_groups.photo_group
    ]
    print(media_groups)
    return media_groups


async def get_type_actions(file: UploadFile) -> dict:
    """Get action depends in content type."""
    _type = file.content_type.split('/')[0]
    actions = __TYPES.get(_type)
    if actions:
        return actions
    return __TYPES.get("text")

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
    await build_media_groups(files)
    if not files:
        async with aio_bot.context():
            message = await aio_bot.send_message(
                chat_id=chat_id,
                text=text
            )
            await save_message(message)

    if files:
        for file in files:
            try:
                await file_sender(file, aio_bot, chat_id, text)
            except Exception as e:
                raise e
            finally:
                text = None
