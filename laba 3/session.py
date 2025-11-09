from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql+asyncpg://postgres:password@localhost:5432/python?async_fallback=True",
    echo=True
)

session_factory = sessionmaker(engine)