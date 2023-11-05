from pydantic import BaseModel, Field


class Car(BaseModel):
    id: str | None = Field(alias='_id', )
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
    price: int = Field(...)
    available: bool = Field(...)
    image_url: str = Field(...)
    type: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "_id": "f0f26cc1-2725-4c91-8d5a-371db1234561",
                "brand": "Volkswagen",
                "model": "Golf",
                "number_of_seats": 5,
                "horse_power": 150,
                "gearbox": "manualna",
                "trunk": 350,
                "fuel_type": "benzyna",
                "number_of_doors": 5,
                "color": "czarny",
                "production_year": 2019,
                "fuel_consumption": 6.5,
                "price": 150,
                "available": True
            }
        }


class CarUpdate(BaseModel):
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
    price: int = Field(...)
    available: bool = Field(...)
    image_url: str = Field(...)
    type: str = Field(...)