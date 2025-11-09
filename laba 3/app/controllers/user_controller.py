from app.services.user_service import *
from litestar import Litestar, get, post, put, delete, patch
from litestar.di import Provide
from litestar.controller import Controller
from .UserResponse import *

class UserController(Controller):
    path = "/users"
    dependencies = {"user_service": Provide("user_service")}

    @get("/{user_id:int}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: uuid,
    ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise Exception(detail=f"User with ID {user_id} not found")
        return self.map_user_to_response(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
    ) -> list[UserResponse]:
        """Получить всех пользователей"""
        users = await user_service.get_by_filter()
        return list(map(self.map_user_to_response, users))
        

    @post()
    async def create_user(
        self,
        user_service: UserService,
        user_data: UserCreate,
        ) -> UserResponse:
        """Добавить пользователя"""
        user = await user_service.create(user_data)
        return self.map_user_to_response(user)

    @delete("/{user_id:int}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: int,
    ) -> None:
        """Удалить пользователя"""
        await user_service.delete(user_id)

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: int,
        user_data: UserCreate,
    ) -> UserResponse:
        """Обновить пользователя"""
        updated = await user_service.update(user_id, user_data)
        return self.map_user_to_response(updated)


    def map_user_to_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            login=user.login,
            email=user.email,
            description=user.description or ""
        )