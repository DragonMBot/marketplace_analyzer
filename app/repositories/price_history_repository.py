from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.database.models.price_history import (
    PriceHistory
)


class PriceHistoryRepository:

    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    async def create(
        self,
        product_id: int,
        price: float,
        old_price: float | None
    ):

        history = PriceHistory(
            product_id=product_id,
            price=price,
            old_price=old_price
        )

        self.db.add(
            history
        )

        await self.db.commit()

        return history