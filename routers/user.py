from uuid import UUID
from fastapi import APIRouter, Request, Response, Body, status, HTTPException, Depends
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT
from auth.auth import role_access, user_access, get_bearer_token
from const.roles import Role
from models.user import User, UserUpdate, UserDetails
from services.keycloak import Keycloak

router = APIRouter()


@router.get("/", response_description="List all users", description="Must be role employee",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def get_users(request: Request):
    users = list(request.app.database['Users'].find())
    return users


@router.get("/{id}", description="Must be role employee or the same user", response_description="Show a user")
def get_user(request: Request, id: str):
    user_access(request, id)
    user = request.app.database['Users'].find_one(
        {"_id": id}
    )
    if not user:
        return JSONResponse(content={"detail": f"User {id} does not exist"}, status_code=404)
    return user


@router.post("/", response_description="Add a user")
def add_user(request: Request, user: User = Body(...)):
    user = user.model_dump(by_alias=True)
    new_user = request.app.database['Users'].insert_one(user)
    created_user = request.app.database['Users'].find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user


@router.put("/{id}", response_description="Update a user", description="Must be role employee",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def update_user(request: Request, id: str, user: UserUpdate = Body(...)):
    user_data = user.dict(exclude_unset=True)

    update_result = request.app.database['Users'].update_one(
        {"_id": id}, {"$set": user_data}
    )

    if update_result.modified_count == 1:
        updated_user = request.app.database['Users'].find_one({'_id': id})
        return updated_user
    if update_result.matched_count == 1:
        return JSONResponse(content={"detail": f"User {id} has not been updated"}, status_code=400)
    return JSONResponse(content={"detail": f"User {id} not found"}, status_code=404)


@router.delete("/{id}", response_description="Delete a user", description="Must be role employee",
               dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def delete_user(request: Request, id: str):
    deleted_user = request.app.database['Users'].delete_one(
        {"_id": id}
    )
    if deleted_user.deleted_count == 0:
        return JSONResponse(content={"detail": f"User {id} does not exist"}, status_code=404)
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.put("/{id}/subtractMoney", description="Must be role employee",
            response_description="Subtract money to the user",
            dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def subtract_money(request: Request, id: str, amount: int):
    user = request.app.database['Users'].find_one(
        {"_id": id}
    )
    if user["wallet_balance"] >= amount:
        user["wallet_balance"] -= amount
        request.app.database['Users'].update_one(
            {"_id": id},
            {"$set": {"wallet_balance": user["wallet_balance"]}}
        )
        return {"message": f"Successfully subtract {amount} to user's wallet. New balance: {user['wallet_balance']}"}
    else:
        raise HTTPException(status_code=400, detail="Insufficient balance")


@router.put("/{id}/addMoney", description="Must be role employee or the same user",
            response_description="Adding money to the user")
def add_money(request: Request, id: str, amount: int):
    user_access(request, id)
    user = request.app.database['Users'].find_one(
        {"_id": id}
    )
    user["wallet_balance"] += amount
    request.app.database['Users'].update_one(
        {"_id": id},
        {"$set": {"wallet_balance": user["wallet_balance"]}}
    )
    return {"message": f"Successfully added {amount} to user's wallet. New balance: {user['wallet_balance']}"}


@router.get("/mongo_exist/{user_id}",
            summary="Checks if current user exist in mongo",
            description="Must be role employee or the same user",
            response_description="204 if exists. 404 if not")
def is_user_data_in_mongo(request: Request, user_id: str):
    user_access(request, user_id)
    user = request.app.database['Users'].find_one(
        {"_id": user_id}
    )
    if user:
        return Response(status_code=HTTP_204_NO_CONTENT)
    return JSONResponse(content={"detail": f"User {user_id} does not yet exist"}, status_code=404)


@router.get("/details/", summary="Gets full user info for logged in user", response_description="User info")
def get_user_details(request: Request) -> UserDetails:
    token_info = Keycloak(request).get_token_info()
    user_id = token_info['sub']
    first_name = token_info['given_name']
    last_name = token_info['family_name']
    email = token_info['email']
    username = token_info['preferred_username']
    user = request.app.database['Users'].find_one(
        {"_id": user_id}
    )
    return UserDetails(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        licence_number=user['licence_number'],
        wallet_balance=user['wallet_balance'],
        country=user['country'],
        city=user['city'],
        street=user['street'],
        postal_code=user['postal_code'],
        house_number=user['house_number'],
        apartment_number=user['apartment_number'],
        phone_number=user['phone_number'],
    )