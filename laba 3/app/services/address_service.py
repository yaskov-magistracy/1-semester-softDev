from uuid import UUID

from app.models import Address

from ..DTO.AddressCreate import AddressCreate
from ..repositories.address_repository import AddressRepository


class AddressService:
    def __init__(self, address_repository: AddressRepository):
        self.address_repository = address_repository

    async def get_by_id(self, address_id: UUID) -> Address | None:
        address = await self.address_repository.get_by_id(address_id)
        return address

    async def get_by_filter(
        self, skip: int = 0, limit: int = 100, **filters
    ) -> list[Address]:
        return await self.address_repository.get_by_filters(skip, limit, **filters)

    async def create(self, address_data: AddressCreate) -> Address:
        return await self.address_repository.create(address_data)

    async def update(self, address_id: UUID, address_data: AddressCreate) -> Address:
        return await self.address_repository.update(address_id, address_data)

    async def delete(self, address_id: UUID) -> None:
        return await self.address_repository.delete(address_id)
