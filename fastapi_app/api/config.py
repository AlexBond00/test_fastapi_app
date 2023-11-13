from pathlib import Path
from typing import Final

__DEFAULT_LIMIT: Final[int] = 50

__DEFAULT_OFFSET: Final[int] = 0

__TYPES: Final[dict] = {
    "audio": {
        "method": "send_audio",
        "container": "audio_group"
    },
    "image": {
        "method": "send_photo",
        "container": "photo_group"
    },  # 10 mb
    "video": {
        "method": "send_video",
        "container": "video_group"

    },
    "text": {
        "method": "send_document",
        "container": "document_group"

    }
}

__ROOT_PATH: Final[Path] = Path(__file__).parent.parent

__MEDIA_PATH: Final[Path] = __ROOT_PATH / 'media'

# How many days token stays valid before recreation
__TOKEN_DAY_EXPIRE: Final[int] = 7
