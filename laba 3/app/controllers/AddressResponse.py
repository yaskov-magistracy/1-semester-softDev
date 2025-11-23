import uuid

from pydantic import BaseModel


class AddressResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    street: str
