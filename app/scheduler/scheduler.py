from apscheduler.schedulers.asyncio import (
    AsyncIOScheduler
)

from apscheduler.triggers.interval import (
    IntervalTrigger
)

from app.core.logger import logger

from app.tasks.collect_prices import (
    collect_prices_task
)


scheduler = AsyncIOScheduler(
    timezone="UTC"
)


def start_scheduler() -> None:

    logger.info(
        "Starting APScheduler..."
    )

    scheduler.add_job(
        func=collect_prices_task,
        trigger=IntervalTrigger(
            minutes=30
        ),
        id="collect_prices",
        name="Collect product prices",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=300
    )

    scheduler.start()

    logger.info(
        "APScheduler started"
    )


def stop_scheduler() -> None:

    logger.info(
        "Stopping APScheduler..."
    )

    scheduler.shutdown(
        wait=False
    )

    logger.info(
        "APScheduler stopped"
    )
from apscheduler.schedulers.asyncio import (
    AsyncIOScheduler
)

from app.core.logger import logger

from app.scheduler.jobs import (
    register_jobs
)


class SchedulerManager:

    def __init__(self):

        self.scheduler = (
            AsyncIOScheduler(
                timezone="UTC"
            )
        )

    def start(self):

        register_jobs(
            self.scheduler
        )

        self.scheduler.start()

        logger.info(
            "Scheduler started"
        )

        for job in self.scheduler.get_jobs():

            logger.info(
                f"Registered job: "
                f"{job.id}"
            )

    def stop(self):

        self.scheduler.shutdown(
            wait=False
        )

        logger.info(
            "Scheduler stopped"
        )


scheduler_manager = (
    SchedulerManager()
)