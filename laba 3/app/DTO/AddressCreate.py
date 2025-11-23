import uuid

from pydantic import BaseModel


class AddressCreate(BaseModel):
    user_id: uuid.UUID
    street: str
