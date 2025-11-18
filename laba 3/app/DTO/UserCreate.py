from pydantic import BaseModel

class UserCreate(BaseModel):
    login: str 
    email: str 
    description: str 