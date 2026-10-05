import httpx
from loguru import logger
from typing import Sequence

from src.domain.exceptions import ExternalAPIError, IncorrectResponseFormatError


class ExternalCurrencyAPIClientHttpx:
    
    def __init__(self, url: str):
        self.url = url
    
    async def fetch_latest_currencies(self) -> Sequence[dict]:
        
        try:
            
            async with httpx.AsyncClient(timeout=10) as client:
                
                logger.debug("CLI Sync Currencies: trying to make request")
                
                response = await client.get(self.url)
                response.raise_for_status() # raise httpx.HTTPStatusError if status 4xx, 5xx
                result = response.json()
                
                logger.debug("CLI Sync Currencies: got response")
                logger.debug("CLI Sync Currencies: checking result's format")
                
                # check if result is list[dict]
                # and all dicts have fields
                fields = {"txt", "rate", "cc", "exchangedate"}

                # 1. check types
                if isinstance(result, list) and all(isinstance(item, dict) for item in result):
                    
                    # 2. check fields
                    if all(fields.issubset(item.keys()) for item in result):
                        logger.debug("CLI Sync Currencies: result is correct")
                        return result
    
                    else:
                        logger.error("CLI Sync Currencies: dicts dont have all fields")
                        raise IncorrectResponseFormatError("Dicts in result dont have all fields")
                else:
                    logger.error("CLI Sync Currencies: result is not list of dicts")
                    raise IncorrectResponseFormatError("Result is not list of dicts")
                
        except httpx.TimeoutException:
            logger.error("CLI Sync Currencies: Timout exceede")
            raise ExternalAPIError("Timout exceeded")

        except httpx.ConnectError:
            logger.error("CLI Sync Currencies: cant connect to server")
            raise ExternalAPIError("Cant connect to server")

        except httpx.HTTPStatusError as e:
            logger.error(f"CLI Sync Currencies: server response with {e.response.status_code} code")
            raise ExternalAPIError(f"server response with {e.response.status_code} code")

        except httpx.RequestError as e:
            logger.error(f"CLI Sync Currencies: networking error - {e}")
            raise ExternalAPIError(f"networking error: {e}")

    
