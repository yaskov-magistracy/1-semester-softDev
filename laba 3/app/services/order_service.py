from ..repositories.order_repository import OrderRepository
from ..DTO.OrderCreate import OrderCreate
from uuid import UUID
from app.models import Order

class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def get_by_id(self, order_id: UUID) -> Order | None:
        order = await self.order_repository.get_by_id(order_id)
        return order

    async def get_by_filter(self, skip: int = 0, limit: int = 100, **filters) -> list[Order]:
        return await self.order_repository.get_by_filters(skip, limit, **filters)

    async def create(self, order_data: OrderCreate) -> Order:
        return await self.order_repository.create(order_data)

    async def update(self, order_id: UUID, order_data: OrderCreate) -> Order:
        return await self.order_repository.update(order_id, order_data)

    async def delete(self, order_id: UUID) -> None:
        return await self.order_repository.delete(order_id)