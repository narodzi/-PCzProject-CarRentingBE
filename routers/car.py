import uuid
from datetime import datetime, date

import isodate
from fastapi import APIRouter, Request, Response, Body, status, Depends

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT
from auth.auth import role_access
from const import const
from const.roles import Role
from models.car import Car, CarUpdate, CarWithStatus, CarStatus
from models.rental import Rental

router = APIRouter()


@router.get("/", response_description="List all cars")
def get_cars(request: Request):
    cars = list(request.app.database['Cars'].find(limit=1000))
    return cars


@router.get("/{id}", response_description="Show a car")
def get_car(request: Request, id: str):
    car = request.app.database['Cars'].find_one(
        {"_id": id}
    )
    if not car:
        return JSONResponse(content={"detail": f"Car {id} does not exist"}, status_code=404)
    return car


@router.post("/", description="Must be role employee", dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def add_car(request: Request, car: CarUpdate = Body(...)):
    car = jsonable_encoder(car)
    car['_id'] = str(uuid.uuid4())
    new_car = request.app.database['Cars'].insert_one(car)
    created_car = request.app.database['Cars'].find_one(
        {"_id": new_car.inserted_id}
    )
    return created_car


@router.put("/{id}", response_description="Update a car", description="Must be role employee",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def update_car(request: Request, id: str, car: CarUpdate = Body(...)):
    car = {k: v for k, v in car.model_dump().items() if v is not None}

    update_result = request.app.database['Cars'].update_one(
        {"_id": id}, {"$set": car}
    )

    if update_result.modified_count == 1:
        update_result = request.app.database['Cars'].find_one({'_id': id})
        return update_result
    if update_result.matched_count == 1:
        return JSONResponse(content={"detail": f"Car {id} has not been updated"}, status_code=400)
    return JSONResponse(content={"detail": f"Car {id} not found"}, status_code=404)


@router.delete("/{id}", response_description="Delete a car", description="Must be role employee",
               dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def delete_car(request: Request, id: str):
    deleted_car = request.app.database['Cars'].delete_one(
        {"_id": id}
    )
    if deleted_car.deleted_count == 0:
        return JSONResponse(content={"detail": f"Car {id} does not exist"}, status_code=404)
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/with_status/",
            response_description="All cars with necessary information and status",
            description="Must be role employee",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def get_cars_with_status(request: Request) -> list[CarWithStatus]:
    rentals = list(map(Rental.from_dict, request.app.database['Rental'].find()))
    cars = list(map(Car.from_dict, request.app.database['Cars'].find()))
    cars_with_status = []

    for car in cars:
        # checking if car is not available
        car_with_status = CarWithStatus.from_car(car, CarStatus.OFF)
        if car.available:
            # checking if car is now rented
            car_rentals: list[Rental] = list(filter(lambda rental: rental.car_id == car.id, rentals))
            for car_rental in car_rentals:
                if car_rental.is_canceled:
                    continue
                start_date = datetime.strptime(car_rental.start_date, const.DATE_FORMAT)
                end_date = datetime.strptime(car_rental.end_date, const.DATE_FORMAT)
                if start_date <= datetime.now() <= end_date:
                    car_with_status.status = CarStatus.RENTED
                    break
            # if none of these conditions were met the car is available
            else:
                car_with_status.status = CarStatus.AVAILABLE
        cars_with_status.append(car_with_status)
    return cars_with_status
