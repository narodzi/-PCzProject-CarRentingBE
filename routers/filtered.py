from datetime import datetime

from fastapi import APIRouter, Request, Body

from const import const
from models.car import Car
from models.filtered import RentalSearch, RentalSearchResult

from models.rental import Rental

router = APIRouter()


@router.post("/", response_description="Show a car")
def get_car(request: Request, params: RentalSearch = Body(...)) -> list[RentalSearchResult]:
    query = {}

    if params.number_of_seats is not None:
        query["number_of_seats"] = params.number_of_seats
    if params.brand is not None:
        query["brand"] = params.brand
    if params.type is not None:
        query["type"] = params.type
    if params.gearbox is not None:
        query["gearbox"] = params.gearbox
    if params.fuel_type is not None:
        query["fuel_type"] = params.fuel_type
    if params.number_of_doors is not None:
        query["number_of_doors"] = params.number_of_doors

    if params.earliest_production_year is not None:
        query["production_year"] = {"$gte": params.earliest_production_year}
    if params.minimal_horse_power is not None:
        query["horse_power"] = {"$gte": params.minimal_horse_power}
    if params.minimal_trunk_size is not None:
        query["trunk"] = {"$gte": params.minimal_trunk_size}
    if params.minimal_price is not None:
        query["price"] = {"$gte": params.minimal_price, "$lte": params.maximal_price}

    cars: list[Car] = list(map(Car.model_validate, request.app.database['Cars'].find(query)))
    cars = [car for car in cars if car.available]

    rentals: list[Rental] = list(map(Rental.model_validate, request.app.database['Rental'].find()))
    rentals = [rental for rental in rentals if not rental.is_canceled]

    start_date = datetime.strptime(params.start_date, const.DATE_FORMAT)
    end_date = datetime.strptime(params.end_date, const.DATE_FORMAT)
    rentals_id = [rental.car_id for rental in rentals
                  if datetime.strptime(rental.start_date, const.DATE_FORMAT) < end_date and
                  datetime.strptime(rental.end_date, const.DATE_FORMAT) > start_date]

    filtered_cars = [car for car in cars if car.id not in rentals_id]

    result_dto_list = [
        RentalSearchResult(
            _id=car.id,
            image_url=car.image_url,
            brand=car.brand,
            model=car.model,
            number_of_seats=car.number_of_seats,
            horse_power=car.horse_power,
            gearbox=car.gearbox,
            trunk=car.trunk,
            fuel_type=car.fuel_type,
            number_of_doors=car.number_of_doors,
            color=car.color,
            production_year=car.production_year,
            fuel_consumption=car.fuel_consumption,
            price_overall=car.price * (end_date - start_date).days,
        )
        for car in filtered_cars
    ]
    return result_dto_list
