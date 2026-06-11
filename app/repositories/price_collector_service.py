from app.core.logger import logger

from app.services.parser_service import (
    ParserService
)

from app.repositories.price_history_repository import (
    PriceHistoryRepository
)


class PriceCollectorService:

    def __init__(
        self,
        db
    ):
        self.db = db

    async def collect_product(
        self,
        product
    ):

        logger.info(
            f"Collecting prices: {product.id}"
        )

        parser_service = (
            ParserService()
        )

        result = (
            await parser_service.parse_product(
                product.marketplace.name.lower(),
                product.external_id
            )
        )

        if not result.current_price:
            return

        product.current_price = (
            result.current_price
        )

        await self.db.commit()

        repo = (
            PriceHistoryRepository(
                self.db
            )
        )

        await repo.create(
            product.id,
            result.current_price,
            result.old_price
        )

        logger.info(
            f"Price updated "
            f"{product.id} -> "
            f"{result.current_price}"
        )