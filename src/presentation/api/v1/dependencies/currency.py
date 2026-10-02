from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.infrastructures.database.repositories.currency import CurrencyRepositorySQL
from src.application.services.currency import CurrencyService
from src.infrastructures.database.db_connection import get_db_session


def get_currency_service(db_session: AsyncSession = Depends(get_db_session)) -> CurrencyService:
    
    user_repo = CurrencyRepositorySQL(db_session)
    user_service = CurrencyService(user_repo)
    
    return user_service