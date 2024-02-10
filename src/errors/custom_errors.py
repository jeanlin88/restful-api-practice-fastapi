class BaseError(Exception):
    default_message: str = "this is a default message"

    def __init__(self):
        super().__init__(self.default_message)
        pass
    pass


class UserNotFoundError(BaseError):
    default_message = "user not found"
    pass


class IncorrectPassword(BaseError):
    pass


class NotAdminError(BaseError):
    default_message = "user is not admin"
    pass
