from sqlalchemy import UUID, delete, select, update

from core.database import AsyncDatabase
from models.user import User


class UserRepository:
    db: AsyncDatabase

    def __init__(self, db: AsyncDatabase):
        self.db = db
        pass

    async def create_user(self, data: User) -> UUID:
        async with self.db.session_maker() as session:
            session.add(data)
            await session.commit()
            pass
        return data.id

    async def get_users(self) -> list[User]:
        stmt = select(User)
        async with self.db.session_maker() as session:
            users = await session.scalars(stmt)
            pass
        return users

    async def get_user(self, id: UUID) -> User | None:
        async with self.db.session_maker() as session:
            user = await session.get(User, id)
            pass
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        async with self.db.session_maker() as session:
            user = await session.scalar(stmt)
            pass
        return user

    async def update_user(self, id: UUID, data: dict) -> None:
        stmt = (
            update(User)
            .where(User.id == id)
            .values(**data)
        )
        async with self.db.session_maker() as session:
            await session.execute(stmt)
            pass
        return None

    async def delete_user(self, id: UUID) -> None:
        stmt = delete(User).where(User.id == id)
        async with self.db.session_maker() as session:
            await session.execute(stmt)
            pass
        return None
    pass
