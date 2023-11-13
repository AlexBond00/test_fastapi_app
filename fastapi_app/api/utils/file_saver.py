import aiofiles

from ..config import __MEDIA_PATH
from ..tortoise_models.file_model import FileModel


async def save_file(content: bytes, filename: str, message_id: int):
    """Save file on server and in DB."""
    path = __MEDIA_PATH / filename

    async with aiofiles.open(path, 'wb') as out_file:
        await out_file.write(content)

    await FileModel.create(
        path=path,
        message_id=message_id
    )
