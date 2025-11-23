from typing import Optional

from pydantic import BaseModel


class UserUpdate(BaseModel):
    login: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
