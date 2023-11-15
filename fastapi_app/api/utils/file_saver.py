import uuid

import aiofiles
from fastapi import UploadFile

from ..config import __MEDIA_PATH
from ..tortoise_models.file_model import FileModel
from ..tortoise_models.message_model import MessageModel


async def save_file(
        content: bytes,
        filename: str,
        message: MessageModel,
        content_type: str
):
    """Save file on server and in DB."""
    path = str(__MEDIA_PATH / filename)
    # folder with fastapi_app
    relation_path = path.split("fastapi_app/")[-1]

    async with aiofiles.open(path, 'wb') as out_file:
        await out_file.write(content)

    await FileModel.create(
        message=message,
        path=relation_path,
        content_type=content_type
    )


async def bulk_save_file(
        mapped_files: dict[MessageModel, UploadFile],
):
    """Save multiple files on server and in DB."""
    # TODO: same code in senders.send_according...
    for message, file in mapped_files.items():
        salt = uuid.uuid4().hex
        content = await file.read()
        filename = salt + "_" + file.filename
        content_type = file.content_type.split("/")[0]
        await save_file(
            content, filename, message, content_type
        )
