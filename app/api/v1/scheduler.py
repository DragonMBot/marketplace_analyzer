from fastapi import APIRouter

from app.tasks.collect_prices import (
    collect_prices_task
)

router = APIRouter(
    prefix="/scheduler",
    tags=["Scheduler"]
)


@router.post(
    "/collect-prices"
)
async def collect_prices():

    await collect_prices_task()

    return {
        "status": "ok"
    }