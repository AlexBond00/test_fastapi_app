from typing import Final
from pathlib import Path

__DEFAULT_LIMIT: Final[int] = 20

__DEFAULT_OFFSET: Final[int] = 0

__TYPES: Final[dict] = {
    "audio": "send_audio",
    "image": "send_photo",  # 10 mb
    "video": "send_video",
    "text": "send_document"
}

__ROOT_PATH: Final[Path] = Path(__file__).parent.parent

__MEDIA_PATH: Final[Path] = __ROOT_PATH / 'media'

# How many days token stays valid before recreation
__TOKEN_DAY_EXPIRE: Final[int] = 7
