import json
from uuid import UUID

from errors.custom_errors import UserNotFoundError
from models.user import User
from repositories.user_repo import UserRepository
from schemas.user import UserCreate, UserDetailGet, UserGet, UserUpdate
from service.password_service import PasswordService


class UserUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
    ):
        self.user_repo = user_repo
        pass

    async def create_and_get_user(self, user_data: UserCreate) -> UserGet:
        hashed_password = PasswordService.hash(user_data.password)
        user_dict = json.loads(
            user_data.model_dump_json(
                by_alias=True,
                exclude=['password'],
            )
        ) | {"hashed_password": hashed_password}
        user_model = User(**user_dict)
        user_id = await self.user_repo.create_user(user_model)
        orm_user = await self.user_repo.get_user(id=user_id)
        if orm_user is None:
            raise UserNotFoundError
        return UserGet.model_validate(orm_user)

    async def get_users(self) -> list[UserGet]:
        orm_users = await self.user_repo.get_users()
        return [UserGet.model_validate(orm_user) for orm_user in orm_users]

    async def get_user(self, id: UUID) -> UserDetailGet:
        orm_user = await self.user_repo.get_user(id)
        if orm_user is None:
            raise UserNotFoundError
        return UserDetailGet.model_validate(orm_user)

    async def update_and_get_user(self, id: UUID, user_data: UserUpdate) -> None:
        user_dict = json.loads(
            user_data.model_dump_json(
                by_alias=True,
                exclude=["password"],
                exclude_unset=True,
            ),
        )
        if user_data.password is not None:
            hashed_password = PasswordService.hash(user_data.password)
            user_dict |= {
                "hashed_password": hashed_password,
            }
            pass
        await self.user_repo.update_user(id=id, data=user_dict)
        orm_user = await self.user_repo.get_user(id=id)
        if orm_user is None:
            raise UserNotFoundError
        return UserGet.model_validate(orm_user)

    async def delete_user(self, id: UUID) -> None:
        await self.user_repo.delete_user(id=id)
        return None
    pass
