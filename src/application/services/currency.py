from typing import Sequence
from loguru import logger

from src.domain.interfaces.repositories import ICurrencyRepository
from src.domain.entities.currency import CurrencyEntity
from src.domain.exceptions import CurrencyNotFoundError
from src.application.dtos.currency import CurrencyDTO, ConvertedCurrenciesDTO


class CurrencyService:
    
    def __init__(self, currency_repo: ICurrencyRepository):
        self.currency_repo = currency_repo
        
    async def convert_currency(self,
                               amount: float,
                               currency_name_from: str | None = None,
                               currency_name_to: str | None = None,
                               currency_codename_from: str | None = None,
                               currency_codename_to: str | None = None
                            ) -> ConvertedCurrenciesDTO:
        
        if amount <= 0:
            logger.debug("CurrencyService: convering currency - amount < 0")
            raise ValueError("Amount should be greater than 0")
        
        # by names
        if currency_name_from and currency_name_to:
            logger.debug("CurrencyService: convering currency by name - getting info from db")
        
            currency_from = await self.currency_repo.get_currency_by_name(currency_name_from)
            if currency_from is None:
                raise CurrencyNotFoundError(f"Currency {currency_name_from} not found")
            
            currency_to = await self.currency_repo.get_currency_by_name(currency_name_to)
            if currency_to is None:
                raise CurrencyNotFoundError(f"Currency {currency_name_to} not found")
        
        # by codenames
        elif currency_codename_from and currency_codename_to:
            logger.debug("CurrencyService: convering currency by codename - getting info from db")
            
            currency_from = await self.currency_repo.get_currency_by_codename(currency_codename_from)
            if currency_from is None:
                raise CurrencyNotFoundError(f"Currency {currency_codename_from} not found")
            
            currency_to = await self.currency_repo.get_currency_by_codename(currency_codename_to)
            if currency_to is None:
                raise CurrencyNotFoundError(f"Currency {currency_codename_to} not found")
            
        else:
            logger.debug("CurrencyService: convering currency - no parameters were given")
            raise TypeError("No parameters were given")
        
        logger.debug("CurrencyService: convering currency - calculating rate and amount")
        
        result, rate = self._calculate_converted_currency(
                                    currency_from.rate_to_uah,
                                    currency_to.rate_to_uah,
                                    amount)
        
        logger.debug("CurrencyService: convering currency - mapping to dto")
        
        return self._to_convertedDto(currency_from, currency_to,
                                    amount, result, rate)
    
    async def get_all_currencies(self) -> Sequence[CurrencyDTO]:
        
        logger.debug("CurrencyService: getting all currencies from db - trying")
        currencies = await self.currency_repo.get_all_currencies()
        logger.debug(f"CurrencyService: getting all currencies from db - found {len(currencies)} rows")
        
        return [CurrencyDTO.model_validate(currency) for currency in currencies]
        
    
    def _calculate_converted_currency(
                        self,
                        rate_from: float,
                        rate_to: float,
                        amount: float) -> tuple[float, float]:
        
        exchange_rate = round(rate_from / rate_to, 2)
        result = round(exchange_rate * amount, 2)
        return (result, exchange_rate)
    
    def _to_convertedDto(self,
                        currency_from: CurrencyEntity,
                        currency_to: CurrencyEntity,
                        amount: float,
                        result: float,
                        rate: float) -> ConvertedCurrenciesDTO:

        dto = ConvertedCurrenciesDTO(from_code=currency_from.code,
                                   from_name=currency_from.name,
                                   from_codename=currency_from.codename,
                                   to_code=currency_to.code,
                                   to_name=currency_to.name,
                                   to_codename=currency_to.codename,
                                   amount=amount,
                                   result=result,
                                   rate=rate)   
        return dto     
        