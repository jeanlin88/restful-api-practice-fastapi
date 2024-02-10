import time
from json import loads

import jwt

from core.config import JWTSettings
from schemas.auth import TokenPayload


class TokenService:
    algorithm: str
    secret: str
    expiration_seconds: int

    def __init__(self, settings: JWTSettings):
        self.algorithm = settings.JWT_ALGORITHM
        self.secret = settings.JWT_SECRET
        self.expiration_seconds = settings.JWT_EXP_MINUTE * 60
        pass

    def encode(self, user_id: str, is_admin: bool) -> str:
        exipration_timestamp = int(time.time()) + self.expiration_seconds
        payload = TokenPayload(
            userID=user_id,
            isAdmin=is_admin,
            exp=exipration_timestamp,
        )
        payload_dict = loads(payload.model_dump_json(by_alias=True))
        token = jwt.encode(payload=payload_dict, key=self.secret)
        return token

    def decode(self, token: str) -> TokenPayload:
        payload_dict = jwt.decode(
            jwt=token, key=self.secret, algorithms=self.algorithm,
        )
        payload = TokenPayload(**payload_dict)
        return payload
    pass
