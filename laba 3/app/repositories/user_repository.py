from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..DTO.UserCreate import UserCreate
from ..DTO.UserUpdate import UserUpdate
from ..models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> User | None:
        result = await self.session.execute(select(User).where(User.id == id))

        return result.scalars().one_or_none()

    async def get_by_email(self, email) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))

        return result.scalars().one_or_none()

    async def get_by_filters(
        self, skip: int = 0, limit: int = 100, **filters
    ) -> list[User]:
        result = await self.session.execute(
            select(User).filter_by(**filters).offset(skip).limit(limit)
        )

        return result.scalars().all()

    async def create(self, data: UserCreate) -> User:
        user = User(login=data.login, email=data.email, description=data.description)
        self.session.add(user)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, id: UUID, user_update: UserUpdate) -> User:
        result = await self.session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        if not user:
            raise Exception("Where is no entity with same Id")

        if user_update.login is not None and user_update.login != "":
            user.login = user_update.login

        if user_update.email is not None and user_update.email != "":
            user.email = user_update.email

        if user_update.description is not None and user_update.description != "":
            user.description = user_update.description

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, id: UUID) -> None:
        await self.session.execute(delete(User).where(User.id == id))
        await self.session.commit()
