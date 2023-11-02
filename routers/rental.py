from typing import List

from fastapi import APIRouter, Request, Response, Body, status

from fastapi.encoders import jsonable_encoder

from models.rental import Rental, UpdateRental

router = APIRouter()


@router.get("/", response_description="List all rentals", response_model=List[Rental])
def read_rentals(request: Request):
    rentals = list(request.app.database['Rental'].find(limit=1000))
    return rentals


@router.get("/{id}", response_description="Show a rental", response_model=Rental)
def read_rental(request: Request, id: str):
    rental = request.app.database['Rental'].find_one(
        {"_id": id}
    )
    return rental


@router.post("/add", response_model=Rental)
def add_rental(request: Request, rental: Rental = Body(...)):
    rental = jsonable_encoder(rental)
    new_rental = request.app.database['Rental'].insert_one(rental)
    create_rental = request.app.database['Rental'].find_one(
        {"_id": new_rental.inserted_id}
    )
    return create_rental


@router.put("/{id}", response_description="Update a rental", response_model=UpdateRental)
def update_rental(request: Request, id: str, rental: UpdateRental = Body(...)):
    rental = {k: v for k, v in rental.dict().items() if v is not None}

    if len(rental) >= 1:
        updated_rental = request.app.database['Rental'].update_one(
            {"_id": id}, {"$set": rental}
        )

        if updated_rental.modified_count == 0:
            return "Rental not found"

        exit_rental = request.app.database['Rental'].find_one(
            {"_id": id}
        )

        return exit_rental

    else:
        return "Invalid input"


@router.delete("/{id}", response_description="Delete a rental")
def delete_rental(request: Request, id: str, response: Response):
    deleted_rental = request.app.database['Rental'].delete_one(
        {"_id": id}
    )

    if deleted_rental.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    else:
        return "Rental not found"


@router.get("/car/{id}", response_description="Show rentals of a car")
def get_car(request: Request, id: str):
    rentals = list(request.app.database['Rental'].find(
        {"car_id": id},
        limit=1000
    ))
    return rentals


@router.get("/user/{id}", response_description="Show rentals of a user")
def get_car(request: Request, id: str):
    rentals = list(request.app.database['Rental'].find(
        {"user_id": id},
        limit=1000
    ))
    return rentals
