from fastapi import (APIRouter, 
                     Depends, 
                     status, 
                     HTTPException)
from typing import Sequence
from loguru import logger

from src.domain.exceptions import CurrencyNotFoundError
from src.application.services.currency import CurrencyService
from src.presentation.api.v1.schemas.currency import (CurrenciesToConvert,
                                                      CurrencyNameDTO,
                                                      ConvertedCurrencyDTO) # presentation dtos
from src.presentation.api.v1.dependencies.currency import get_currency_service


router = APIRouter(prefix="/currencies", tags=["Currencies"])


# convert by codename
@router.post("/convert", response_model=ConvertedCurrencyDTO)
async def convert_currency(
        currencies: CurrenciesToConvert,
        currency_service: CurrencyService = Depends(get_currency_service)
        ) -> ConvertedCurrencyDTO:
    
    try:
        logger.info("Converting currencies...")
        
        result = await currency_service.convert_currency(
                                            amount=currencies.amount,
                                            currency_codename_from=currencies.from_codename,
                                            currency_codename_to=currencies.to_codename)
        return ConvertedCurrencyDTO.model_validate(result)
    
    except CurrencyNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))

# get all currency names
@router.get("/", response_model=Sequence[CurrencyNameDTO])
async def get_currencies_names(
        currency_service: CurrencyService = Depends(get_currency_service)
        ) -> Sequence[CurrencyNameDTO]:
    
    logger.info("Getting al currencies names...")
    
    currencies = await currency_service.get_all_currencies()
    return [CurrencyNameDTO.model_validate(currency) for currency in currencies]




# ####
# from src.infrastructures.database.tables_manager import insert_uah_currency
# @router.get("/test-insert-uah")
# async def insert_uah():
#     await insert_uah_currency()
# #####
