from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base
from sqlalchemy import Boolean, Column

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


settings = relationship(
    "UserSettings",
    uselist=False,
    back_populates="user"
)
class User(Base):

    __tablename__ = "users"
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String, nullable=False, default="user")

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255)
    )