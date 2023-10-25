from typing import List

from fastapi import APIRouter, Request, Response, Body, status

from fastapi.encoders import jsonable_encoder

from models.rental import Rental, UpdateRental

router = APIRouter()


@router.get("/rental/all", response_description="List all rentals", response_model=List[Rental])
def read_rentals(request: Request):
    rentals = list(request.app.database['Rentals'].find(limit=1000))
    return rentals


@router.get("/rental/{id}", response_description="Show a rental", response_model=Rental)
def read_rental(request: Request, id: str):
    rental = list(request.app.database['Rentals'].find_one(
        {"_id": id}
    ))
    return rental


@router.post("/rental/add", response_model=Rental)
def add_rental(request: Request, rental: Rental = Body(...)):
    rental = jsonable_encoder(rental)
    new_rental = request.app.database['Rentals'].insert_one(rental)
    create_rental = request.app.database['Rentals'].find_one(
        {"_id": new_rental.inserted_id}
    )
    return create_rental


@router.put("/rental/{id}", response_description="Update a rental", response_model=UpdateRental)
def update_rental(request: Request, id: str, rental: UpdateRental = Body(...)):
    rental = {k: v for k, v in rental.dict().items() if v is not None}

    if len(rental) >= 1:
        updated_rental = request.app.database['Rentals'].update_one(
            {"_id": id}, {"$set": rental}
        )

        if updated_rental.modified_count == 0:
            return "Rental not found"

        exit_rental = request.app.database['Rentals'].find_one(
            {"_id": id}
        )

        return exit_rental

    else:
        return "Invalid input"


@router.delete("/rental/{id}", response_description="Delete a rental")
def delete_rental(request: Request, id: str, response: Response):
    deleted_rental = request.app.database['Rentals'].delete_one(
        {"_id": id}
    )

    if deleted_rental.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    else:
        return "Rental not found"