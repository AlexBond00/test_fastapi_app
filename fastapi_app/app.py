import asyncio
import json

import uvicorn
from fastapi import FastAPI
from tortoise import Tortoise

from api.api_router import api_router


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


async def main():
    await init_tortoise()
    config = uvicorn.Config("app:app", port=8080)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
