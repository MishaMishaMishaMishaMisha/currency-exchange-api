from typing import Protocol, Sequence


class IExternalCurrencyAPIClient(Protocol):
    
    url: str
    
    async def fetch_latest_currencies(self) -> Sequence[dict]:
        """
        Returns:
            Sequence[dict]: currencies list in format: 
                {
                    "r030": code,        # 123
                    "txt": name,         # Долар США
                    "rate": rate,        # 45.000
                    "cc":codename,       # USD
                    "exchangedate": str  # 01.01.2026
                }
        """
        pass
    
