from typing import List

from fastapi import APIRouter, Request, Response, Body, status

from fastapi.encoders import jsonable_encoder

from models.maintenance import Maintenance, UpdateMaintenance

router = APIRouter()


@router.get("/", response_description="List all maintenances", response_model=List[Maintenance])
def read_maintenances(request: Request):
    maintenances = list(request.app.database['Maintenance'].find(limit=1000))
    return maintenances


@router.get("/{id}", response_description="Show a maintenance", response_model=Maintenance)
def read_maintenance(request: Request, id: str):
    maintenance = request.app.database['Maintenance'].find_one(
        {"_id": id}
    )
    return maintenance


@router.post("/", response_model=Maintenance)
def add_maintenance(request: Request, maintenance: Maintenance = Body(...)):
    maintenance = jsonable_encoder(maintenance)
    maintenance['_id'] = str(uuid.uuid4())
    new_maintenance = request.app.database['Maintenance'].insert_one(maintenance)
    created_maintenance = request.app.database['Maintenance'].find_one(
        {"_id": new_maintenance.inserted_id}
    )
    return created_maintenance


@router.put("/{id}", response_description="Update a maintenance", response_model=UpdateMaintenance)
def update_maintenance(request: Request, id: str, maintenance: UpdateMaintenance = Body(...)):
    maintenance = {k: v for k, v in maintenance.dict().items() if v is not None}

    if len(maintenance) >= 1:
        updated_maintenance = request.app.database['Maintenance'].update_one(
            {"_id": id}, {"$set": maintenance}
        )

        if updated_maintenance.modified_count == 0:
            return "Maintenance not found"

        exit_maintenance = request.app.database['Maintenance'].find_one(
            {"_id": id}
        )

        return exit_maintenance

    else:
        return "Invalid input"


@router.delete("/{id}", response_description="Delete a maintenance")
def delete_maintenance(request: Request, id: str, response: Response):
    deleted_maintenance = request.app.database['Maintenance'].delete_one(
        {"_id": id}
    )

    if deleted_maintenance.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    else:
        return "Maintenance not found"


@router.get("/car/{id}", response_description="Show maintenances of a car")
def get_maintenances_of_car(request: Request, id: str):
    maintenances = list(request.app.database['Maintenance'].find(
        {"car_id": id},
        limit=1000
    ))
    return maintenances
