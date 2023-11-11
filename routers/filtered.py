import http.client
import json
import uuid
from typing import List

from fastapi import APIRouter, Request, Response, Body, status, Query

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT
from models.filtered import RentalSearchDto

from datetime import datetime


router = APIRouter()


@router.post("/test2", response_description="Show a car")
def get_car(request: Request, params: RentalSearchDto = Body(...)):
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
    array = [x['car_id'] for x in rentals if not((datetime.strptime(((x['start_date']).split("T"))[0], '%Y-%m-%d').date()-datetime.strptime(((params.end_date).split("T"))[0], '%Y-%m-%d').date()).days>0 or (datetime.strptime(((x['end_date']).split("T"))[0], '%Y-%m-%d').date()-datetime.strptime(((params.start_date).split("T"))[0], '%Y-%m-%d').date()).days<0)]
    #array2 = [x['car_id'] for x in rentals if not(((parse_datetime(x['start_date'])).date()-(parse_datetime(params.end_date)).date()).days > 0 or ((parse_datetime(x['end_date'])).date()-(parse_datetime(params.start_date)).date()).days < 0)]

    filtered_cars = [car for car in cars if car['_id'] not in array]
    if not cars:
        return JSONResponse(content={"detail": f"Car {id} does not exist"}, status_code=404)
    return filtered_cars


@router.get("/test", response_description="Show a car")
def get_car(request: Request, number_of_seats: int, production_year: int):
    query = {}
    query["number_of_seats"] = number_of_seats
    query["production_year"] = {"$gte": production_year}
    car = list(request.app.database['Cars'].find(
        query
    ))
    print(car)
    if not car:
        return JSONResponse(content={"detail": f"Car {id} does not exist"}, status_code=404)
    return car


@router.get("/", response_description="Show a car")
def get_car(request: Request, number_of_seats: int):
    cars = list(request.app.database['Cars'].find(limit=1000))
    # cars = request.app.database['Cars'].find(
    #     {"brand": brand}
    # )
    query = {}

    filtered_cars = [car for car in cars if car["number_of_seats"] == number_of_seats]
    print(filtered_cars)
    if not filtered_cars:
        return JSONResponse(content={"detail": f"Car {id} does not exist"}, status_code=404)
    return filtered_cars
#
# @router.get("/search", response_model=List[RentalSearchResultDto])
# async def search_cars(params: RentalSearchDto,request: Request):
#     # Przykładowa logika przeszukiwania bazy danych MongoDB
#     cars = list(request.app.database['Cars'].find(limit=1000))
#     query = {}
#     if params.brand:
#         query["brand"] = params.brand
#     if params.type:
#         query["type"] = params.type
#     if params.earliest_production_year:
#         query["production_year"] = {"$gte": params.earliest_production_year}
#     if params.gearbox:
#         query["gearbox"] = params.gearbox
#     if params.fuel_type:
#         query["fuel_type"] = params.fuel_type
#     if params.minimal_horse_power:
#         query["horse_power"] = {"$gte": params.minimal_horse_power}
#     if params.number_of_seats:
#         query["number_of_seats"] = {"$gte": params.number_of_seats}
#     if params.number_of_doors:
#         query["number_of_doors"] = {"$gte": params.number_of_doors}
#     if params.minimal_trunk_size:
#         query["trunk_size"] = {"$gte": params.minimal_trunk_size}
#     if params.minimal_price:
#         query["price"] = {"$gte": params.minimal_price}
#     if params.maximal_price:
#         query["price"] = {"$lte": params.maximal_price}
#
#     # Przeszukaj bazę danych
#     results = list(request.app.database['Cars'].find(query))
#
#     # Mapowanie wyników do formatu RentalSearchResultDto
#     mapped_results = []
#     for result in results:
#         mapped_result = RentalSearchResultDto(
#             id=str(result["_id"]),
#             img_url=result["img_url"],
#             brand=result["brand"],
#             model=result["model"],
#             number_of_seats=result["number_of_seats"],
#             horse_power=result["horse_power"],
#             gearbox=result["gearbox"],
#             trunk=result["trunk"],
#             fuel_type=result["fuel_type"],
#             number_of_doors=result["number_of_doors"],
#             color=result["color"],
#             production_year=result["production_year"],
#             fuel_consumption=result["fuel_consumption"],
#             price_overall=result["price_overall"],
#         )
#         mapped_results.append(mapped_result)
#
#     return mapped_results
