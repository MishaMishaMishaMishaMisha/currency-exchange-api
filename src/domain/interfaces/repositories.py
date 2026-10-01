from typing import Protocol, Sequence
from uuid import UUID
from datetime import datetime

from src.domain.entities.user import UserEntity
from src.domain.entities.refresh_session import RefreshSessionEntity
from src.domain.entities.currency import CurrencyEntity


class IUserRepository(Protocol):
    
    async def add_user(self, user: UserEntity) -> UserEntity: 
        pass
    
    async def get_user_by_id(self, user_id: UUID) -> UserEntity | None:
        pass
    
    async def get_user_by_username(self, username: str) -> UserEntity | None:
        pass
    
    async def get_user_by_email(self, email: str) -> UserEntity | None:
        pass
    
    async def get_users(self, limit: int, offset: int) -> Sequence[UserEntity]:
        pass
    

class IRefreshSessionRepository(Protocol):
    
    async def create_session(self, 
                             user_id: UUID, 
                             token: str, 
                             expires_at: datetime) -> RefreshSessionEntity:
        pass

    async def get_active_session(self, token: str) -> RefreshSessionEntity | None:
        pass

    async def revoke_session(self, token: str) -> None:
        pass


class ICurrencyRepository(Protocol):
    
    # insert with autoupdate
    async def upsert_currencies(self, currencies: list[CurrencyEntity]) -> None:
        pass
    
    async def get_all_currencies(self) -> Sequence[CurrencyEntity]:
        pass

    async def get_currency_by_name(self, currency_name: str) -> CurrencyEntity | None:
        pass
    
    async def get_currency_by_codename(self, currency_codename: str) -> CurrencyEntity | None:
        pass

