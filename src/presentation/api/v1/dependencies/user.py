from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.infrastructures.database.repositories.user import UserRepositorySQL
from src.application.services.user import UserService
from src.infrastructures.database.db_connection import get_db_session


def get_user_service(db_session: AsyncSession = Depends(get_db_session)) -> UserService:
    
    user_repo = UserRepositorySQL(db_session)
    user_service = UserService(user_repo)
    
    return user_service
