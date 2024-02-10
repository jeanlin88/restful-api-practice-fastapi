from uuid import UUID

from sqlalchemy import Boolean, LargeBinary, String, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class User(Base):
    __tablename__ = "app_user"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=False),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    email: Mapped[str] = mapped_column(String(128))
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary(256))
    name: Mapped[str] = mapped_column(String(32))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    pass
