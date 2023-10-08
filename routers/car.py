from typing import List

from fastapi import APIRouter, Request

from models.car import Car

router = APIRouter()


@router.get("/", response_description="List all cars", response_model=List[Car])
def read_cars(request: Request):
    cars = list(request.app.database['Cars'].find(limit=1000))
    return cars
