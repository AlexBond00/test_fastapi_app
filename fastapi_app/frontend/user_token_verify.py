from http import HTTPStatus
from typing import Annotated, Union
from uuid import UUID

from fastapi import Cookie, HTTPException, Form

from api.tortoise_models.token_model import Token

from api.tortoise_models.token_model import Token


async def validate_user_token(
        user_token: Annotated[str | None, Cookie()] = None
) -> None:
    """Token validator."""
    exception = HTTPException(status_code=HTTPStatus.FORBIDDEN)
    exception.detail = {"error": "Permission denied"}
    try:
        uuid_token = UUID(user_token)
    except ValueError as e:
        detail = {"message": str(e)}
        exception.detail.update(detail)
        raise exception
    if not await Token.filter(token=uuid_token).exists():
        detail = {"message": "Invalid token"}
        exception.detail.update(detail)
        raise exception
