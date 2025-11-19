from pydantic import BaseModel
import uuid
import datetime

class AddressCreate(BaseModel):
    user_id: uuid.UUID
    street: str