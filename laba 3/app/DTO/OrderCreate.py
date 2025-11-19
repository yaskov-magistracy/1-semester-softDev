from pydantic import BaseModel
import uuid
import datetime

class OrderCreate(BaseModel):
    user_id: uuid.UUID
    address_id: uuid.UUID
    product_id: uuid.UUID
    date: datetime.datetime