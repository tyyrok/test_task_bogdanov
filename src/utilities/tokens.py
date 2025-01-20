from datetime import timedelta
from typing import TypedDict, Union

from configs.config import jwt_settings
from schemas.token import TokenAccessRefresh
from security.token import access_security, refresh_security


class TokenSubject(TypedDict):
    id: int
    global_id: int


class AdminTokenSubject(TypedDict):
    id: int
    role: str


async def create_tokens(
    subject: Union[TokenSubject, AdminTokenSubject],
) -> TokenAccessRefresh:
    access_token = await create_access_token(subject)
    refresh_token = await create_refresh_token(subject)
    return TokenAccessRefresh(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


async def create_access_token(
    subject: Union[TokenSubject, AdminTokenSubject],
) -> str:
    return access_security.create_access_token(subject=subject)


async def create_refresh_token(
    subject: Union[TokenSubject, AdminTokenSubject],
) -> str:
    return refresh_security.create_refresh_token(
        subject=subject,
        expires_delta=timedelta(
            minutes=jwt_settings.JWT_REFRESH_TOKEN_EXPIRES
        ),
    )
