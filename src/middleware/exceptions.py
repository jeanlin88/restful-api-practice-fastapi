from logging import ERROR, log
from typing import Awaitable, Callable

from fastapi import HTTPException, Request, Response, status
from fastapi.responses import JSONResponse

from schemas.response import ResponseFail


async def custom_exception_handler(_, exc: HTTPException):
    fail_response = ResponseFail(
        status_code=exc.status_code,
        error=exc.detail,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=fail_response.model_dump(),
    )


async def exception_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]],
):
    try:
        response = await call_next(request)
        pass
    except Exception as ex:
        log(ERROR, "auth failed", exc_info=ex)
        fail_response = ResponseFail(error=str(ex))
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=fail_response.model_dump(),
        )
        pass
    return response
