from pydantic import BaseModel


class ServiceInfo(BaseModel):
    name_service: str
    version: str


class SettingsInfo(BaseModel):
    JWT_ACCESS_TOKEN_EXPIRES: int
    JWT_REFRESH_TOKEN_EXPIRES: int
