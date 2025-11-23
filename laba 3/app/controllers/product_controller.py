from uuid import UUID

from litestar import delete, get, post, put
from litestar.controller import Controller
from litestar.params import Body

from ..DTO.ProductCreate import ProductCreate
from ..services.product_service import ProductService
from .ProductResponse import ProductResponse


class ProductController(Controller):
    path = "/products"

    @get("/{product_id:uuid}")
    async def get_product_by_id(
        self,
        product_service: ProductService,
        product_id: UUID,
    ) -> ProductResponse:
        """Получить продукт по ID"""
        product = await product_service.get_by_id(product_id)
        if not product:
            raise Exception(detail=f"Product with ID {product_id} not found")
        return self.map_product_to_response(product)

    @get()
    async def get_all_products(
        self,
        product_service: ProductService,
    ) -> list[ProductResponse]:
        """Получить все продукты"""
        products = await product_service.get_by_filter()
        return [self.map_product_to_response(product) for product in products]

    @post("/")
    async def create_product(
        self,
        product_service: ProductService,
        data: ProductCreate = Body(),
    ) -> ProductResponse:
        """Добавить продукт"""
        product = await product_service.create(data)
        return self.map_product_to_response(product)

    @delete("/{product_id:uuid}")
    async def delete_product(
        self,
        product_service: ProductService,
        product_id: UUID,
    ) -> None:
        """Удалить продукт"""
        await product_service.delete(product_id)

    @put("/{product_id:uuid}")
    async def update_product(
        self,
        product_service: ProductService,
        product_id: UUID,
        data: ProductCreate = Body(),
    ) -> ProductResponse:
        """Обновить продукт"""
        updated = await product_service.update(product_id, data)
        return self.map_product_to_response(updated)

    def map_product_to_response(self, product) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            name=product.name,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )
