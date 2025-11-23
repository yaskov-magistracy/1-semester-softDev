import uuid

from ..DTO.UserCreate import UserCreate
from ..DTO.UserUpdate import UserUpdate
from ..models import User
from ..repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        user = await self.user_repository.get_by_id(user_id)
        return user

    async def get_by_filter(
        self, skip: int = 0, limit: int = 100, **filters
    ) -> list[User]:
        return await self.user_repository.get_by_filters(skip, limit, **filters)

    async def create(self, user_data: UserCreate) -> User:
        return await self.user_repository.create(user_data)

    async def update(self, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        return await self.user_repository.update(user_id, user_data)

    async def delete(self, user_id: uuid.UUID) -> None:
        return await self.user_repository.delete(user_id)
