import asyncio
import json
import logging
import sys

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from tortoise import Tortoise

from api.api_router import api_router
from frontend.front_api import router

logging.basicConfig(level=logging.INFO, stream=sys.stderr)


async def init_tortoise():
    with open("db_config.json") as f:
        json_data = json.load(f)

    await Tortoise.init(
        config=json_data,
        use_tz=True
    )
    await Tortoise.generate_schemas(safe=True)


app = FastAPI()
app.include_router(api_router)
app.include_router(router)
app.mount(
    "/static", StaticFiles(directory="static", html=True), name="static"
)


async def main():
    await init_tortoise()
    config = uvicorn.Config("app:app", port=8888, reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
