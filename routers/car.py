from typing import List

from fastapi import APIRouter, Request, Response, Body, status

from fastapi.encoders import jsonable_encoder

from models.car import Car

router = APIRouter()


@router.get("/cars", response_description="List all cars", response_model=List[Car])
def read_cars(request: Request):
    cars = list(request.app.database['Cars'].find(limit=1000))
    return cars


@router.get("/car/{id}", response_description="Show a car", response_model=Car)
def read_car(request: Request, id: str):
    car = list(request.app.database['Cars'].find_one(
        {"_id": id}
    ))
    return car


@router.post("/addcar", response_model=Car)
def add_car(request: Request, car: Car = Body(...)):
    car = jsonable_encoder(car)
    new_car = request.app.database['Cars'].insert_one(car)
    create_car = request.app.database['Cars'].find_one(
        {"_id": new_car.inserted_id}
    )
    return create_car


@router.put("/car/{id}", response_description="Update a car", response_model=UpdateCar)
def update_car(request: Request, id: str, car: UpdateCar = Body(...)):
    car = {k: v for k, v in car.dict().items() if v is not None}

    if len(car) >= 1:
        updated_car = request.app.database['Cars'].update_one(
            {"_id": id}, {"$set": car}
        )

        if updated_car.modified_count == 0:
            return "Car not found"

        exit_car = request.app.database['Cars'].find_one(
            {"_id": id}
        )

        return exit_car

    else:
        return "Invalid input"


@router.delete("/car/{id}", response_description="Delete a car")
def delete_car(request: Request, id: str, response: Response):
    deleted_car = request.app.database['Cars'].delete_one(
        {"_id": id}
    )

    if deleted_car.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    else:
        return "Car not found"
