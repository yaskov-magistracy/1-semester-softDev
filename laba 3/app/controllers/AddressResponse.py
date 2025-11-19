from pydantic import BaseModel
import uuid
import datetime

class AddressResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    street: str