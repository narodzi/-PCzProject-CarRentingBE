import os
from typing import List

import jwt
from starlette import status
from starlette.requests import Request as StarletteRequest
from fastapi import HTTPException, Depends

from const.roles import Role


def get_bearer_token(request: StarletteRequest) -> str:
    """
    Get Bearer token value from request
    :param request: request to get the token from
    :return: token without the "Bearer " prefix
    """
    authorization_header = request.headers.get("authorization")
    if authorization_header:
        return authorization_header.replace("Bearer ", "")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No access token')


def role_access(roles: List[Role]):
    """
    Get function that will validate if a user has on of a given roles and raise HTTPException if not
    :param roles: list of roles to check
    :return: function for validation
    """
    def authorize(jwt_token: str = Depends(get_bearer_token)):
        options = {"verify_signature": False}
        decoded_data = jwt.decode(jwt_token, algorithms=["RS256"], options=options)
        for role in roles:
            if role.name.lower() in decoded_data['realm_access']['roles']:
                return
        if os.getenv("DEBUG") != "1":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return authorize


def user_access(request: StarletteRequest, user_id: str):
    """
    Validate if a user has access to a user data of a given user_id and
    raise HTTPException if not
    :param request: request to check
    :param user_id: user id to check
    """
    jwt_token = get_bearer_token(request)
    options = {"verify_signature": False}
    decoded_data = jwt.decode(jwt_token, algorithms=["RS256"], options=options)
    if decoded_data["sub"] == user_id:
        return
    if Role.EMPLOYEE.name.lower() in decoded_data['realm_access']['roles']:
        return
    if os.getenv("DEBUG") != "1":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
