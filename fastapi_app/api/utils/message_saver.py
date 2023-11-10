from aiogram.types import Message

from ..tortoise_models.message_model import MessageModel


async def save_message(message: Message):
    """DB message savior."""
    json_str = message.model_dump_json()
    message = await MessageModel.create(
        chat_id=message.chat.id,
        bot_id=message.bot.id,
        json=json_str,
        message_id=message.message_id
    )
    # Returns message_id to link to it
    return message.message_id
