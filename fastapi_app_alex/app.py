import asyncio
import json
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from tortoise import Tortoise

from message_model import MessageModel


async def init_tortoise():
    with open("db_config.json") as f:
        json_data = json.load(f)

    await Tortoise.init(
        config=json_data,
        use_tz=True
    )
    await Tortoise.generate_schemas(safe=True)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/messages", response_class=HTMLResponse)
async def read_item(request: Request):
    records_message: list[MessageModel] = await MessageModel.all()
    dialog_list = set()
    for record in records_message:
        dialog_list.add(record.chat_id)

    print(dialog_list)
    return templates.TemplateResponse("index.html", {"request": request, "dialog_list": dialog_list})


@app.get("/dialog/{chat_id}", response_class=HTMLResponse)
async def read_item(request: Request, chat_id):
    records_message: list[MessageModel] = await MessageModel.filter(chat_id=chat_id).all()
    print(records_message)
    return templates.TemplateResponse("chat.html", {"request": request, "records_message": records_message})



async def main():
    await init_tortoise()
    config = uvicorn.Config("app:app", port=8080)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
