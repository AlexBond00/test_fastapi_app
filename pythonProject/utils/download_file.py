import uuid
from pathlib import Path
from typing import Final

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from file_model import FileModel

__MEDIA_PATH: Final[Path] = (
        Path(__file__).parent.parent.parent / "fastapi_app/static/media/"
)


async def download_file(event: Message):
    """Download file from tg server."""
    # Possible attributes in event(Message) instance
    attrs = ["document", "photo", "audio", "video"]

    for attr in attrs:
        # Check if message has files or not
        file = getattr(event, attr)
        if not file:
            continue
        # If file is image tg makes them in 3 copies with
        # different qualities, choose the middle one
        if attr == "photo":
            file = file[-2]
        # Generating uuid salt to reach uniqueness in filename
        salt = uuid.uuid4().hex
        file_id = file.file_id
        try:
            file = await event.bot.get_file(file_id)
        except TelegramBadRequest as e:
            continue
        file_path = file.file_path
        # Be sure you have "/media/" directory in tg-app root
        # TODO: refactor this?
        filename = __MEDIA_PATH / (salt + "_" + file_path.split('/')[-1])
        await event.bot.download_file(file_path, filename)
        await save_file_in_db(
            str(filename), event.message_id, event.bot.id,
            event.chat.id, "image"
        )


async def save_file_in_db(
        path: str,
        message_id: int,
        bot_id: int,
        chat_id: int,
        content_type: str
):
    """Save file in DB."""
    path = path.split("fastapi_app/")[-1]
    await FileModel.create(
        path=path,
        message_id=message_id,
        bot_id=bot_id,
        chat_id=chat_id,
        content_type=content_type
    )
