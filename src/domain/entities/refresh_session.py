from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class RefreshSessionEntity:
    
    id: UUID | None
    user_id: UUID
    token_hash: str
    is_revoked: bool
    expires_at: datetime
    updated_at: datetime
