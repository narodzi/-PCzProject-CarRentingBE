import datetime
import uuid
from typing import List
from pydantic import BaseModel, Field


class Car(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
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
    last_car_service: datetime = Field(...)
    next_car_service: datetime = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Opelek"
            }
        }


class UpdateCar(BaseModel):
    id: str = Field(alias='_id')
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
    last_car_service: datetime = Field(...)
    next_car_service: datetime = Field(...)
