import uuid
from typing import List, Optional
from pydantic import BaseModel, Field


class Maintenance(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    car_id: str = Field(...)
    date: str = Field(...)
    type: str = Field(...)
    description: str = Field(...)

    class Config:
        allow_population_by_field_name = True


class MaintenanceUpdate(BaseModel):
    car_id: str = Field(...)
    date: str = Field(...)
    type: str = Field(...)
    description: str = Field(...)
