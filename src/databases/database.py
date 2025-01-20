from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from configs.config import db_settings


SQLALCHEMY_MASTER_DATABASE_URL = (
    "postgresql+asyncpg://"
    f"{db_settings.POSTGRES_USER}:"
    f"{db_settings.POSTGRES_PASSWORD}@"
    f"{db_settings.POSTGRES_HOST}:"
    f"{db_settings.POSTGRES_PORT}/"
    f"{db_settings.POSTGRES_DB}"
)


master_engine = create_async_engine(
    url=SQLALCHEMY_MASTER_DATABASE_URL,
    pool_size=40,
    max_overflow=10,
    echo=True,
    pool_recycle=1800,
)

master_session = async_sessionmaker(
    master_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_master_session() -> AsyncGenerator[AsyncSession, None]:
    async with master_session() as session:
        yield session
