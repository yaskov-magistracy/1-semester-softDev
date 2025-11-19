from ..repositories.product_repository import ProductRepository
from ..DTO.ProductCreate import ProductCreate
from uuid import UUID
from app.models import Product

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_by_id(self, product_id: UUID) -> Product | None:
        product = await self.product_repository.get_by_id(product_id)
        return product

    async def get_by_filter(self, skip: int = 0, limit: int = 100, **filters) -> list[Product]:
        return await self.product_repository.get_by_filters(skip, limit, **filters)

    async def create(self, product_data: ProductCreate) -> Product:
        return await self.product_repository.create(product_data)

    async def update(self, product_id: UUID, product_data: ProductCreate) -> Product:
        return await self.product_repository.update(product_id, product_data)

    async def delete(self, product_id: UUID) -> None:
        return await self.product_repository.delete(product_id)