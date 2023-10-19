from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias='_id')
    first_name: str = Field(...)
    surname: str = Field(...)
    email: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "first_name": "Dominik",
                "surname": "Szwedzinski",
                "email": "DoSz@example.com",
            }
        }