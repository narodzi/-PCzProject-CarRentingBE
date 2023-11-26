import os
import jwt
from fastapi import HTTPException
from starlette import status
from starlette.requests import Request as StarletteRequest
from fastapi.requests import Request


class Keycloak:
    def __init__(self, request: Request):
        self._request = request

    @staticmethod
    def _get_bearer_token(request: StarletteRequest) -> str:
        """
        Get Bearer token value from request
        :param request: request to get the token from
        :return: token without the "Bearer " prefix
        """
        if os.getenv("DEBUG") == "1":
            return ""
        authorization_header = request.headers.get("authorization")
        if authorization_header:
            return authorization_header.replace("Bearer ", "")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No access token')

    def get_user_id(self):
        jwt_token = self._get_bearer_token(self._request)
        options = {"verify_signature": False}
        decoded_data = jwt.decode(jwt_token, algorithms=["RS256"], options=options)
        return decoded_data["sub"]
