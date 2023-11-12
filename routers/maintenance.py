import uuid
from typing import List

from fastapi import APIRouter, Request, Response, Body

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT

from models.maintenance import Maintenance, MaintenanceUpdate

router = APIRouter()


@router.get("/", response_description="List all maintenances", response_model=List[Maintenance])
def get_maintenances(request: Request):
    maintenances = list(request.app.database['Maintenance'].find(limit=1000))
    return maintenances


@router.get("/{id}", response_description="Show a maintenance", response_model=Maintenance)
def get_maintenance(request: Request, id: str):
    maintenance = request.app.database['Maintenance'].find_one(
        {"_id": id}
    )
    if not maintenance:
        return JSONResponse(content={"detail": f"Maintenance {id} does not exist"}, status_code=404)
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


@router.put("/{id}", response_description="Update a maintenance", response_model=MaintenanceUpdate)
def update_maintenance(request: Request, id: str, maintenance: MaintenanceUpdate = Body(...)):
    maintenance = {k: v for k, v in maintenance.model_dump().items() if v is not None}

    update_result = request.app.database['Maintenance'].update_one(
        {"_id": id}, {"$set": maintenance}
    )

    if update_result.modified_count == 1:
        update_result = request.app.database['Maintenance'].find_one({'_id': id})
        return update_result
    if update_result.matched_count == 1:
        return JSONResponse(content={"detail": f"Maintenance {id} has not been updated"}, status_code=400)
    return JSONResponse(content={"detail": f"Maintenance {id} not found"}, status_code=404)


@router.delete("/{id}", response_description="Delete a maintenance")
def delete_maintenance(request: Request, id: str, response: Response):
    deleted_maintenance = request.app.database['Maintenance'].delete_one(
        {"_id": id}
    )
    if deleted_maintenance.deleted_count == 0:
        return JSONResponse(content={"detail": f"Maintenance {id} does not exist"}, status_code=404)
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/car/{car_id}", response_description="Show maintenances of a car")
def get_maintenances_of_car(request: Request, car_id: str):
    maintenances = list(request.app.database['Maintenance'].find(
        {"car_id": car_id},
        limit=1000
    ))
    return maintenances
