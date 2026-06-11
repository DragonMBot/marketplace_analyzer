from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Text,
    Boolean
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database.base import Base


class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    marketplace_id: Mapped[int] = mapped_column(
        ForeignKey("marketplaces.id"),
        index=True
    )

    external_id: Mapped[str] = mapped_column(
        String(255),
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(1000)
    )

    url: Mapped[str] = mapped_column(
        String(2000),
        unique=True
    )

    image_url: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )

    brand: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    category: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    current_price: Mapped[float] = mapped_column(
        Float
    )

    current_old_price: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    rating: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    reviews_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    marketplace = relationship(
        "Marketplace",
        back_populates="products"
    )

    price_history = relationship(
        "PriceHistory",
        back_populates="product",
        cascade="all, delete-orphan"
    )