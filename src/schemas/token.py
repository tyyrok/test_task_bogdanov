from pydantic import BaseModel  # noqa: A005, RUF100


class UserLogin(BaseModel):
    user_uid: str
    session_uid: str


class TokenPayload(BaseModel):
    id: int


class TokenAccessRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
