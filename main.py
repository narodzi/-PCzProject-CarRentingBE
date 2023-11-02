from typing import Union

import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient

from config import MONGO_URL, DATABASE_NAME
from routers.car import router as car_router
from routers.user import router as user_router
from routers.rental import router as rental_router

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(MONGO_URL)
    app.database = app.mongodb_client[DATABASE_NAME]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(car_router, tags=["cars"], prefix="/cars")
app.include_router(user_router, tags=["users"], prefix="/users")
app.include_router(rental_router, tags=["rentals"], prefix="/rentals")
