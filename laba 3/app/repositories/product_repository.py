from datetime import datetime
from uuid import UUID
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Product
from ..DTO.ProductCreate import ProductCreate

class ProductRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> Product | None:
        result = await self.session.execute(
            select(Product)
            .where(Product.id == id))
        
        return result.scalars().one_or_none()

    
    async def get_by_filters(self, skip: int = 0, limit: int = 100, **filters) -> list[Product]:
        result = await self.session.execute(
            select(Product)
            .filter_by(**filters)
            .offset(skip)
            .limit(limit))
        
        return result.scalars().all()

    async def create(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.session.add(product)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update(self, id: UUID, product_update: ProductCreate) -> Product:
        result = await self.session.execute(
            select(Product)
            .where(Product.id == id))
        product = result.scalar_one_or_none()
        if not product:
            raise Exception("Where is no entity with same Id")
        
        if product_update.name is not None:
            product.name = product_update.name
        
        if product_update.quantity is not None:
            product.quantity = product_update.quantity
        
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, id: UUID) -> None:
        await self.session.execute(
            delete(Product).where(Product.id == id))
        await self.session.commit()