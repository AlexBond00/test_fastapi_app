from datetime import datetime
from pprint import pprint
from typing import Any

from api.tortoise_models.file_model import FileModel
from api.tortoise_models.legacy_message_model import LegacyMessageModel


async def response_parsing(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records_list: list = []
    for record in records:
        is_bot = record.get("json").get("from_user").get("is_bot")
        text = record.get("json").get("text")
        date = record.get("created_at")[:16]
        date_now: datetime = datetime.now()
        found_id = record.get("id")
        message_id = record.get("message_id")
        file: FileModel = await FileModel.get_or_none(message_id=found_id)
        # checking for the presence of a file
        if file:
            file_path = file.path
            print(file_path)
            file_type = file.content_type
            file_id = file.id
        else:
            file_path = False
            file_type = False
            file_id = False
        # converting a string to a date object
        date_time_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        # checking how much time has passed since sending the message
        timer_limit = date_now - date_time_obj
        if timer_limit.days < 2:
            checking_time = True
        else:
            checking_time = False
        correct_date = str(date_time_obj.date())
        correct_time = str(date_time_obj.time())

        # get the modified messages
        legacy_messages_list: list[dict[str]] = []
        legacy_messages: list[LegacyMessageModel] = await LegacyMessageModel.filter(
            message_id=record.get("id")
        ).all()
        for legacy_message in legacy_messages:
            legacy_messages_list.append({"created_at": str(legacy_message.created_at)[:16],
                                         "text": legacy_message.json.get("text")})

        records_list.append({"is_bot": is_bot, "text": text,
                             "correct_date": correct_date, "correct_time": correct_time,
                             "checking_time": checking_time,
                             "file_path": file_path,
                             "file_type": file_type,
                             "file_id": file_id,
                             "message_id": message_id,
                             "legacy_messages_list": legacy_messages_list})

    return records_list
