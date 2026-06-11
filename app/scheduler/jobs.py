from apscheduler.triggers.interval import (
    IntervalTrigger
)

from app.tasks.collect_prices import (
    collect_prices_task
)

from app.scheduler.settings import (
    scheduler_settings
)


def register_jobs(
    scheduler
):

    scheduler.add_job(
        func=collect_prices_task,
        trigger=IntervalTrigger(
            minutes=(
                scheduler_settings
                .PRICE_UPDATE_INTERVAL_MINUTES
            )
        ),
        id="collect_prices",
        name="Collect product prices",
        replace_existing=True,
        max_instances=(
            scheduler_settings
            .JOB_MAX_INSTANCES
        ),
        coalesce=True,
        misfire_grace_time=(
            scheduler_settings
            .JOB_MISFIRE_GRACE_TIME
        )
    )