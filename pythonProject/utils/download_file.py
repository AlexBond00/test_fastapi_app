import uuid

from aiogram.types import Message

from file_model import FileModel


async def download_file(event: Message):
    """Download file from tg server."""
    actions = [
        "document",
        "photo",
        "audio",
        "video"
    ]
    for action in actions:
        # Check if message has files or not
        files = getattr(event, action)
        if not files:
            continue
        # If files are images or videos tg makes them in 3 copies with
        # different qualities, choose the middle one
        if action in ("photo", "video"):
            file = files[-2]
        else:
            file = files
        # Uniqueness with uuid aslt
        salt = uuid.uuid4().hex
        file_id = file.file_id
        file = await event.bot.get_file(file_id)
        file_path = file.file_path
        filename = "media/" + salt + "_" + file_path.split('/')[-1]
        await event.bot.download_file(file_path, filename)
        await save_file_in_db(filename, event.message_id)


async def save_file_in_db(path: str, message_id: int):
    """Save file in DB."""
    await FileModel.create(
        path=path,
        message_id=message_id
    )
