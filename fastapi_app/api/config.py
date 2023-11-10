from typing import Final

from aiogram import Bot

__DEFAULT_LIMIT: Final[int] = 10

__DEFAULT_OFFSET: Final[int] = 0

__TYPES = {
    "audio": "send_audio",
    "image": "send_photo",  # 10 mb
    "video": "send_video",
    "text": "send_document"
}
