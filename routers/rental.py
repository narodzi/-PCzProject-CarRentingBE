import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, Response, Body, Depends

from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT
from auth.auth import role_access, user_access
from const import const
from const.roles import Role
from models.car import Car
from models.rental import Rental, RentalAdd

from models.user import User

router = APIRouter()


@router.get("/",
            summary="Get all rentals",
            response_model=List[Rental],
            description="Get all rentals. Must be role employee",
            response_description="All rentals",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def read_rentals(request: Request):
    rentals = list(request.app.database['Rental'].find())
    return rentals


@router.get("/{id}",
            summary="Get a rental",
            response_model=Rental,
            description="Get rental of a given id. Must be role employee or the same user",
            response_description="Rental of a given id")
def read_rental(request: Request, id: str):
    rental = request.app.database['Rental'].find_one(
        {"_id": id}
    )
    if not rental:
        return JSONResponse(content={"detail": f"Rental {id} does not exist"}, status_code=404)
    user_access(request, rental['user_id'])
    return rental


@router.post("/",
             summary="Add new rental",
             response_model=Rental,
             description="Adding new rental. Must be role employee or the same user",
             response_description="Created rental")
def add_rental(request: Request, rental_add: RentalAdd = Body(...)):
    car_dict = request.app.database['Cars'].find_one(
        {"_id": rental_add.car_id}
    )
    car = Car.model_validate(car_dict)
    user_id = rental_add.user_id
    user_access(request, user_id)
    if not car.available:
        return JSONResponse(content={"detail": f"Car {rental_add.car_id} is not available"}, status_code=400)

    start_date = datetime.strptime(rental_add.start_date, const.DATE_FORMAT)
    end_date = datetime.strptime(rental_add.end_date, const.DATE_FORMAT)
    if start_date > end_date:
        return JSONResponse(content={"detail": f"start_date must be before end_date"},
                            status_code=400)
    days_to_rent = (end_date - start_date).days
    if days_to_rent == 0:
        return JSONResponse(content={"detail": f"Rent time must be longer than 0 days"},
                            status_code=400)

    car_rentals_dict = request.app.database['Rental'].find({"car_id": car.id})
    car_rentals: list[Rental] = list(map(Rental.model_validate, car_rentals_dict))
    for car_rental in car_rentals:
        if car_rental.is_canceled:
            continue
        start_date_existing = datetime.strptime(car_rental.start_date, const.DATE_FORMAT)
        end_date_existing = datetime.strptime(car_rental.end_date, const.DATE_FORMAT)
        if end_date_existing <= start_date or start_date_existing >= end_date:
            continue
        return JSONResponse(content={"detail": f"Car is rented in that time"},
                            status_code=400)
    price_overall = car.price * days_to_rent

    user_dict = request.app.database['Users'].find_one(
        {"_id": user_id}
    )
    user = User.model_validate(user_dict)
    if user.wallet_balance < price_overall:
        return JSONResponse(content={"detail": f"User {user_id} does not have sufficient balance"},
                            status_code=400)
    user.wallet_balance -= price_overall
    request.app.database['Users'].update_one(
        {"_id": user_id},
        {"$set": {"wallet_balance": user.wallet_balance}}
    )
    rental_to_add = Rental.model_validate({
        '_id': str(uuid.uuid4()),
        'car_id': rental_add.car_id,
        'user_id': user_id,
        'start_date': rental_add.start_date,
        'end_date': rental_add.end_date,
        'price_overall': price_overall,
        'is_canceled': False,
    })

    request.app.database['Rental'].insert_one(rental_to_add.model_dump(by_alias=True))
    created_rental = request.app.database['Rental'].find_one(
        {"_id": rental_to_add.id}
    )
    return created_rental


@router.delete("/{id}",
               response_description="Delete a rental",
               description="Delete rental of a given id. Must be role employee",
               dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def delete_rental(request: Request, id: str, response: Response):
    deleted_rental = request.app.database['Rental'].delete_one(
        {"_id": id}
    )
    if deleted_rental.deleted_count == 0:
        return JSONResponse(content={"detail": f"Rental {id} does not exist"}, status_code=404)
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/car/{car_id}",
            summary="Get rentals of given car",
            description="Get rentals for a car of a given id. Must be role employee",
            response_description="Rentals of a given car",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def get_rentals_of_car(request: Request, car_id: str):
    rentals = list(request.app.database['Rental'].find(
        {"car_id": car_id}
    ))
    return rentals


@router.get("/user/{user_id}",
            summary="Get rentals of given user",
            description="Get rentals for user of given user id. Must be role employee or the same user",
            response_description="Rentals of a user")
def get_rentals_of_user(request: Request, user_id: str):
    user_access(request, user_id)
    rentals = list(request.app.database['Rental'].find(
        {"user_id": user_id},
    ))
    return rentals


@router.post("/cancel/{rental_id}",
             summary='Cancel rental',
             description="Cancel rental of a given id. Must be role employee or the same user",
             response_description="Whether the rental was canceled successfully",
             status_code=HTTP_204_NO_CONTENT)
def cancel_rental(request: Request, rental_id: str):
    rental_dict = request.app.database['Rental'].find_one(
        {"_id": rental_id}
    )
    if not rental_dict:
        return JSONResponse(content={"detail": f"Rental {rental_id} does not exist"}, status_code=404)
    rental = Rental.model_validate(rental_dict)
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
