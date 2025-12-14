import uuid
import json
from types import SimpleNamespace
from datetime import datetime

from ..DTO.UserCreate import UserCreate
from ..DTO.UserUpdate import UserUpdate
from ..models import User
from ..repositories.user_repository import UserRepository
from ..cache.redis_client import get_redis


class UserService:
    CACHE_PREFIX = "user:"
    CACHE_TTL = 3600

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self._redis = get_redis()

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        if self._redis is not None:
            key = f"{self.CACHE_PREFIX}{user_id}"
            raw = await self._redis.get(key)
            if raw:
                data = json.loads(raw)
                return SimpleNamespace(
                    id=uuid.UUID(data["id"]),
                    login=data["login"],
                    email=data["email"],
                    description=data.get("description", ""),
                )

        user = await self.user_repository.get_by_id(user_id)
        if user and self._redis is not None:
            key = f"{self.CACHE_PREFIX}{user_id}"
            payload = {
                "id": str(user.id),
                "login": user.login,
                "email": user.email,
                "description": user.description or "",
            }
            await self._redis.setex(key, self.CACHE_TTL, json.dumps(payload))
        return user

    async def get_by_filter(
        self, skip: int = 0, limit: int = 100, **filters
    ) -> list[User]:
        return await self.user_repository.get_by_filters(skip, limit, **filters)

    async def create(self, user_data: UserCreate) -> User:
        user = await self.user_repository.create(user_data)
        if user and self._redis is not None:
            key = f"{self.CACHE_PREFIX}{user.id}"
            payload = {
                "id": str(user.id),
                "login": user.login,
                "email": user.email,
                "description": user.description or "",
            }
            await self._redis.setex(key, self.CACHE_TTL, json.dumps(payload))
        return user

    async def update(self, user_id: uuid.UUID, user_data: UserUpdate) -> User:
        user = await self.user_repository.update(user_id, user_data)
        if self._redis is not None:
            key = f"{self.CACHE_PREFIX}{user_id}"
            await self._redis.delete(key)
        return user

    async def delete(self, user_id: uuid.UUID) -> None:
        if self._redis is not None:
            key = f"{self.CACHE_PREFIX}{user_id}"
            await self._redis.delete(key)
        return await self.user_repository.delete(user_id)
