from sqlalchemy import String

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database.base import Base


class Marketplace(Base):

    __tablename__ = "marketplaces"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    domain: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    products = relationship(
        "Product",
        back_populates="marketplace"
    )