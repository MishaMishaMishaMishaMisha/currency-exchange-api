from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr


class CreateUserDTO(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserDTO(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True