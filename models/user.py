import uuid
from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    mail_address: str = Field(...)
    licence_number: str = Field(...)
    wallet_balance: float = Field(...)
    loyalty_points: int = Field(...)
    country: str = Field(...)
    city: str = Field(...)
    postal_code: str = Field(...)
    house_number: str = Field(...)
    apartment_number: str = Field(...)
    phone_number: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "first_name": "Dominik",
                "last_name": "Szwedzinski",
                "mail_address": "DoSz@example.com",
            }
        }
