from pydantic import BaseModel
import uuid
import datetime

class OrderResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    address_id: uuid.UUID
    product_id: uuid.UUID
    date: datetime.datetime