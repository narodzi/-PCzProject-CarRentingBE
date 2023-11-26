from decimal import Decimal

import bson
from pydantic import BaseModel, Field


class Rental(BaseModel):
    id: str = Field(alias='_id')
    car_id: str = Field(...)
    user_id: str = Field(...)
    start_date: str = Field(...)
    end_date: str = Field(...)
    price_overall: int = Field(...)
    is_canceled: bool = Field(...)
    penalty: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
              "_id": "c1b2a3e9-9c8c-4e9f-9f4c-1b1a2e3c4d5d",
              "car_id": "f0f26cc1-2725-4c91-8d5a-371db1234561",
              "user_id": "7b94e329-214b-4c02-8e2a-0aae651b0785",
              "start_date": "2023-10-11T12:00:00Z",
              "end_date": "2023-10-15T12:00:00Z",
              "price_overall": 350.2,
              "is_canceled": False,
              "penalty": 0
            }
        }


class RentalUpdate(BaseModel):
    car_id: str = Field(...)
    user_id: str = Field(...)
    start_date: str = Field(...)
    end_date: str = Field(...)
    price_overall: int = Field(...)
    is_canceled: bool = Field(...)
    penalty: int = Field(...)


class RentalAdd(BaseModel):
    car_id: str = Field(...)
    start_date: str = Field(...)
    end_date: str = Field(...)
