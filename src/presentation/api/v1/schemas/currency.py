from pydantic import BaseModel, Field


# input
class CurrenciesToConvert(BaseModel):
    from_codename: str = Field(examples=["USD", "usd"])
    to_codename: str = Field(examples=["EUR", "eur"])
    amount: float = Field(gt=0, examples=["100.0", "50"])


# response
class CurrencyNameDTO(BaseModel):
    name: str
    codename: str
    
    class Config:
        from_attributes = True
        
class ConvertedCurrencyDTO(BaseModel):
    result: float
    rate: float
    
    class Config:
        from_attributes = True