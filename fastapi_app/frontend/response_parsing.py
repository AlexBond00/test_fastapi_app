from datetime import datetime
from typing import Any


async def response_parsing(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records_list: list = []
    for record in records:
        is_bot = record.get("json").get("from_user").get("is_bot")
        text = record.get("json").get("text")
        date = record.get("created_at")
        message_id = record.get("message_id")
        # converting a string to a date object
        date_time_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        correct_date = str(date_time_obj.date())
        correct_time = str(date_time_obj.time())

        records_list.append({"is_bot": is_bot, "text": text,
                             "correct_date": correct_date, "correct_time": correct_time[:5],
                             "message_id": message_id})

    return records_list
