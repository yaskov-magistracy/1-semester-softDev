from datetime import datetime
from uuid import UUID
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Order
from ..DTO.OrderCreate import OrderCreate


class OrderRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> Order | None:
        result = await self.session.execute(
            select(Order)
            .where(Order.id == id))
        
        return result.scalars().one_or_none()

    
    async def get_by_filters(self, skip: int = 0, limit: int = 100, **filters) -> list[Order]:
        result = await self.session.execute(
            select(Order)
            .filter_by(**filters)
            .offset(skip)
            .limit(limit))
        
        return result.scalars().all()

    async def create(self, data: OrderCreate) -> Order:
        order = Order(**data.model_dump())
        self.session.add(order)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def update(self, id: UUID, order_update: OrderCreate) -> Order:
        result = await self.session.execute(
            select(Order)
            .where(Order.id == id))
        order = result.scalar_one_or_none()
        if not order:
            raise Exception("Where is no entity with same Id")
        
        if order_update.date is not None:
            order.date = order_update.date
        
        if order_update.user_id is not None:
            order.user_id = order_update.user_id
        
        if order_update.address_id is not None:
            order.address_id = order_update.address_id
        
        if order_update.product_id is not None:
            order.product_id = order_update.product_id
        
        order.updated_at = datetime.now()
        
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def delete(self, id: UUID) -> None:
        await self.session.execute(
            delete(Order).where(Order.id == id))
        await self.session.commit()