from typing import Annotated
from ..services.address_service import *
from litestar import Litestar, get, post, put, delete, patch
from litestar.di import Provide
from litestar.params import Body
from litestar.dto import DTOData
from litestar.controller import Controller
from .AddressResponse import *
from uuid import UUID

class AddressController(Controller):
    path = "/addresses"

    @get("/{address_id:uuid}")
    async def get_address_by_id(
        self,
        address_service: AddressService,
        address_id: UUID,
    ) -> AddressResponse:
        """Получить адрес по ID"""
        address = await address_service.get_by_id(address_id)
        if not address:
            raise Exception(detail=f"Address with ID {address_id} not found")
        return self.map_address_to_response(address)

    @get()
    async def get_all_addresses(
        self,
        address_service: AddressService,
    ) -> list[AddressResponse]:
        """Получить все адреса"""
        addresses = await address_service.get_by_filter()
        return [self.map_address_to_response(address) for address in addresses]
        

    @post("/")
    async def create_address(
        self,
        address_service: AddressService,
        data: AddressCreate = Body(),
        ) -> AddressResponse:
        """Добавить адрес"""
        address = await address_service.create(data)
        return self.map_address_to_response(address)

    @delete("/{address_id:uuid}")
    async def delete_address(
        self,
        address_service: AddressService,
        address_id: UUID,
    ) -> None:
        """Удалить адрес"""
        await address_service.delete(address_id)

    @put("/{address_id:uuid}")
    async def update_address(
        self,
        address_service: AddressService,
        address_id: UUID,
        data: AddressCreate = Body(),
    ) -> AddressResponse:
        """Обновить адрес"""
        updated = await address_service.update(address_id, data)
        return self.map_address_to_response(updated)

    def map_address_to_response(self, address: Address) -> AddressResponse:
        return AddressResponse(
            id=address.id,
            user_id=address.user_id,
            street=address.street,
            created_at=address.created_at,
            updated_at=address.updated_at
        )