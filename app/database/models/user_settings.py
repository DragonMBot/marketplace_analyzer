from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database.base import Base


class UserSettings(Base):

    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True
    )

    email_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    browser_notifications: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    price_drop_percent: Mapped[int] = mapped_column(
        Integer,
        default=10
    )

    user = relationship(
        "User",
        back_populates="settings"
    )
