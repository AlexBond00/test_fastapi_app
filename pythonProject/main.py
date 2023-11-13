import asyncio
import datetime
import json

import aiogram
from tortoise import Tortoise

from dialogue_model import DialogueModel
from message_middleware import SaveMiddleware
from message_model import MessageModel
from legacy_message_model import LegacyMessageModel

async def init_tortoise():
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
        answer = await message.answer("Hello_world!")
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

    bot = aiogram.Bot(token="6489796599:AAGyUnbepH9PN_aE7VYcutmxtCw7Wwmhoek")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
