import uuid
from typing import List

from fastapi import APIRouter, Request, Response, Body, Depends

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT
from auth.auth import role_access
from const.roles import Role
from models.maintenance import Maintenance, MaintenanceUpdate

router = APIRouter()


@router.get("/",
            summary="Get all maintenances",
            response_model=List[Maintenance],
            response_description="All maintenances",
            description="Get all maintanances. Must be role employee",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def get_maintenances(request: Request):
    maintenances = list(request.app.database['Maintenance'].find())
    return maintenances


@router.get("/{id}",
            summary="Show maintenance",
            response_model=Maintenance,
            response_description="Maintenance of a given id",
            description="Shows maintenance for a given id. Must be role employee",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def get_maintenance(request: Request, id: str):
    maintenance = request.app.database['Maintenance'].find_one(
        {"_id": id}
    )
    if not maintenance:
        return JSONResponse(content={"detail": f"Maintenance {id} does not exist"}, status_code=404)
    return maintenance


@router.post("/",
             response_model=Maintenance,
             summary="Add new maintenance",
             description="Adds new maintenance. Must be role employee",
             response_description="Created new maintenance",
             dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def add_maintenance(request: Request, maintenance: Maintenance = Body(...)):
    maintenance = jsonable_encoder(maintenance)
    maintenance['_id'] = str(uuid.uuid4())
    new_maintenance = request.app.database['Maintenance'].insert_one(maintenance)
    created_maintenance = request.app.database['Maintenance'].find_one(
        {"_id": new_maintenance.inserted_id}
    )
    return created_maintenance


@router.put("/{id}",
            summary="Update a maintenance",
            response_model=MaintenanceUpdate,
            description="Update maintenance of a given id. Must be role employee",
            response_description="Updated maintenance",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
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


@router.delete("/{id}",
               summary="Delete a maintenance",
               description="Deletes maintenance of a given id. Must be role employee",
               dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def delete_maintenance(request: Request, id: str):
    deleted_maintenance = request.app.database['Maintenance'].delete_one(
        {"_id": id}
    )
    if deleted_maintenance.deleted_count == 0:
        return JSONResponse(content={"detail": f"Maintenance {id} does not exist"}, status_code=404)
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.get("/car/{car_id}",
            summary="Get maintenances of a car",
            description="Get maintenances for a car of a given id. Must be role employee",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def get_maintenances_of_car(request: Request, car_id: str):
    maintenances = list(request.app.database['Maintenance'].find(
        {"car_id": car_id}
    ))
    return maintenances
