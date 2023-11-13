from pathlib import Path
from typing import Final

from aiogram.types import (
    InputMediaAudio, InputMediaPhoto, InputMediaDocument, InputMediaVideo
)

__DEFAULT_LIMIT: Final[int] = 50

__DEFAULT_OFFSET: Final[int] = 0

__TYPE_ACTIONS: Final[dict] = {
    "audio": {
        "method": "send_audio",
        "container": "audio",
        "aio_file_builder": InputMediaAudio
    },
    "image": {
        "method": "send_photo",
        "container": "image",
        "aio_file_builder": InputMediaPhoto
    },
    "video": {
        "method": "send_video",
        "container": "video",
        "aio_file_builder": InputMediaVideo

    },
    "text": {
        "method": "send_document",
        "container": "text",
        "aio_file_builder": InputMediaDocument
    }
}

__ROOT_PATH: Final[Path] = Path(__file__).parent.parent

__MEDIA_PATH: Final[Path] = __ROOT_PATH / 'static/media'

# How many days token stays valid before recreation
__TOKEN_DAY_EXPIRE: Final[int] = 7
