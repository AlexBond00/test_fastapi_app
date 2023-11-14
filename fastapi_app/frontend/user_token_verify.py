from http import HTTPStatus
from typing import Annotated

from fastapi import Cookie, HTTPException

from api.tortoise_models.token_model import Token


async def validate_user_token(
        user_token: Annotated[str | None, Cookie()] = None):
    list_tokens: list[str] = []
    tokens: list[Token] = await Token.all()
    for token in tokens:
        list_tokens.append(str(token.token))
    if not(user_token in list_tokens):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="You don't have access!"
        )
