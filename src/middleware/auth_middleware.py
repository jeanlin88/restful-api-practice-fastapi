from logging import DEBUG, ERROR, log

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from schemas.request import AuthedRequest
from service.token_service import TokenService

auth_header = APIKeyHeader(name='Authorization', auto_error=False)


class AuthMiddleware:
    token_service: TokenService

    def __init__(self, token_service: TokenService):
        self.token_service = token_service
        pass

    async def get_user_id(
        self,
        request: AuthedRequest,
        token: bytes | None = Security(auth_header),
    ):
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token missing",
            )
        try:
            payload = self.token_service.decode(token)
            request.state.user_id = payload.user_id
            pass
        except Exception as ex:
            log(ERROR, "auth failed", exc_info=ex)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(ex),
            )
        pass
    pass
