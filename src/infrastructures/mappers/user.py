from src.infrastructures.database.models.user import UserModel
from src.domain.entities.user import UserEntity


def userModel_to_userEntity(user_model: UserModel) -> UserEntity:
    
    user = UserEntity(id=user_model.id,
                      username=user_model.username,
                      email=user_model.email,
                      password_hash=user_model.password_hash,
                      created_at=user_model.created_at,
                      updated_at=user_model.updated_at)
    
    return user