"""
Contains decorator to use when an endpoint needs certain role to execute
"""
from typing import List

from starlette import status
from starlette.requests import Request as StarletteRequest

import jwt
from fastapi import Depends, HTTPException

from const.roles import Role


def get_bearer_token(request: StarletteRequest):
    authorization_header = request.headers.get("authorization")
    if authorization_header:
        return authorization_header.replace("Bearer ", "")
    return ""


def role_access(roles: List[Role]):
    def authorize(jwt_token: str = Depends(get_bearer_token)):
        options = {"verify_signature": False}
        decoded_data = jwt.decode(jwt_token, algorithms=["RS256"], options=options)
        for role in roles:
            if role.name.lower() in decoded_data['realm_access']['roles']:
                return
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return authorize

# return wrapper
#
# def role_access(roles: List[str]):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             jwt_token = args[0].headers.get('authorization').replace("Bearer ", "")
#             options = {"verify_signature": False}
#             decoded_data = jwt.decode(jwt_token, algorithms=["RS256"], options=options)
#             func(*args, **kwargs)
#         return wrapper
#     return decorator
