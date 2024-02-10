from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from errors.custom_errors import NotAdminError, UserNotFoundError
from middleware.auth_middleware import AuthMiddleware
from schemas.request import AuthedRequest
from schemas.response import get_error_responses_dict
from schemas.user import (
    ResponseUserDetailGet,
    ResponseUserGet,
    ResponseUsersGet,
    UserCreate,
    UserUpdate,
)
from use_cases.auth_use_case import AuthUseCase
from use_cases.user_use_case import UserUseCase


class UserController:
    router: APIRouter
    auth_middleware: AuthMiddleware
    user_use_case: UserUseCase

    def __init__(
        self,
        auth_middleware: AuthMiddleware,
        auth_use_case: AuthUseCase,
        user_use_case: UserUseCase,
    ):
        self.auth_middleware = auth_middleware
        self.auth_use_case = auth_use_case
        self.user_use_case = user_use_case
        self.router = APIRouter(
            dependencies=[Depends(self.auth_middleware.get_user_id)],
            responses=get_error_responses_dict(
                status.HTTP_401_UNAUTHORIZED,
            ),
        )
        self.router.add_api_route(
            path="/",
            endpoint=self.get_users,
            response_model=ResponseUsersGet,
            status_code=status.HTTP_200_OK,
            methods=["GET"],
        )
        self.router.add_api_route(
            path="/me",
            endpoint=self.get_me,
            response_model=ResponseUserDetailGet,
            status_code=status.HTTP_200_OK,
            responses=get_error_responses_dict(
                status.HTTP_404_NOT_FOUND,
            ),
            methods=["GET"],
        )
        self.router.add_api_route(
            path="/{id}",
            endpoint=self.get_user,
            response_model=ResponseUserGet,
            status_code=status.HTTP_200_OK,
            responses=get_error_responses_dict(
                status.HTTP_404_NOT_FOUND,
            ),
            methods=["GET"],
        )
        admin_router = APIRouter(
            dependencies=[Depends(self.auth_use_case.check_admin)],
        )
        admin_router.add_api_route(
            path="/",
            endpoint=self.create_user,
            response_model=ResponseUserGet,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )
        admin_router.add_api_route(
            path="/{id}",
            endpoint=self.update_user,
            response_model=ResponseUserGet,
            status_code=status.HTTP_200_OK,
            methods=["PATCH"],
        )
        admin_router.add_api_route(
            path="/{id}",
            endpoint=self.delete_user,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["DELETE"],
        )
        self.router.include_router(admin_router)
        pass

    async def create_user(self, user_data: UserCreate):
        try:
            created_user = await self.user_use_case.create_and_get_user(user_data)
        except NotAdminError as ex:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(ex),
            )
        return ResponseUserGet(result=created_user)

    async def get_users(self):
        result = await self.user_use_case.get_users()
        return ResponseUsersGet(result=result)

    async def get_me(self, request: AuthedRequest):
        current_user_id = request.state.user_id
        try:
            result = await self.user_use_case.get_user(id=current_user_id)
            return ResponseUserDetailGet(result=result)
        except UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )

    async def get_user(self, id: UUID):
        try:
            result = await self.user_use_case.get_user(id=id)
            return ResponseUserGet(result=result)
        except UserNotFoundError as ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ex),
            )

    async def update_user(self, id: UUID, user_data: UserUpdate):
        try:
            updated_user = await self.user_use_case.update_and_get_user(id, user_data)
        except NotAdminError as ex:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(ex),
            )
        return ResponseUserGet(result=updated_user)

    async def delete_user(self, id: UUID):
        try:
            await self.user_use_case.delete_user(id)
        except NotAdminError as ex:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(ex),
            )
        pass
