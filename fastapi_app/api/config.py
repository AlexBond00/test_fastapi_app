from pathlib import Path
from typing import Final

from aiogram.types import (
    InputMediaAudio, InputMediaPhoto, InputMediaDocument, InputMediaVideo
)

__DEFAULT_LIMIT: Final[int] = 100

__DEFAULT_OFFSET: Final[int] = 0

__TYPE_ACTIONS: Final[dict] = {
    "audio": {
        "method": "send_audio",
        "container": "audio",
        "aio_file_builder": InputMediaAudio
    },
    "image": {
        "method": "send_photo",
        "container": "visual",
        "aio_file_builder": InputMediaPhoto
    },
    "video": {
        "method": "send_video",
        "container": "visual",
        "aio_file_builder": InputMediaVideo
    },
    "text": {
        "method": "send_document",
        "container": "text",
        "aio_file_builder": InputMediaDocument
    }
}

__ROOT_PATH: Final[Path] = Path(__file__).parent.parent

# Store media in static path to reach files from templates
__MEDIA_PATH: Final[Path] = __ROOT_PATH / 'static/media'

# How many days token stays valid before recreation
__TOKEN_DAY_EXPIRE: Final[int] = 7

__TG_MEDIA_TYPES: Final[tuple] = ("audio", "image", "video", "text")
