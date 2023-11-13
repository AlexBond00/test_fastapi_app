from http import HTTPStatus
from typing import Annotated

from fastapi import Cookie, HTTPException


async def validate_user_token(
        user_token: Annotated[str | None, Cookie()] = None):
    if user_token != "fewrg44ff3rvg343f4gvrrr":
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="You don't have access!"
        )