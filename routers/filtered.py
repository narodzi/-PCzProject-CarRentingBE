from fastapi import APIRouter, Request, Body

from models.filtered import RentalSearch, RentalSearchResult

from isodate import parse_datetime

router = APIRouter()


@router.post("/", response_description="Show a car")
def get_car(request: Request, params: RentalSearch = Body(...)):
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

    cars = list(request.app.database['Cars'].find(query))

    rentals = list(request.app.database['Rental'].find(limit=1000))

    start_date = (parse_datetime(params.start_date)).date()
    end_date = (parse_datetime(params.end_date)).date()
    array = [x['car_id'] for x in rentals if not (((parse_datetime(x['start_date'])).date() - end_date).days > 0 or (
            (parse_datetime(x['end_date'])).date() - start_date).days < 0)]

    filtered_cars = [car for car in cars if car['_id'] not in array]

    result_dto_list = [
        RentalSearchResult(
            _id=item['_id'],
            image_url=item['image_url'],
            brand=item['brand'],
            model=item['model'],
            number_of_seats=item['number_of_seats'],
            horse_power=item['horse_power'],
            gearbox=item['gearbox'],
            trunk=item['trunk'],
            fuel_type=item['fuel_type'],
            number_of_doors=item['number_of_doors'],
            color=item['color'],
            production_year=item['production_year'],
            fuel_consumption=item['fuel_consumption'],
            price_overall=item['price'] * (end_date - start_date).days,
        )
        for item in filtered_cars
    ]

    return result_dto_list
