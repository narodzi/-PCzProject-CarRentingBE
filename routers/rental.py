import uuid
from typing import List

from fastapi import APIRouter, Request, Response, Body, status, Depends

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT

from auth.role_access import role_access
from const.roles import Role
from models.rental import Rental, RentalUpdate

router = APIRouter()


@router.get("/", response_description="List all rentals", response_model=List[Rental],
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def read_rentals(request: Request):
    rentals = list(request.app.database['Rental'].find(limit=1000))
    return rentals


@router.get("/{id}", response_description="Show a rental", response_model=Rental,
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def read_rental(request: Request, id: str):
    rental = request.app.database['Rental'].find_one(
        {"_id": id}
    )
    if not rental:
        return JSONResponse(content={"detail": f"Rental {id} does not exist"}, status_code=404)
    return rental


@router.post("/", response_model=Rental, dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def add_rental(request: Request, rental: RentalUpdate = Body(...)):
    rental = jsonable_encoder(rental)
    rental['_id'] = str(uuid.uuid4())
    new_rental = request.app.database['Rental'].insert_one(rental)
    created_rental = request.app.database['Rental'].find_one(
        {"_id": new_rental.inserted_id}
    )
    return created_rental


@router.put("/{id}", response_description="Update a rental", response_model=RentalUpdate,
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def update_rental(request: Request, id: str, rental: RentalUpdate = Body(...)):
    rental = {k: v for k, v in rental.dict().items() if v is not None}

    update_result = request.app.database['Rental'].update_one(
        {"_id": id}, {"$set": rental}
    )

    if update_result.modified_count == 1:
        update_result = request.app.database['Rental'].find_one({'_id': id})
        return update_result
    if update_result.matched_count == 1:
        return JSONResponse(content={"detail": f"Rental {id} has not been updated"}, status_code=400)
    return JSONResponse(content={"detail": f"Rental {id} not found"}, status_code=404)


@router.delete("/{id}", response_description="Delete a rental",
               dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def delete_rental(request: Request, id: str, response: Response):
    deleted_rental = request.app.database['Rental'].delete_one(
        {"_id": id}
    )
    if deleted_rental.deleted_count == 0:
        return JSONResponse(content={"detail": f"Rental {id} does not exist"}, status_code=404)
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/car/{car_id}", response_description="Show rentals of a car",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def get_rentals_of_car(request: Request, car_id: str):
    rentals = list(request.app.database['Rental'].find(
        {"car_id": car_id},
        limit=1000
    ))
    return rentals


@router.get("/user/{user_id}", response_description="Show rentals of a user")
def get_rentals_of_user(request: Request, user_id: str):
    # TODO: Check here if this is the same user that asks for its rentals
    rentals = list(request.app.database['Rental'].find(
        {"user_id": user_id},
        limit=1000
    ))
    return rentals
