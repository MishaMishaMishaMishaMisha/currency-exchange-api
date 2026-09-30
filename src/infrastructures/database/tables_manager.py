from src.infrastructures.database.models.base import BaseModel
from src.infrastructures.database.db_connection import engine


async def create_tables():
    
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


async def drop_tables():
    
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
    
