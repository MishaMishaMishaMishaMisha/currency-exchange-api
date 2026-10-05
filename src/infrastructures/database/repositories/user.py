from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import Sequence
from uuid import UUID

from src.infrastructures.database.models.user import UserModel
from src.domain.entities.user import UserEntity
from src.infrastructures.mappers.user import userModel_to_userEntity
from src.domain.exceptions import (UserError,
                                   UsernameTakenError,
                                   EmailTakenError)


class UserRepositorySQL:
    
    def __init__(self, db_session: AsyncSession):    
        self.db_session = db_session
        
    async def make_commit(self):
        await self.db_session.commit()
        
    async def make_rollback(self):
        await self.db_session.rollback()
        

    # protocol methods
    async def add_user(self, user: UserEntity) -> UserEntity: 
        
        user_model = UserModel(username=user.username,
                               email=user.email,
                               password_hash=user.password_hash)
        
        try:
            self.db_session.add(user_model)
            await self.db_session.commit()
            await self.db_session.refresh(user_model)
            
            user.id = user_model.id
            user.created_at = user_model.created_at
            user.updated_at = user_model.updated_at
            
            return user

        except IntegrityError as e:
            await self.db_session.rollback()

            msg = str(e.orig)

            if 'ix_users_username' in msg:
                raise UsernameTakenError

            if 'ix_users_email' in msg:
                raise EmailTakenError

            raise UserError(str(e))
        
    async def get_user_by_id(self, user_id: UUID) -> UserEntity | None:
        
        query = select(UserModel).where(UserModel.id==user_id)
        
        res = await self.db_session.execute(query)
        user_model = res.scalar_one_or_none()

        if user_model:
            return userModel_to_userEntity(user_model)
    
    async def get_user_by_username(self, username: str) -> UserEntity | None:

        query = select(UserModel).where(UserModel.username==username)
        
        res = await self.db_session.execute(query)
        user_model = res.scalar_one_or_none()

        if user_model:
            return userModel_to_userEntity(user_model)
    
    async def get_user_by_email(self, email: str) -> UserEntity | None:

        query = select(UserModel).where(UserModel.email==email)
        
        res = await self.db_session.execute(query)
        user_model = res.scalar_one_or_none()

        if user_model:
            return userModel_to_userEntity(user_model)
    
    async def get_users(self, limit: int, offset: int) -> Sequence[UserEntity]:

        query = (select(UserModel)
                 .order_by(UserModel.created_at)
                 .limit(limit)
                 .offset(offset))
        
        res = await self.db_session.execute(query)
        user_models = res.scalars().all()
        
        users = [userModel_to_userEntity(user_model) for user_model in user_models]
        return users
    
    