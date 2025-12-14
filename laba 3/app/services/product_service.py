from uuid import UUID

from app.models import Product

from ..DTO.ProductCreate import ProductCreate
from ..repositories.product_repository import ProductRepository
from ..cache.redis_client import get_redis
from types import SimpleNamespace
import json
from datetime import datetime


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        self._redis = get_redis()
        self.CACHE_PREFIX = "product:"
        self.CACHE_TTL = 600

    async def get_by_id(self, product_id: UUID) -> Product | None:
        if self._redis is not None:
            key = f"{self.CACHE_PREFIX}{product_id}"
            raw = await self._redis.get(key)
            if raw:
                data = json.loads(raw)
                created_at = datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
                updated_at = datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None
                return SimpleNamespace(
                    id=UUID(data["id"]),
                    name=data["name"],
                    quantity=int(data.get("quantity", 0)),
                    created_at=created_at,
                    updated_at=updated_at,
                )

        product = await self.product_repository.get_by_id(product_id)
        if product and self._redis is not None:
            key = f"{self.CACHE_PREFIX}{product_id}"
            payload = {
                "id": str(product.id),
                "name": product.name,
                "quantity": int(product.quantity),
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None,
            }
            await self._redis.setex(key, self.CACHE_TTL, json.dumps(payload))
        return product

    async def get_by_filter(
        self, skip: int = 0, limit: int = 100, **filters
    ) -> list[Product]:
        return await self.product_repository.get_by_filters(skip, limit, **filters)

    async def create(self, product_data: ProductCreate) -> Product:
        product = await self.product_repository.create(product_data)
        if product and self._redis is not None:
            key = f"{self.CACHE_PREFIX}{product.id}"
            payload = {
                "id": str(product.id),
                "name": product.name,
                "quantity": int(product.quantity),
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None,
            }
            await self._redis.setex(key, self.CACHE_TTL, json.dumps(payload))
        return product

    async def update(self, product_id: UUID, product_data: ProductCreate) -> Product:
        product = await self.product_repository.update(product_id, product_data)
        if product and self._redis is not None:
            key = f"{self.CACHE_PREFIX}{product_id}"
            payload = {
                "id": str(product.id),
                "name": product.name,
                "quantity": int(product.quantity),
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None,
            }
            await self._redis.setex(key, self.CACHE_TTL, json.dumps(payload))
        return product

    async def delete(self, product_id: UUID) -> None:
        return await self.product_repository.delete(product_id)
