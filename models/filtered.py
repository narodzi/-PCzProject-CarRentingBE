from dataclasses import dataclass

from pydantic import BaseModel, Field


class RentalSearchResult(BaseModel):
    id: str = Field(..., alias='_id', )
    image_url: str = Field(...)
    brand: str = Field(...)
    model: str = Field(...)
    number_of_seats: int = Field(...)
    horse_power: int = Field(...)
    gearbox: str = Field(...)
    trunk: int = Field(...)
    fuel_type: str = Field(...)
    number_of_doors: int = Field(...)
    color: str = Field(...)
    production_year: int = Field(...)
    fuel_consumption: float = Field(...)
    price_overall: int = Field(...)


class RentalSearch(BaseModel):
    start_date: str = Field(...)
    end_date: str = Field(...)
    brand: str | None = Field(None)
    type: str | None = Field(None)
    earliest_production_year: int | None = Field(None)
    gearbox: str | None = Field(None)
    fuel_type: str | None = Field(None)
    minimal_horse_power: int | None = Field(None)
    number_of_seats: int | None = Field(None)
    number_of_doors: int | None = Field(None)
    minimal_trunk_size: int | None = Field(None)
    minimal_price: int | None = Field(None)
    maximal_price: int | None = Field(None)


@dataclass
class FilterParameters:
    cars_brands: list[str]
    number_of_seats: list[int]
    gearboxes: list[str]
    fuel_types: list[str]
    number_of_doors: list[int]\
    # TODO: ADD Type field here
