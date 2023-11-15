from typing import Annotated
from uuid import UUID
import aiohttp
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from tortoise.fields import UUIDField
from fastapi.responses import Response
from api.tortoise_models.token_model import Token
from .response_parsing import response_parsing
from .user_token_verify import validate_user_token
import binascii
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


@router.post("/dialogues/{bot_id}/{chat_id}", response_class=HTMLResponse)
async def choose_dialogue(request: Request,
                          bot_id,
                          chat_id,
                          user_token: Annotated[dict, Depends(validate_user_token)],
                          offset: int = 0,
                          limit: int = 10
                          ):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8888/bots/{bot_id}/dialogues/{chat_id}/messages') as result:
            records = await result.json()

    records_list = await response_parsing(records)

    return templates.TemplateResponse("chats.html", {"request": request, "records_list": records_list,
                                                     "chat_id": chat_id, "bot_id": bot_id, "offset": offset,
                                                     "limit": limit})


@router.get("/verification/")
async def verification(request: Request):
    return templates.TemplateResponse("verification.html", {"request": request})


@router.post("/verification_info/")
async def verification(user_token: Annotated[str | None, Form()] = None):
    error = "Invalid token"
    token_exist: bool = await Token.exists(token=user_token)
    if not token_exist:
        return error
    response = RedirectResponse("/messages/")
    response.set_cookie(key="user_token", value=user_token)
    return response
