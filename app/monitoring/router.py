import os

from fastapi import APIRouter, Response

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    multiprocess,
    generate_latest
)

from app.core.logger import logger


router = APIRouter()


@router.get("/metrics", include_in_schema=False)
async def metrics():

    try:

        registry = CollectorRegistry()

        multiprocess.MultiProcessCollector(
            registry
        )

        data = generate_latest(registry)

        return Response(
            content=data,
            media_type=CONTENT_TYPE_LATEST
        )

    except Exception as exc:

        logger.exception(
            f"Metrics generation failed: {exc}"
        )

        return Response(
            content="# metrics error\n",
            media_type="text/plain",
            status_code=500
        )