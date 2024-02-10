from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class SettingsLoader:
    @staticmethod
    def load_env():
        load_dotenv()
        pass
    pass


class AppSettings(BaseSettings):
    TITLE: str
    VERSION: str
    DEBUG: bool
    pass


class DatabaseSettings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    pass


class JWTSettings(BaseSettings):
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET: str
    JWT_EXP_MINUTE: int = 60
    pass
