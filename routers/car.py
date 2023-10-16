import http.client
import json
import uuid
from typing import List

from fastapi import APIRouter, Request, Response, Body, status

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT

from models.car import Car, CarUpdate

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


@router.post("/")
def add_car(request: Request, car: CarUpdate = Body(...)):
    car = jsonable_encoder(car)
    car['_id'] = str(uuid.uuid4())
    new_car = request.app.database['Cars'].insert_one(car)
    created_car = request.app.database['Cars'].find_one(
        {"_id": new_car.inserted_id}
    )
    return created_car


@router.put("/{id}", response_description="Update a car")
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


@router.delete("/{id}", response_description="Delete a car")
def delete_car(request: Request, id: str):
    deleted_car = request.app.database['Cars'].delete_one(
        {"_id": id}
    )
    if deleted_car.deleted_count == 0:
        return JSONResponse(content={"detail": f"Car {id} does not exist"}, status_code=404)
    return Response(status_code=HTTP_204_NO_CONTENT)
