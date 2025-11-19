from pydantic import BaseModel
import uuid

class ProductCreate(BaseModel):
    name: str
    quantity: int