from src.infrastructures.database.models.currency import CurrencyModel
from src.domain.entities.currency import CurrencyEntity


def currencyModel_to_currencyEntity(currency_model: CurrencyModel) -> CurrencyEntity:
    
    currency = CurrencyEntity(code=currency_model.code,
                              name=currency_model.name,
                              codename=currency_model.codename,
                              rate_to_uah=currency_model.rate_to_uah,
                              exchange_date=currency_model.exchange_date,
                              created_at=currency_model.created_at,
                              updated_at=currency_model.updated_at)
    
    return currency
