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

    class Config:
        allow_population_by_field_name = True


class RentalUpdate(BaseModel):
    car_id: str = Field(...)
    user_id: str = Field(...)
    start_date: str = Field(...)
    end_date: str = Field(...)
    price_overall: int = Field(...)
    is_canceled: bool = Field(...)


class RentalAdd(BaseModel):
    user_id: str = Field(...)
    car_id: str = Field(...)
    start_date: str = Field(...)
    end_date: str = Field(...)
