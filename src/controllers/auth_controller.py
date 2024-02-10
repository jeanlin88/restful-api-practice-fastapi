from fastapi import APIRouter, HTTPException, status

from errors.custom_errors import IncorrectPassword, UserNotFoundError
from schemas.auth import Login, ResponseLoginSuccess
from schemas.response import get_error_responses_dict
from use_cases.auth_use_case import AuthUseCase


class AuthController:
    router: APIRouter
    auth_use_case: AuthUseCase

    def __init__(self, auth_use_case: AuthUseCase):
        self.auth_use_case = auth_use_case
        self.router = APIRouter()
        self.router.add_api_route(
            path="/",
            endpoint=self.login,
            response_model=ResponseLoginSuccess,
            status_code=status.HTTP_200_OK,
            responses=get_error_responses_dict(
                status.HTTP_401_UNAUTHORIZED,
            ),
            methods=["POST"],
        )
        pass

    async def login(self, login_data: Login):
        try:
            result = await self.auth_use_case.login(login_data=login_data)
            return ResponseLoginSuccess(result=result)
        except (UserNotFoundError, IncorrectPassword):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="login failed",
            )
    pass
