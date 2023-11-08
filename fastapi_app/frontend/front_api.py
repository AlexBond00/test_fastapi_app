from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from fastapi_app.message_model import MessageModel



router = APIRouter()

router.mount("/static", StaticFiles(directory="static", html=True), name="static")


templates = Jinja2Templates(directory="templates")


@router.get("/messages", response_class=HTMLResponse)
async def read_item(request: Request):
    records_message: list[MessageModel] = await MessageModel.all()
    dialog_list = set()
    for record in records_message:
        dialog_list.add(record.chat_id)

    print(dialog_list)
    return templates.TemplateResponse("index.html", {"request": request, "dialog_list": dialog_list})


@router.get("/dialog/{chat_id}", response_class=HTMLResponse)
async def read_item(request: Request, chat_id):
    records_message: list[MessageModel] = await MessageModel.filter(chat_id=chat_id).all()
    print(records_message)
    return templates.TemplateResponse("chat.html", {"request": request, "records_message": records_message})

