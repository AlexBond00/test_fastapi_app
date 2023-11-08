# from fastapi import APIRouter, Request
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
#
#
#
# from ..api.api_router import get_messages
# from fastapi_app.models.dialogue_model import DialogueModel
# from fastapi_app.models.message_model import MessageModel
#
# router = APIRouter()
#
# router.mount("/static", StaticFiles(directory="frontend/static", html=True), name="static")
#
#
# templates = Jinja2Templates(directory="templates")
#
#
# @router.get("/messages", response_class=HTMLResponse)
# async def read_item(request: Request):
#     records_message: list[DialogueModel] = await get_dialogue_list()
#
#     print(records_message)
#     return templates.TemplateResponse("index.html", {"request": request, "dialog_list": records_message})
#
#
# @router.get("/dialog/{chat_id}", response_class=HTMLResponse)
# async def read_item(request: Request, chat_id):
#     records_message: list[MessageModel] = await MessageModel.filter(chat_id=chat_id).all()
#     print(records_message)
#     return templates.TemplateResponse("chat.html", {"request": request, "records_message": records_message})
#
