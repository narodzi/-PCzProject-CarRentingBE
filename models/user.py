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
        schema_extra = {
            "example": {
              "_id": "7b94e329-214b-4c02-8e2a-0aae651b0785",
              "licence_number": "SKE 567AZ",
              "wallet_balance": 125.75,
              "country": "Polska",
              "city": "Warszawa",
              "postal_code": "02-100",
              "house_number": "12",
              "apartment_number": "3",
              "phone_number": "+48 123 456 789"
            }
        }


class UserUpdate(BaseModel):
    licence_number: str = Field(...)
    wallet_balance: int = Field(...)
    country: str = Field(...)
    city: str = Field(...)
    postal_code: str = Field(...)
    house_number: str = Field(...)
    apartment_number: str = Field(...)
    phone_number: str = Field(...)
