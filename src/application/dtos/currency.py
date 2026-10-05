from datetime import datetime, date
from pydantic import BaseModel


class CurrencyDTO(BaseModel):
    code: int
    name: str
    codename: str
    rate_to_uah: float
    exchange_date: date
    created_at: datetime | None
    updated_at: datetime | None
    
    class Config:
        from_attributes = True

class ConvertedCurrenciesDTO(BaseModel):
    from_code: int
    from_name: str
    from_codename: str
    
    to_code: int
    to_name: str
    to_codename: str
    
    amount: float
    result: float
    rate: float
    
    class Config:
        from_attributes = True
    