from typing import List
from fastapi import APIRouter, Request, Response, Body, status
from fastapi.encoders import jsonable_encoder
from models.user import User  # Import model User zamiast Car
from uuid import UUID
router = APIRouter()

@router.get("/users", response_description="List all users", response_model=List[User])
def read_users(request: Request):
    users = list(request.app.database['Users'].find(limit=1000))
    return users

@router.get("/user/{id}", response_description="Show a user", response_model=User)
def read_user(request: Request, id: UUID):
    user = list(request.app.database['Users'].find_one({"_id": id}))
    return user

@router.post("/adduser", response_model=User)
def add_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.database['Users'].insert_one(user)
    created_user = request.app.database['Users'].find_one({"_id": new_user.inserted_id})
    return created_user

@router.put("/user/{id}", response_description="Update a user", response_model=User)
def update_user(request: Request, id: UUID, user: User = Body(...)):
    user_dict = {k: v for k, v in user.items() if v is not None}

    if len(user_dict) >= 1:
        updated_user = request.app.database['Users'].update_one({"_id": id}, {"$set": user_dict})

        if updated_user.modified_count == 0:
            return "User not found"

        existing_user = request.app.database['Users'].find_one({"_id": id})
        return existing_user

    else:
        return "Invalid input"

@router.delete("/user/{id}", response_description="Delete a user")
def delete_user(request: Request, id: UUID, response: Response):
    deleted_user = request.app.database['Users'].delete_one({"_id": id})

    if deleted_user.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    else:
        return "User not found"