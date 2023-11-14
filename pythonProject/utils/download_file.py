import uuid

from aiogram.types import Message

from file_model import FileModel


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
        file = await event.bot.get_file(file_id)
        file_path = file.file_path
        # Be sure you have "/media/" directory in tg-app root
        filename = "media/" + salt + "_" + file_path.split('/')[-1]
        await event.bot.download_file(file_path, filename)
        await save_file_in_db(filename, event.message_id)


async def save_file_in_db(path: str, message_id: int):
    """Save file in DB."""
    await FileModel.create(
        path=path,
        message_id=message_id
    )
