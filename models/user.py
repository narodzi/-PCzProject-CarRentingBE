from decimal import Decimal

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(alias='_id')
    licence_number: str = Field(...)
    wallet_balance: int = Field(...)
    country: str = Field(...)
    city: str = Field(...)
    postal_code: str = Field(...)
    house_number: str = Field(...)
    apartment_number: str = Field(...)
    phone_number: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class UserUpdate(BaseModel):
    licence_number: str = Field(...)
    wallet_balance: int = Field(...)
    country: str = Field(...)
    city: str = Field(...)
    postal_code: str = Field(...)
    house_number: str = Field(...)
    apartment_number: str = Field(...)
    phone_number: str = Field(...)
