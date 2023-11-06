import uuid
from typing import List, Optional
from pydantic import BaseModel, Field


class Maintenance(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    car_id: str = Field(...)
    date: str = Field(...)
    type: str = Field(...)
    description: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e"
            }
        }


class UpdateMaintenance(BaseModel):
    car_id: str = Field(...)
    date: str = Field(...)
    type: str = Field(...)
    description: int = Field(...)
