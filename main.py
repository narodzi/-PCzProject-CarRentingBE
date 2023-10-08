from typing import Union

from fastapi import FastAPI
from pymongo import MongoClient

from config import MONGO_URL, DATABASE_NAME
from routers.car import router as car_router

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
