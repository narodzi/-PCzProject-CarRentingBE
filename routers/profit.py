#TODO delete unused imports
import uuid
from datetime import datetime, timedelta
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


#TODO send period
# zyski z ostaniego miesiaca, ostaniego roku, ogółem
@router.get("/",
            summary="Get profits with period",
            #TODO description
            response_description="",
            # description="Must be role employee",
            # dependencies=[Depends(role_access([Role.EMPLOYEE]))]
            )
def get_profit_with_period(request: Request) -> int:
    rentals = list(map(Rental.model_validate, request.app.database['Rental'].find()))
    active_rentals = [x for x in rentals if x.is_canceled is False]
    today = datetime.now()
    start_date = today

    #TODO SEND request period
    period = "last_month"

    profits = 0
    if period == "last_month":
        start_date -= timedelta(days=30)
        print(start_date)
        profits = sum(
            rental.price_overall for rental in active_rentals if
            start_date <= datetime.fromisoformat(rental.start_date) <= today)
    elif period == "last_year":
        start_date -= timedelta(days=365)
        profits = sum(
            rental.price_overall for rental in active_rentals if
            start_date <= datetime.fromisoformat(rental.start_date) <= today)
    elif period == "all_time":
        start_date = datetime.min
        profits = sum(
            rental.price_overall for rental in active_rentals if
            datetime.fromisoformat(rental.start_date) >= start_date)
    return profits


# zyski z kazdego miesiaca w roku
@router.get("/monthly",
            summary="Get profits with period",
            #TODO description
            response_description="",
            # description="Must be role employee",
            # dependencies=[Depends(role_access([Role.EMPLOYEE]))]
            )
def get_profits_from_12month(request: Request):
    rentals = list(map(Rental.model_validate, request.app.database['Rental'].find()))
    active_rentals = [x for x in rentals if x.is_canceled is False]
    today = datetime.now()
    profits_by_month = {}

    for i in range(12):
        month = (today.month - i - 1) % 12 + 1
        year = today.year
        start_date = datetime(year, month, 1)
        end_date = start_date.replace(day=1, month=month % 12 + 1, year=year if month % 12 != 0 else year + 1)
        profits = sum(rental.price_overall for rental in active_rentals
                      if start_date <= datetime.fromisoformat(rental.start_date) < end_date)

        profits_by_month[start_date.strftime("%Y-%m")] = profits

    return profits_by_month
