from uuid import UUID
from typing import Sequence

from src.domain.interfaces.repositories import IUserRepository
from src.domain.entities.user import UserEntity
from src.domain.exceptions import UserNotFoundError
from src.application.dtos.user import CreateUserDTO, UserDTO
from src.core.security import hash_password


class UserService:
    
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
        
    async def add_user(self, user_dto: CreateUserDTO) -> UserDTO:
        
        password_hash = hash_password(user_dto.password)
        
        user_entity = UserEntity(id=None,
                                 username=user_dto.username,
                                 email=user_dto.email,
                                 password_hash=password_hash,
                                 created_at=None,
                                 updated_at=None)
        
        saved_user = await self.user_repo.add_user(user_entity)
        
        return UserDTO.model_validate(saved_user)
    
    async def get_user(self, user_id: UUID) -> UserDTO:
        
        user_entity = await self.user_repo.get_user_by_id(user_id)
        
        if user_entity is None:
            raise UserNotFoundError
        
        return UserDTO.model_validate(user_entity)
    
    async def get_users(self, limit: int, offset: int) -> Sequence[UserDTO]:
        
        users_entity = await self.user_repo.get_users(limit, offset)
        return [UserDTO.model_validate(u) for u in users_entity]
        
        
        