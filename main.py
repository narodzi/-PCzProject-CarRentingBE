from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pymongo import MongoClient

from config import MONGO_URL, DATABASE_NAME
from routers.car import router as car_router
from routers.user import router as user_router
from routers.rental import router as rental_router
from routers.filtered import router as filtered_router
from routers.maintenance import router as maintenance_router
from routers.profit import router as profit_router

app = FastAPI(
    title="Car Renting",
    description="API for car renting service",
    version="1.0.0"
)

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


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
app.include_router(filtered_router, tags=["filtered"], prefix="/filtered")
app.include_router(maintenance_router, tags=["maintenances"], prefix="/maintenances")
app.include_router(profit_router, tags=["profit"], prefix="/profit")
