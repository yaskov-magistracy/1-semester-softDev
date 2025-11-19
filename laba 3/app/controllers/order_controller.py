from typing import Annotated
from ..services.order_service import OrderService
from litestar import Litestar, get, post, put, delete, patch
from litestar.di import Provide
from litestar.params import Body
from litestar.dto import DTOData
from litestar.controller import Controller
from .OrderResponse import OrderResponse
from ..DTO.OrderCreate import OrderCreate
from uuid import UUID

class OrderController(Controller):
    path = "/orders"

    @get("/{order_id:uuid}")
    async def get_order_by_id(
        self,
        order_service: OrderService,
        order_id: UUID,
    ) -> OrderResponse:
        """Получить заказ по ID"""
        order = await order_service.get_by_id(order_id)
        if not order:
            raise Exception(detail=f"Order with ID {order_id} not found")
        return self.map_order_to_response(order)

    @get()
    async def get_all_orders(
        self,
        order_service: OrderService,
    ) -> list[OrderResponse]:
        """Получить все заказы"""
        orders = await order_service.get_by_filter()
        return [self.map_order_to_response(order) for order in orders]
        

    @post("/")
    async def create_order(
        self,
        order_service: OrderService,
        data: OrderCreate = Body(),
        ) -> OrderResponse:
        """Добавить заказ"""
        order = await order_service.create(data)
        return self.map_order_to_response(order)

    @delete("/{order_id:uuid}")
    async def delete_order(
        self,
        order_service: OrderService,
        order_id: UUID,
    ) -> None:
        """Удалить заказ"""
        await order_service.delete(order_id)

    @put("/{order_id:uuid}")
    async def update_order(
        self,
        order_service: OrderService,
        order_id: UUID,
        data: OrderCreate = Body(),
    ) -> OrderResponse:
        """Обновить заказ"""
        updated = await order_service.update(order_id, data)
        return self.map_order_to_response(updated)

    def map_order_to_response(self, order) -> OrderResponse:
        return OrderResponse(
            id=order.id,
            date=order.date,
            user_id=order.user_id,
            address_id=order.address_id,
            product_id=order.product_id,
            created_at=order.created_at,
            updated_at=order.updated_at
        )