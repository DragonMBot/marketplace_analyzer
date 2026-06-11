from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger

from app.cache.keys import CacheKeys
from app.cache.redis import redis_manager

from app.monitoring.metrics import (
    products_processed_total,
    products_failed_total,
    product_price_updates_total,
    price_history_records_total,
    increment_parser_run,
    increment_parser_error
)

from app.repositories.price_history_repository import (
    PriceHistoryRepository
)

from app.services.parser_service import ParserService


class PriceCollectorService:

    def __init__(self, db: AsyncSession):

        self.db = db

    async def collect_product(self, product) -> None:

        lock_key = CacheKeys.parser_lock(product.id)

        locked = await redis_manager.acquire_lock(
            lock_key,
            ttl=120
        )

        if not locked:

            logger.info(
                f"[LOCK SKIP] Product {product.id}"
            )

            return

        logger.info(
            f"[LOCK ACQUIRED] Product {product.id}"
        )

        try:

            # ====================================================
            # PARSING
            # ====================================================

            increment_parser_run(
                product.marketplace.name.lower()
            )

            parser = ParserService()

            result = await parser.parse_product(
                marketplace=product.marketplace.name.lower(),
                external_id=product.external_id
            )

            if not result:

                logger.warning(
                    f"No parser result: {product.id}"
                )

                products_failed_total.inc()
                increment_parser_error(
                    product.marketplace.name.lower()
                )

                return

            if result.current_price is None:

                logger.warning(
                    f"No price found: {product.id}"
                )

                products_failed_total.inc()

                return

            # ====================================================
            # PRICE UPDATE
            # ====================================================

            old_price = product.current_price

            product.current_price = result.current_price

            if result.old_price is not None:

                product.old_price = result.old_price

            await self.db.commit()

            product_price_updates_total.inc()

            logger.info(
                f"[PRICE UPDATED] "
                f"Product={product.id} "
                f"Price={result.current_price}"
            )

            # ====================================================
            # PRICE HISTORY
            # ====================================================

            history_repo = PriceHistoryRepository(self.db)

            await history_repo.create(
                product_id=product.id,
                price=result.current_price,
                old_price=old_price
            )

            price_history_records_total.inc()

            # ====================================================
            # SUCCESS METRICS
            # ====================================================

            products_processed_total.inc()

        except Exception as exc:

            await self.db.rollback()

            products_failed_total.inc()

            increment_parser_error(
                product.marketplace.name.lower()
            )

            logger.exception(
                f"[ERROR] Product {product.id}: {exc}"
            )

            raise

        finally:

            await redis_manager.release_lock(lock_key)

            logger.info(
                f"[LOCK RELEASED] Product {product.id}"
            )