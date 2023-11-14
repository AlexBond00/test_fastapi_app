import asyncio
import datetime
import json

import aiogram
from tortoise import Tortoise

from dialogue_model import DialogueModel
from legacy_message_model import LegacyMessageModel
from message_middleware import SaveMiddleware
from message_model import MessageModel


async def init_tortoise():
    """Tortoise initialization."""
    with open("db_config.json") as f:
        json_data = json.load(f)

    await Tortoise.init(
        config=json_data,
        use_tz=True
    )
    await Tortoise.generate_schemas(safe=True)


async def main():
    """Main logic."""
    dp = aiogram.Dispatcher()
    dp.message.middleware(SaveMiddleware())

    await init_tortoise()

    @dp.message()
    async def message_handler(message: aiogram.types.Message):
        answer = await message.answer("Hello world!")
        dialogue = await DialogueModel.get_or_none(
            chat_id=message.chat.id,
            bot_id=message.bot.id
        )
        json_bot = answer.model_dump_json()
        await MessageModel.create(
            chat_id=message.chat.id,
            bot_id=message.bot.id,
            message_id=answer.message_id,
            json=json_bot
        )
        await dialogue.update_from_dict(
            {"updated_at": datetime.datetime.now()}
        )
        await dialogue.save()

    @dp.edited_message()
    async def edited_message_handler(edited_message: aiogram.types.Message):
        message_id = edited_message.message_id
        chat_id = edited_message.chat.id
        new_text = edited_message.text
        message_to_edit = await MessageModel.get_or_none(
            chat_id=chat_id,
            message_id=message_id,
            bot_id=edited_message.bot.id
        )
        if message_to_edit:
            js_obj = message_to_edit.json
            await LegacyMessageModel.create(
                chat_id=chat_id,
                bot_id=message_to_edit.bot_id,
                message_id=message_id,
                json=js_obj
            )
            js_obj['text'] = new_text
            upd = {"json": js_obj}
            await message_to_edit.update_from_dict(upd)
            await message_to_edit.save()

    bots = [
        aiogram.Bot(token="6188043261:AAGYFnlrD1WhjK7UIoaa2XP1GZl6qE0dW3g"),
        aiogram.Bot(token="5889733176:AAHKbaB70yUayTROdGcebwYQWjr3g4a6KYs")
    ]

    await dp.start_polling(*bots)


if __name__ == "__main__":
    asyncio.run(main())
