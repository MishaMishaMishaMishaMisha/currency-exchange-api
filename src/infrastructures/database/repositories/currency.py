from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from typing import Sequence
from dataclasses import asdict
from loguru import logger

from src.infrastructures.database.models.currency import CurrencyModel
from src.domain.entities.currency import CurrencyEntity
from src.infrastructures.mappers.currency import currencyModel_to_currencyEntity


class CurrencyRepositorySQL:
    
    def __init__(self, db_session: AsyncSession):    
        self.db_session = db_session
        
    async def make_commit(self):
        await self.db_session.commit()
        
    async def make_rollback(self):
        await self.db_session.rollback()
        
    # protocol methods
    async def upsert_currencies(self, currencies: list[CurrencyEntity]) -> None:
        
        logger.debug("CurrencyRepositorySQL: upsert currencies - trying")
        
        if not currencies:
            logger.debug("CurrencyRepositorySQL: upsert currencies - list is empty")
            return
        
        currencies_dicts = [asdict(currency) for currency in currencies]
        
        query = insert(CurrencyModel).values(currencies_dicts)
        update_query = query.on_conflict_do_update(
                            index_elements=['code'],
                            set_={
                                'name': query.excluded.name,
                                'codename': query.excluded.codename,
                                'rate_to_uah': query.excluded.rate_to_uah,
                                'exchange_date': query.excluded.exchange_date,
                                'updated_at': func.timezone("utc", func.now())}
        )

        logger.debug("CurrencyRepositorySQL: upsert currencies - executing query")
        
        await self.db_session.execute(update_query)
        await self.db_session.commit()
        
        logger.debug("CurrencyRepositorySQL: upsert currencies - done")
    
    async def get_all_currencies(self) -> Sequence[CurrencyEntity]:
        
        logger.debug("CurrencyRepositorySQL: getting all currencies")

        query = select(CurrencyModel)
        res = await self.db_session.execute(query)
        
        models = res.scalars().all()
        currenies_entities = [
            currencyModel_to_currencyEntity(model) for model in models]
        
        return currenies_entities
    
    async def get_currency_by_name(self, currency_name: str) -> CurrencyEntity | None:
        
        logger.debug("CurrencyRepositorySQL: getting currency by name")

        query = select(CurrencyModel).where(CurrencyModel.name==currency_name)
        res = await self.db_session.execute(query)
        
        model =  res.scalar_one_or_none()
        if model:
            return currencyModel_to_currencyEntity(model)
    
    async def get_currency_by_codename(self, currency_codename: str) -> CurrencyEntity | None:
        
        logger.debug("CurrencyRepositorySQL: getting currency by codename")

        query = select(CurrencyModel).where(CurrencyModel.codename==currency_codename)
        res = await self.db_session.execute(query)
        
        model = res.scalar_one_or_none()
        if model:
            return currencyModel_to_currencyEntity(model)
    