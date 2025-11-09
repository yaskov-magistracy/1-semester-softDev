import os
from litestar import Litestar
from litestar.di import Provide
import uvicorn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from typing import AsyncGenerator
from app.services.user_service import *
from app.repositories.user_repository import *
from app.controllers.user_controller import *

# Настройка базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/python?async_fallback=True")

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_factory = async_sessionmaker(
    engine,     
    expire_on_commit=False,
    class_=AsyncSession)

async def provide_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Провайдер сессии базы данных"""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    """Провайдер репозитория пользователей"""
    return UserRepository(db_session)

async def provide_user_service(user_repository: UserRepository) -> UserService:
    """Провайдер сервиса пользователей"""
    return UserService(user_repository)

app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
    },
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
