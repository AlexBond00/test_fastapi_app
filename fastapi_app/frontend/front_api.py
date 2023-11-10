
from pprint import pprint
import datetime
from typing import Annotated

import aiohttp
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from starlette.responses import RedirectResponse, JSONResponse


class SendMessage(BaseModel):
    message_text: str


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post("/messages", response_class=HTMLResponse)
async def get_dialogue(request: Request):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8888/bots') as result:
            bots = await result.json()

    return templates.TemplateResponse("index.html", {"request": request, "bots": bots})


@router.get("/bots/{bot_id}/")
async def get_dialogue_list(request: Request, bot_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8888/bots/{bot_id}/dialogues/') as result:
            dialogues = await result.json()

    return templates.TemplateResponse("dialogues.html", {"request": request, "dialogues": dialogues, "bot_id": bot_id})


@router.get("/dialog/{bot_id}/{chat_id}", response_class=HTMLResponse)
async def choose_dialogue(request: Request, bot_id, chat_id):
    records_list: list = []

    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8888/bots/{bot_id}/dialogues/{chat_id}') as result:
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
                       ):
    return templates.TemplateResponse("send_message.html", {"request": request, "chat_id": chat_id, "bot_id": bot_id})


@router.get("/delete_message/{bot_id}/{chat_id}/{message_id}", response_class=HTMLResponse)
async def delete_message(request: Request, bot_id, chat_id):

    records_list: list = []
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8888/bots/{bot_id}/dialogues/{chat_id}') as result:
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


@router.get("/verification")
def verification(request: Request):
    return templates.TemplateResponse("verification.html", {"request": request})


@router.post("/verification_info")
def verification(user_token: str = Form(default=None)):
    if user_token == "fewrg44ff3rvg343f4gvrrr":
        content = {"user_token": user_token}
        response = JSONResponse(content=content)
        response.set_cookie(key="user_token", value=user_token)
        return RedirectResponse("/messages")
    else:
        return "Токен неверный"

