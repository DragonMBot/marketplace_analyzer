from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Index
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database.base import Base


class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        index=True
    )

    token_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    expires_at: Mapped[datetime]

    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    user = relationship(
        "User"
    )

    __table_args__ = (
        Index(
            "idx_refresh_user",
            "user_id"
        ),
    )
