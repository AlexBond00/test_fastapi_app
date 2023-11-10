
from pprint import pprint
import datetime
from typing import Annotated

import aiohttp
from fastapi import APIRouter, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from starlette.responses import RedirectResponse


class SendMessage(BaseModel):
    message_text: str


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/messages", response_class=HTMLResponse)
async def get_dialogue(request: Request):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080/bots') as result:
            bots = await result.json()

    return templates.TemplateResponse("index.html", {"request": request, "bots": bots})


@router.get("/bots/{bot_id}/")
async def get_dialogue_list(request: Request, bot_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8080/bots/{bot_id}/dialogues') as result:
            dialogues = await result.json()

    return templates.TemplateResponse("dialogues.html", {"request": request, "dialogues": dialogues, "bot_id": bot_id})


@router.get("/dialog/{bot_id}/{chat_id}", response_class=HTMLResponse)
async def choose_dialogue(request: Request, bot_id, chat_id):
    records_list: list = []

    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8080/bots/{bot_id}/dialogues/{chat_id}') as result:
            records = await result.json()
    for record in records:
        is_bot = record.get("json").get("from_user").get("is_bot")
        text = record.get("json").get("text")
        date = record.get("created_at")
        message_id = record.get("message_id")
        # converting a string to a date object
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        correct_date = str(date_time_obj.date())
        correct_time = str(date_time_obj.time())

        records_list.append({"is_bot": is_bot, "text": text,
                             "correct_date": correct_date, "correct_time": correct_time[:5],
                             "message_id": message_id})
    return templates.TemplateResponse("chats.html", {"request": request, "records_list": records_list,
                                                     "chat_id": chat_id, "bot_id": bot_id})


@router.post("/{bot_id}/{chat_id}/")
async def send_message(request: Request,
                       bot_id,
                       chat_id
                       # text: Annotated[str | None, Form()] = None,
                       # files: Annotated[list[UploadFile], File()] = None
                       ):
    print(bot_id)
    print(chat_id)
    # async with aiohttp.ClientSession() as session:
    #     data = aiohttp.FormData()
    #     data.add_field(
    #         name="text",
    #         value=text
    #     )
    #     for file in files:
    #         data.add_field(
    #             name="files",
    #             value=file,
    #             filename="files"
    #         )
    #     result = await session.post(url=f'http://localhost:8080/bots/{bot_id}/dialogues/{chat_id}/SendMessage/',
    #                                 data=data
    #                                 )
    #     print(await result.text())
    return templates.TemplateResponse("send_message.html", {"request": request, "chat_id": chat_id, "bot_id": bot_id})


@router.get("/delete_message/{bot_id}/{chat_id}/{message_id}", response_class=HTMLResponse)
async def delete_message(request: Request, bot_id, chat_id):
    print("Deleted")

    records_list: list = []
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8080/bots/{bot_id}/dialogues/{chat_id}') as result:
            records = await result.json()
    for record in records:
        is_bot = record.get("json").get("from_user").get("is_bot")
        text = record.get("json").get("text")
        date = record.get("created_at")
        message_id = record.get("message_id")
        # converting a string to a date object
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        correct_date = str(date_time_obj.date())
        correct_time = str(date_time_obj.time())

        records_list.append({"is_bot": is_bot, "text": text,
                             "correct_date": correct_date, "correct_time": correct_time[:5],
                             "message_id": message_id})
    return templates.TemplateResponse("chats.html", {"request": request, "records_list": records_list,
                                                     "chat_id": chat_id, "bot_id": bot_id})
