from typing import List

from fastapi import APIRouter, Request

from models.rental import Rental

router = APIRouter()


@router.get("/", response_description="List all rentals", response_model=List[Rental])
def read_cars(request: Request):
    rentals = list(request.app.database['Rentals'].find(limit=1000))
    return rentals
