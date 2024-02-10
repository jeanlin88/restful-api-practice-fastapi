from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from schemas.response import ResponseSuccess


class Login(BaseModel):
    email: EmailStr
    password: str
    pass


class TokenPayload(BaseModel):
    user_id: UUID = Field(alias="userID")
    is_admin: bool = Field(alias="isAdmin")
    expires_at: int = Field(alias="exp")
    pass


class LoginSuccess(BaseModel):
    token: str
    pass


class ResponseLoginSuccess(ResponseSuccess):
    result: LoginSuccess
    pass
