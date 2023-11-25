import uuid
from typing import List

from fastapi import APIRouter, Request, Response, Body, status, Depends

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT
from auth.auth import role_access, user_access
from const.roles import Role
from models.rental import Rental, RentalUpdate

from isodate import parse_datetime

router = APIRouter()


@router.get("/", response_description="List all rentals", response_model=List[Rental],
            description="Must be role employee", dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def read_rentals(request: Request):
    rentals = list(request.app.database['Rental'].find(limit=1000))
    return rentals


@router.get("/{id}", response_description="Show a rental", response_model=Rental,
            description="Must be role employee", dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def read_rental(request: Request, id: str):
    rental = request.app.database['Rental'].find_one(
        {"_id": id}
    )
    if not rental:
        return JSONResponse(content={"detail": f"Rental {id} does not exist"}, status_code=404)
    return rental


@router.post("/", response_model=Rental, description="Must be role employee",
             dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def add_rental(request: Request, rental: RentalUpdate = Body(...)):
    rental = jsonable_encoder(rental)

    car = request.app.database['Cars'].find_one(
        {"_id": rental['car_id']}
    )

    if not car['available']:
        return JSONResponse(content={"detail": f"Car {rental['car_id']} is not available"}, status_code=400)

    user = request.app.database['Users'].find_one(
        {"_id": rental['user_id']}
    )

    price = car['price'] * (parse_datetime(rental['end_date']).date() - parse_datetime(rental['start_date']).date()).days

    if user['wallet_balance'] < price:
        return JSONResponse(content={"detail": f"User {rental['user_id']} does not have sufficient balance"},
                            status_code=400)

    rental['_id'] = str(uuid.uuid4())
    new_rental = request.app.database['Rental'].insert_one(rental)
    created_rental = request.app.database['Rental'].find_one(
        {"_id": new_rental.inserted_id}
    )
    return created_rental


@router.put("/{id}", response_description="Update a rental", response_model=RentalUpdate,
            description="Must be role employee", dependencies=[Depends(role_access([Role.EMPLOYEE]))])
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
               description="Must be role employee", dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def delete_rental(request: Request, id: str, response: Response):
    deleted_rental = request.app.database['Rental'].delete_one(
        {"_id": id}
    )
    if deleted_rental.deleted_count == 0:
        return JSONResponse(content={"detail": f"Rental {id} does not exist"}, status_code=404)
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/car/{car_id}", response_description="Show rentals of a car",
            description="Must be role employee", dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def get_rentals_of_car(request: Request, car_id: str):
    rentals = list(request.app.database['Rental'].find(
        {"car_id": car_id},
        limit=1000
    ))
    return rentals


@router.get("/user/{user_id}", description="Must be role employee or the same user",
            response_description="Show rentals of a user")
def get_rentals_of_user(request: Request, user_id: str):
    user_access(request, user_id)
    rentals = list(request.app.database['Rental'].find(
        {"user_id": user_id},
        limit=1000
    ))
    return rentals


@router.post("/cancel/{rental_id}",
             summary='Cancel rental',
             description="Must be role employee or the same user",
             response_description="Rental canceled successfully",
             status_code=HTTP_204_NO_CONTENT)
def cancel_rental(request: Request, rental_id: str):
    rental_dict = request.app.database['Rental'].find_one(
        {"_id": rental_id}
    )
    if not rental_dict:
        return JSONResponse(content={"detail": f"Rental {rental_id} does not exist"}, status_code=404)
    rental = Rental.from_dict(rental_dict)
    user_access(request, rental.user_id)
    if rental.is_canceled:
        return JSONResponse(content={"detail": f"Rental {rental_id} already canceled"}, status_code=400)
    request.app.database['Rental'].update_one(
        {"_id": rental_id}, {"$set": {"is_canceled": True}}
    )
    request.app.database['Users'].update_one(
        {"_id": rental.user_id}, {"$inc": {"wallet_balance": rental.price_overall}}
    )
    return Response(status_code=HTTP_204_NO_CONTENT)
