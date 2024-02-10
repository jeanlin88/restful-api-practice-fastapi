import bcrypt

from errors.custom_errors import IncorrectPassword


class PasswordService:
    @staticmethod
    def hash(password: str) -> bytes:
        encoded_password = password.encode()
        hashed = bcrypt.hashpw(
            password=encoded_password,
            salt=bcrypt.gensalt(),
        )
        return hashed

    @staticmethod
    def verify(password: str, hashed: bytes):
        encoded_password = password.encode()
        valid = bcrypt.checkpw(
            password=encoded_password,
            hashed_password=hashed,
        )
        if not valid:
            raise IncorrectPassword
        pass
    pass
