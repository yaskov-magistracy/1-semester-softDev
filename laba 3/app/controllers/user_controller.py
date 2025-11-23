from uuid import UUID

from litestar import delete, get, post, put
from litestar.controller import Controller
from litestar.params import Body

from ..DTO.UserCreate import UserCreate
from ..DTO.UserUpdate import UserUpdate
from ..models import User
from ..services.user_service import UserService
from .UserResponse import UserResponse


class UserController(Controller):
    path = "/users"

    @get("/{user_id:uuid}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: UUID,
    ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        return self.map_user_to_response(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
    ) -> list[UserResponse]:
        """Получить всех пользователей"""
        users = await user_service.get_by_filter()
        return [self.map_user_to_response(user) for user in users]

    @post("/")
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate = Body(),
    ) -> UserResponse:
        """Добавить пользователя"""
        user = await user_service.create(data)
        return self.map_user_to_response(user)

    @delete("/{user_id:uuid}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: UUID,
    ) -> None:
        """Удалить пользователя"""
        await user_service.delete(user_id)

    @put("/{user_id:uuid}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: UUID,
        data: UserUpdate = Body(),
    ) -> UserResponse:
        """Обновить пользователя"""
        updated = await user_service.update(user_id, data)
        return self.map_user_to_response(updated)

    def map_user_to_response(self, user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            login=user.login,
            email=user.email,
            description=user.description or "",
        )
