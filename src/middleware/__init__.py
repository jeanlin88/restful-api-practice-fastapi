from fastapi import FastAPI

from middleware.exceptions import exception_middleware


def register_middlewares(app: FastAPI):
    app.middleware("http")(exception_middleware)
    pass
