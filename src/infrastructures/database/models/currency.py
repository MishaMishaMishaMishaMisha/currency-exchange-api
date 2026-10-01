from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, DateTime
from datetime import datetime, date

from src.infrastructures.database.models.base import BaseModel


class CurrencyModel(BaseModel):
    
    __tablename__ = "currencies"
    
    code: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(index=True, unique=True)
    
    codename: Mapped[str] = mapped_column(index=True, unique=True)
    
    rate_to_uah: Mapped[float]
    
    exchange_date: Mapped[date]
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=text("now()"))
    
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=text("now()"),
                                                 server_onupdate=text("now()"))
    
    