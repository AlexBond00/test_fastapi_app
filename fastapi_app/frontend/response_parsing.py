from datetime import datetime
from pprint import pprint
from typing import Any

from api.tortoise_models.file_model import FileModel


async def response_parsing(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records_list: list = []
    for record in records:
        is_bot = record.get("json").get("from_user").get("is_bot")
        text = record.get("json").get("text")
        date = record.get("created_at")
        date_now: datetime = datetime.now()
        message_id = record.get("message_id")
        file: FileModel = await FileModel.get_or_none(message_id=message_id)
        if file:
            file_path = file.path
        else:
            file_path = False
        # converting a string to a date object
        date_time_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        # checking how much time has passed since sending the message
        timer_limit = date_now - date_time_obj
        if timer_limit.days < 2:
            checking_time = True
        else:
            checking_time = False
        correct_date = str(date_time_obj.date())
        correct_time = str(date_time_obj.time())

        records_list.append({"is_bot": is_bot, "text": text,
                             "correct_date": correct_date, "correct_time": correct_time[:5],
                             "checking_time": checking_time,
                             "file_path": file_path,
                             "message_id": message_id})

    return records_list
