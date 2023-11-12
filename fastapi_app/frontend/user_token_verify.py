from typing import Annotated

from fastapi import Cookie, HTTPException



async def validate_user_token(user_token: Annotated[str | None, Cookie()] = None):
    if not(user_token == "fewrg44ff3rvg343f4gvrrr"):
        raise HTTPException(status_code=400, detail="You don't have access!")