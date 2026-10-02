from src.infrastructures.database.models.base import BaseModel
from src.infrastructures.database.db_connection import engine


async def create_tables():
    
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


async def drop_tables():
    
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        
        
async def insert_uah_currency():
    
    from src.infrastructures.database.models.currency import CurrencyModel
    from sqlalchemy import func, insert
    from datetime import date
    from sqlalchemy.exc import IntegrityError
    
    async with engine.begin() as conn:
        
        uah_data = {"code": 980,
                    "name": "Українська гривня",
                    "codename": "UAH",
                    "rate_to_uah": 1.0,
                    "exchange_date": date.today()}
        
        try:
            query = insert(CurrencyModel).values([uah_data])
            await conn.execute(query)
            await conn.commit()   
            
        except IntegrityError as e:
            print("uah already in db")
        
