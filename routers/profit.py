from datetime import datetime

from fastapi import APIRouter, Request, Depends

from auth.auth import role_access
from const.roles import Role
from models.rental import Rental


router = APIRouter()


@router.get("/",
            summary="Get profits with period",
            response_description="",
            description="Must be role employee",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))]
            )
def get_profit_with_period(request: Request) -> int:
    rentals = list(map(Rental.model_validate, request.app.database['Rental'].find()))
    active_rentals = [x for x in rentals if x.is_canceled is False]
    start_date = datetime.min
    profits = sum(
        rental.price_overall for rental in active_rentals if
        datetime.fromisoformat(rental.start_date) >= start_date)
    return profits


@router.get("/monthly",
            summary="Get profits with period",
            response_description="",
            description="Must be role employee",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))]
            )
def get_profits_from_12month(request: Request) -> list[int]:
    rentals = list(map(Rental.model_validate, request.app.database['Rental'].find()))
    active_rentals = [x for x in rentals if x.is_canceled is False]
    today = datetime.now()
    profits_by_month = []

    for i in range(12):
        month = (today.month - i - 1) % 12 + 1
        year = today.year
        start_date = datetime(year, month, 1)
        end_date = start_date.replace(day=1, month=month % 12 + 1, year=year if month % 12 != 0 else year + 1)
        profits = sum(rental.price_overall for rental in active_rentals
                      if start_date <= datetime.fromisoformat(rental.start_date) < end_date)

        profits_by_month.append(profits)
    profits_by_month.reverse()

    return profits_by_month
