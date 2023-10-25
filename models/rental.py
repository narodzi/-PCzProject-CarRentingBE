import datetime
import uuid
from typing import List
from pydantic import BaseModel, Field


class Rental(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    car_id: str = Field(...)
    user_id: str = Field(...)
    start_date: datetime = Field(...)
    end_date: datetime = Field(...)
    price_overall: int = Field(...)
    status: str = Field(...)
    penalty: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e"
            }
        }


class UpdateRental(BaseModel):
    car_id: str = Field(...)
    user_id: str = Field(...)
    start_date: datetime = Field(...)
    end_date: datetime = Field(...)
    price_overall: int = Field(...)
    status: str = Field(...)
    penalty: int = Field(...)