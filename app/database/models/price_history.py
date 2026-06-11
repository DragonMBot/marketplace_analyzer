from datetime import datetime

from sqlalchemy import (
    Float,
    Integer,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database.base import Base


class PriceHistory(Base):

    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        index=True
    )

    price: Mapped[float] = mapped_column(
        Float
    )

    old_price: Mapped[float | None] = mapped_column(
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

    collected_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    product = relationship(
        "Product",
        back_populates="price_history"
    )
