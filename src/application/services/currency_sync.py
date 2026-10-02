from loguru import logger
from datetime import datetime
from sqlalchemy import func

from src.domain.interfaces.repositories import ICurrencyRepository
from src.domain.interfaces.external_api_clients import IExternalCurrencyAPIClient
from src.domain.entities.currency import CurrencyEntity


class CurrencySyncService:
    
    def __init__(self, 
                 api_client: IExternalCurrencyAPIClient, 
                 currency_repo: ICurrencyRepository):
        
        self.api_client = api_client
        self.currency_repo = currency_repo

    async def sync_currency(self) -> None:
        
        logger.debug("CurrencySyncService: sync currencies - making request")
        
        currencies_list = await self.api_client.fetch_latest_currencies()
        
        logger.debug("CurrencySyncService: sync currencies - creating entities")
        
        currency_entities = []
        for currency in currencies_list:
            
            exchange_date = datetime.strptime(currency["exchangedate"], 
                                              "%d.%m.%Y")
            
            currency_entity = CurrencyEntity(code=currency["r030"],
                                             name=currency["txt"],
                                             codename=currency["cc"],
                                             rate_to_uah=currency["rate"],
                                             exchange_date=exchange_date,
                                             created_at=func.timezone("utc", func.now()),
                                             updated_at=func.timezone("utc", func.now()))
            
            currency_entities.append(currency_entity)
        
        await self.currency_repo.upsert_currencies(currency_entities)