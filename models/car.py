import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class Car(BaseModel):
    id: str | None = Field(alias='_id', )
    brand: str = Field(...)
    model: str = Field(...)
    number_of_seats: int = Field(...)
    horse_power: int = Field(...)
    gearbox: str = Field(...)
    trunk: int = Field(...)
    fuel_type: List[str] = Field(...)
    number_of_doors: int = Field(...)
    color: str = Field(...)
    production_year: int = Field(...)
    fuel_consumption: float = Field(...)
    price: int = Field(...)
    available: bool = Field(...)
    last_car_service: str = Field(...)
    next_car_service: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Opelek"
            }
        }


class CarUpdate(BaseModel):
    brand: str = Field(...)
    model: str = Field(...)
    number_of_seats: int = Field(...)
    horse_power: int = Field(...)
    gearbox: str = Field(...)
    trunk: int = Field(...)
    fuel_type: List[str] = Field(...)
    number_of_doors: int = Field(...)
    color: str = Field(...)
    production_year: int = Field(...)
    fuel_consumption: float = Field(...)
    price: int = Field(...)
    available: bool = Field(...)
    last_car_service: str = Field(...)
    next_car_service: str = Field(...)