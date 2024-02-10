from pydantic import BaseModel, ConfigDict, EmailStr

from schemas.response import ResponseSuccess


class UserBase(BaseModel):
    name: str
    pass


class UserCreate(UserBase):
    email: EmailStr
    password: str
    pass


class UserGet(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    is_admin: bool
    pass


class UserDetailGet(UserGet):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    pass


class UserUpdate(UserBase):
    email: EmailStr = None
    password: str = None
    name: str = None
    pass


class ResponseUserGet(ResponseSuccess):
    result: UserGet
    pass


class ResponseUserDetailGet(ResponseSuccess):
    result: UserDetailGet
    pass


class ResponseUsersGet(ResponseSuccess):
    result: list[UserGet]
    pass
