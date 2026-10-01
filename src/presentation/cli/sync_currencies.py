import asyncio
from loguru import logger

from src.domain.exceptions import ExternalAPIError, IncorrectResponseFormatError
from src.application.services.currency_sync import CurrencySyncService
from src.infrastructures.database.db_connection import async_session_factory
from src.infrastructures.database.repositories.currency import CurrencyRepositorySQL
from src.infrastructures.external_api.currency_client import ExternalCurrencyAPIClientHttpx
from src.core.config import settings


async def main():
    
    logger.info("CLI Sync Currencies: preparing...")
    
    try: 
        logger.debug("CLI Sync Currencies: creating api_client")

        api_client = ExternalCurrencyAPIClientHttpx(url=settings.external_api.CURRENCY_URL)
        
        async with async_session_factory() as session:
            
            logger.debug("CLI Sync Currencies: creating repo and service")
            
            currency_repo = CurrencyRepositorySQL(session)
            currency_sync_service = CurrencySyncService(api_client=api_client, 
                                                        currency_repo=currency_repo)
            
            logger.info("CLI Sync Currencies: starting")
            
            await currency_sync_service.sync_currency()
            
            logger.info("CLI Sync Currencies: completed")
            
    except (IncorrectResponseFormatError, ExternalAPIError) as e:
        logger.error(f"CLI Sync Currencies: finished with error - {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())

