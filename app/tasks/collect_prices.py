import asyncio
import time

from sqlalchemy import select

from app.core.logger import logger

from app.database.session import async_session_factory

from app.database.models.product import Product

from app.services.price_collector_service import (
    PriceCollectorService
)

from app.monitoring.metrics import (
    scheduler_runs_total,
    scheduler_duration_seconds,
    scheduler_errors_total,
    active_background_tasks
)


# Ограничение параллельных парсеров
MAX_CONCURRENT_TASKS = 5

semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)


async def process_product(product, db):

    async with semaphore:

        service = PriceCollectorService(db)

        await service.collect_product(product)


async def collect_prices_task() -> None:
    """
    Scheduled job:
    Collect prices for all tracked products.
    """

    scheduler_runs_total.inc()

    active_background_tasks.inc()

    start_time = time.perf_counter()

    logger.info(
        "=============================="
    )
    logger.info(
        "PRICE COLLECTION STARTED"
    )
    logger.info(
        "=============================="
    )

    try:

        async with async_session_factory() as db:

            result = await db.execute(
                select(Product)
            )

            products = result.scalars().all()

            logger.info(
                f"Loaded products: {len(products)}"
            )

            tasks = [
                process_product(product, db)
                for product in products
            ]

            await asyncio.gather(
                *tasks,
                return_exceptions=True
            )

        duration = time.perf_counter() - start_time

        scheduler_duration_seconds.observe(
            duration
        )

        logger.info(
            f"PRICE COLLECTION FINISHED "
            f"in {duration:.2f}s"
        )

    except Exception as exc:

        scheduler_errors_total.inc()

        logger.exception(
            f"Scheduler task failed: {exc}"
        )

    finally:

        active_background_tasks.dec()