from pydantic import BaseModel
from typing import Optional

class UserUpdate(BaseModel):
    login: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None