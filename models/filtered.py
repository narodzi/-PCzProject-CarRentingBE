from pydantic import BaseModel, Field
from decimal import Decimal


class RentalSearchResultDto(BaseModel):
    id: str = Field(alias='_id', )
    img_url: str = Field(...)
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
    price_overall: float = Field(...)



class RentalSearchDto(BaseModel):
    start_date: str | None = Field(None)
    end_date: str | None = Field(None)
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




