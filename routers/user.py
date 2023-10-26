from fastapi import APIRouter, Request, Response, Body, status
from fastapi.encoders import jsonable_encoder
from typing import List
from Wypozyczalnia_ProjektPCz.models.user import User

router = APIRouter()


@router.get("/user/all", response_description="List all users", response_model=List[User])
def read_users(request: Request):
    users = list(request.app.database['Users'].find(limit=1000))
    return users


@router.get("/user/{id}", response_description="Show a user", response_model=User)
def read_user(request: Request, id: str):
    user = list(request.app.database['Users'].find_one({"_id": id}))
    return user


@router.post("/user/add", response_model=User)
def add_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.database['Users'].insert_one(user)
    created_user = request.app.database['Users'].find_one({"_id": new_user.inserted_id})
    return created_user


@router.delete("/user/{id}", response_description="Delete a user")
def delete_user(request: Request, id: str, response: Response):
    deleted_user = request.app.database['Users'].delete_one({"_id": id})

    if deleted_user.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    else:
        return "User not found"
