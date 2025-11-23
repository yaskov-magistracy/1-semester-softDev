from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..DTO.AddressCreate import AddressCreate
from ..models import Address


class AddressRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> Address | None:
        result = await self.session.execute(select(Address).where(Address.id == id))

        return result.scalars().one_or_none()

    async def get_by_filters(
        self, skip: int = 0, limit: int = 100, **filters
    ) -> list[Address]:
        result = await self.session.execute(
            select(Address).filter_by(**filters).offset(skip).limit(limit)
        )

        return result.scalars().all()

    async def create(self, data: AddressCreate) -> Address:
        address = Address(**data.model_dump())
        self.session.add(address)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(address)
        return address

    async def update(self, id: UUID, address_update: AddressCreate) -> Address:
        result = await self.session.execute(select(Address).where(Address.id == id))
        address = result.scalar_one_or_none()
        if not address:
            raise Exception("Where is no entity with same Id")

        if address_update.user_id is not None:
            address.user_id = address_update.user_id

        if address_update.street is not None and address_update.street != "":
            address.street = address_update.street

        address.updated_at = datetime.now()

        await self.session.commit()
        await self.session.refresh(address)
        return address

    async def delete(self, id: UUID) -> None:
        await self.session.execute(delete(Address).where(Address.id == id))
        await self.session.commit()
