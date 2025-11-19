import os
from litestar import Litestar
from litestar.di import Provide
import uvicorn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from typing import AsyncGenerator
from .services.user_service import *
from .repositories.user_repository import *
from .controllers.user_controller import *
from .services.order_service import *
from .repositories.order_repository import *
from .controllers.order_controller import *
from .services.product_service import *
from .repositories.product_repository import *
from .controllers.product_controller import *
from .services.address_service import *
from .repositories.address_repository import *
from .controllers.address_controller import *

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

async def provide_order_repository(db_session: AsyncSession) -> OrderRepository:
    """Провайдер репозитория заказов"""
    return OrderRepository(db_session)

async def provide_order_service(order_repository: OrderRepository) -> OrderService:
    """Провайдер сервиса заказов"""
    return OrderService(order_repository)

async def provide_product_repository(db_session: AsyncSession) -> ProductRepository:
    """Провайдер репозитория продуктов"""
    return ProductRepository(db_session)

async def provide_product_service(product_repository: ProductRepository) -> ProductService:
    """Провайдер сервиса продуктов"""
    return ProductService(product_repository)

async def provide_address_repository(db_session: AsyncSession) -> AddressRepository:
    """Провайдер репозитория адресов"""
    return AddressRepository(db_session)

async def provide_address_service(address_repository: AddressRepository) -> AddressService:
    """Провайдер сервиса адресов"""
    return AddressService(address_repository)

app = Litestar(
    route_handlers=[UserController, OrderController, ProductController, AddressController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
        "order_repository": Provide(provide_order_repository),
        "order_service": Provide(provide_order_service),
        "product_repository": Provide(provide_product_repository),
        "product_service": Provide(provide_product_service),
        "address_repository": Provide(provide_address_repository),
        "address_service": Provide(provide_address_service),
    },
    debug=True
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)