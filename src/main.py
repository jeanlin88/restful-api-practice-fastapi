import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException, status

from controllers.auth_controller import AuthController
from controllers.user_controller import UserController
from core.config import AppSettings, DatabaseSettings, JWTSettings, SettingsLoader
from core.database import AsyncDatabase
from middleware import register_middlewares
from middleware.auth_middleware import AuthMiddleware
from middleware.exceptions import custom_exception_handler
from models.base import Base
from repositories.user_repo import UserRepository
from schemas.response import ResponseFail, ResponseSuccess
from service.token_service import TokenService
from use_cases.auth_use_case import AuthUseCase
from use_cases.user_use_case import UserUseCase


@asynccontextmanager
async def lifespan(app: FastAPI):
    # settings
    SettingsLoader.load_env()
    app_settings = AppSettings()
    db_settings = DatabaseSettings()
    jwt_settings = JWTSettings()

    # app
    app.title = app_settings.TITLE
    app.version = app_settings.VERSION

    # logging
    if app_settings.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
        pass

    # database
    async_db = AsyncDatabase(settings=db_settings)
    async with async_db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        pass

    # repositories
    user_repo = UserRepository(db=async_db)

    # services
    token_service = TokenService(settings=jwt_settings)

    # use cases
    auth_use_case = AuthUseCase(
        user_repo=user_repo,
        token_service=token_service,
    )
    user_use_case = UserUseCase(user_repo=user_repo)

    # middlewares
    auth_middleware = AuthMiddleware(token_service=token_service)

    # controllers
    auth_controller = AuthController(auth_use_case=auth_use_case)
    user_controller = UserController(
        auth_middleware=auth_middleware,
        auth_use_case=auth_use_case,
        user_use_case=user_use_case,
    )

    # routers
    api_router = APIRouter(
        responses={
            status.HTTP_200_OK: {"model": ResponseSuccess},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseFail},
        }
    )
    api_router.include_router(
        router=auth_controller.router,
        prefix="/auth",
        tags=["Auth"],
    )
    api_router.include_router(
        router=user_controller.router,
        prefix="/user",
        tags=["User"]
    )

    app.include_router(api_router, prefix="/api")

    yield

    await async_db.clean_up()
    pass

app = FastAPI(lifespan=lifespan)
app.add_exception_handler(HTTPException, custom_exception_handler)
register_middlewares(app=app)
