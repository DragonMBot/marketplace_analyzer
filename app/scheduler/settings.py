from dataclasses import dataclass


@dataclass(slots=True)
class SchedulerSettings:

    PRICE_UPDATE_INTERVAL_MINUTES: int = 30

    MAX_CONCURRENT_PARSERS: int = 5

    JOB_MISFIRE_GRACE_TIME: int = 300

    JOB_MAX_INSTANCES: int = 1


scheduler_settings = SchedulerSettings()