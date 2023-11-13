from pprint import pprint
import datetime
from typing import Annotated

import aiohttp
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from starlette.responses import RedirectResponse, JSONResponse

from .response_parsing import response_parsing
from .user_token_verify import validate_user_token


class SendMessage(BaseModel):
    message_text: str


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post("/messages", response_class=HTMLResponse)
async def get_dialogue(request: Request,
                       user_token: Annotated[dict, Depends(validate_user_token)]
                       ):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8888/bots') as result:
            bots = await result.json()

    return templates.TemplateResponse("index.html", {"request": request, "bots": bots})


@router.get("/bots/{bot_id}/")
async def get_dialogue_list(request: Request,
                            bot_id,
                            user_token: Annotated[dict, Depends(validate_user_token)]
                            ):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8888/bots/{bot_id}/dialogues/') as result:
            dialogues = await result.json()

    return templates.TemplateResponse("dialogues.html", {"request": request, "dialogues": dialogues, "bot_id": bot_id})


@router.get("/dialog/{bot_id}/{chat_id}", response_class=HTMLResponse)
async def choose_dialogue(request: Request,
                          bot_id,
                          chat_id,
                          user_token: Annotated[dict, Depends(validate_user_token)]
                          ):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8888/bots/{bot_id}/dialogues/{chat_id}') as result:
            records = await result.json()

    records_list = await response_parsing(records)

    return templates.TemplateResponse("chats.html", {"request": request, "records_list": records_list,
                                                     "chat_id": chat_id, "bot_id": bot_id})


@router.post("/{bot_id}/{chat_id}/")
async def send_message(request: Request,
                       bot_id,
                       chat_id,
                       user_token: Annotated[dict, Depends(validate_user_token)]
                       ):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8888/bots/{bot_id}/dialogues/{chat_id}') as result:
            records = await result.json()

    records_list = await response_parsing(records)

    return templates.TemplateResponse("chats.html", {"request": request, "records_list": records_list,
                                                     "chat_id": chat_id, "bot_id": bot_id})


@router.get("/delete_message/{bot_id}/{chat_id}/{message_id}", response_class=HTMLResponse)
async def delete_message(request: Request,
                         bot_id,
                         chat_id,
                         user_token: Annotated[dict, Depends(validate_user_token)]
                         ):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8888/bots/{bot_id}/dialogues/{chat_id}') as result:
            records = await result.json()

    records_list = await response_parsing(records)

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
