from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class UserEntity:
    
    id: UUID | None
    username: str
    email: str
    password_hash: str
    created_at: datetime | None
    updated_at: datetime | None
    