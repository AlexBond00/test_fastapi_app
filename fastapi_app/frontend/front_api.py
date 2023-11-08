from pprint import pprint

import aiohttp
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/messages", response_class=HTMLResponse)
async def read_item(request: Request):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080/dialogue') as result:
            record = await result.json()
    return templates.TemplateResponse("index.html", {"request": request, "records_dialog": record})


@router.get("/dialog/{bot_id}/{chat_id}", response_class=HTMLResponse)
async def read_item(request: Request, bot_id, chat_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8080/dialogue/{bot_id}/{chat_id}/') as result:
            records = await result.json()
    records_list = []
    import datetime
    for record in records:
        is_bot = record.get("json").get("from_user").get("is_bot")
        text = record.get("json").get("text")
        date = record.get("created_at")
        # converting a string to a date object
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        correct_date = str(date_time_obj.date())
        correct_time = str(date_time_obj.time())

        pprint(record)
        records_list.append({"is_bot": is_bot, "text": text,
                             "correct_date": correct_date, "correct_time": correct_time[:5]
                             })
    return templates.TemplateResponse("chat.html", {"request": request, "records_list": records_list, "chat_id": chat_id})

