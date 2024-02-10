from os.path import abspath, dirname
from sys import path

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":
    path.append(dirname(abspath(__file__)) + '/../')
    from core.config import DatabaseSettings, SettingsLoader
    from models.user import User
    from service.password_service import PasswordService

    SettingsLoader.load_env()
    db_settings = DatabaseSettings()
    connection_url = URL.create(
        drivername="postgresql",
        username=db_settings.DB_USER,
        password=db_settings.DB_PASS,
        host=db_settings.DB_HOST,
        port=db_settings.DB_PORT,
        database=db_settings.DB_NAME,
    )
    engine = create_engine(url=connection_url, isolation_level="AUTOCOMMIT")
    session_maker = sessionmaker(bind=engine)

    password_service = PasswordService()
    admin_user = User(
        email="admin@example.com",
        hashed_password=password_service.hash("password"),
        name="Administrator",
        is_admin=True,
    )

    with session_maker() as session:
        session.add(admin_user)
        pass
    pass
