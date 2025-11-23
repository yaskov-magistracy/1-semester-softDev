import datetime
import uuid

from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    address_id: uuid.UUID
    product_id: uuid.UUID
    date: datetime.datetime
