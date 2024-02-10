from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import DatabaseSettings


class AsyncDatabase:
    engine: AsyncEngine
    session_maker: async_sessionmaker[AsyncSession]

    def __init__(self, settings: DatabaseSettings):
        connection_url = URL.create(
            drivername="postgresql+asyncpg",
            username=settings.DB_USER,
            password=settings.DB_PASS,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
        )
        self.engine = create_async_engine(
            url=connection_url,
            echo=True,
            isolation_level="AUTOCOMMIT",
        )
        self.session_maker = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )
        pass

    async def clean_up(self):
        await self.engine.dispose()
        pass

    pass
