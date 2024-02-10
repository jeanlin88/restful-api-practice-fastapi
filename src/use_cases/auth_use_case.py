from errors.custom_errors import NotAdminError, UserNotFoundError
from repositories.user_repo import UserRepository
from schemas.auth import Login, LoginSuccess
from schemas.request import AuthedRequest
from service.password_service import PasswordService
from service.token_service import TokenService


class AuthUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        token_service: TokenService,
    ):
        self.user_repo = user_repo
        self.token_service = token_service
        pass

    async def login(self, login_data: Login) -> LoginSuccess:
        orm_user = await self.user_repo.get_user_by_email(email=login_data.email)
        if orm_user is None:
            raise UserNotFoundError
        PasswordService.verify(login_data.password, orm_user.hashed_password)
        token = self.token_service.encode(
            user_id=orm_user.id,
            is_admin=orm_user.is_admin,
        )
        return LoginSuccess(token=token)

    async def check_admin(self, request: AuthedRequest) -> None:
        current_user_id = request.state.user_id
        orm_user = await self.user_repo.get_user(current_user_id)
        if not orm_user.is_admin:
            raise NotAdminError
        pass
    pass
