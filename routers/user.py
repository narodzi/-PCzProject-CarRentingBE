from uuid import UUID
from fastapi import APIRouter, Request, Response, Body, status, HTTPException, Depends
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT
from auth.auth import role_access, user_access, get_bearer_token
from const.roles import Role
from models.user import User, UserUpdate

router = APIRouter()


@router.get("/", response_description="List all users", dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def get_users(request: Request):
    users = list(request.app.database['Users'].find(limit=1000))
    return users


@router.get("/{id}", response_description="Show a user")
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
    # TODO: Integrate this step with keycloak creating user
    user = user.dict()
    new_user = request.app.database['Users'].insert_one(user)
    created_user = request.app.database['Users'].find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user


@router.put("/{id}", response_description="Update a user", dependencies=[Depends(role_access([Role.EMPLOYEE]))])
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


@router.delete("/{id}", response_description="Delete a user", dependencies=[Depends(role_access([Role.EMPLOYEE]))])
def delete_user(request: Request, id: str):
    deleted_user = request.app.database['Users'].delete_one(
        {"_id": id}
    )
    if deleted_user.deleted_count == 0:
        return JSONResponse(content={"detail": f"User {id} does not exist"}, status_code=404)
    return Response(status_code=HTTP_204_NO_CONTENT)


@router.put("/{id}/subtractMoney", response_description="Subtract money to the user")
def subtract_money(request: Request, id: str, amount: float):
    user_access(request, id)
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


@router.put("/{id}/addMoney", response_description="Adding money to the user")
def add_money(request: Request, id: str, amount: float):
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
