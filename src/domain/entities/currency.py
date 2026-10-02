from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class CurrencyEntity:

    code: int       # 840
    name: str       # Долар США
    codename: str   # USD
    rate_to_uah: float
    exchange_date: date
    created_at: datetime | None
    updated_at: datetime | None
