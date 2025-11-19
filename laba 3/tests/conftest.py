import pytest
import pytest_asyncio
from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from sqlalchemy import text, inspect
from app.main import app
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.address_repository import AddressRepository
# Тестовая база данных
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def engine():
    return create_async_engine(TEST_DATABASE_URL, echo=False)


@pytest_asyncio.fixture(scope="session")
async def tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def session(engine, tables):
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session

@pytest_asyncio.fixture(autouse=True)
async def clean_db(session: AsyncSession):
    yield

    engine: AsyncEngine = session.bind

    async with engine.connect() as conn:
        dialect = conn.engine.dialect.name
        def get_tables(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.get_table_names()
        tables = await conn.run_sync(get_tables)

        if dialect == "sqlite":
            await conn.execute(text("PRAGMA foreign_keys = OFF;"))
            for table in tables:
                await conn.execute(text(f"DELETE FROM {table};"))
            await conn.execute(text("PRAGMA foreign_keys = ON;"))
        else:
            table_list = ", ".join(f'"{t}"' for t in tables)
            await conn.execute(
                text(f"TRUNCATE {table_list} RESTART IDENTITY CASCADE;")
            )

        await conn.commit()


@pytest.fixture
def user_repository(session):
    return UserRepository(session)


@pytest.fixture
def product_repository(session):
    return ProductRepository(session)


@pytest.fixture
def order_repository(session):
    return OrderRepository(session)

@pytest.fixture
def address_repository(session):
    return AddressRepository(session)

@pytest.fixture
def client():
    return TestClient(app=app)