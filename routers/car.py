import uuid

from fastapi import APIRouter, Request, Response, Body, status, Depends

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT
from auth.auth import role_access
from const.roles import Role
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


@router.get("/limited/")
def get_cars(request: Request, count: int, filtered: str):
    if filtered == "naprawa":
        maintenances = list(request.app.database['Maintenance'].find(limit=count))
        car_ids = [maintenance['car_id'] for maintenance in maintenances]
        cars = list(request.app.database['Cars'].find({"_id": {"$in": car_ids}}))
        return cars
    elif filtered == "wypozyczone":
        rentals = list(request.app.database['Rental'].find(limit=count))
        car_ids = [rental['car_id'] for rental in rentals]
        cars = list(request.app.database['Cars'].find({"_id": {"$in": car_ids}}))
        return cars
    elif filtered == "wszystkie":
        cars = list(request.app.database['Cars'].find(limit=count))
        return cars
    return JSONResponse(content={"Not found"}, status_code=404)
