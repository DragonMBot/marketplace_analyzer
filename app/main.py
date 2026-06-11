from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.openapi.utils import get_openapi
from app.core.config import settings
from app.core.logger import logger

from app.cache.redis import redis_manager

from app.scheduler.scheduler import (
    scheduler_manager
)

from app.monitoring.router import (
    router as metrics_router
)

from app.monitoring.middleware import (
    PrometheusMiddleware
)

# API Routers
from app.api.v1.auth import (
    router as auth_router
)

from app.api.v1.health import (
    router as health_router
)

from app.api.v1.scheduler import (
    router as scheduler_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle.
    """

    logger.info(
        "========================================"
    )
    logger.info(
        "Starting Price Analyzer Backend..."
    )
    logger.info(
        "========================================"
    )

    try:
        # Redis
        await redis_manager.connect()

        logger.info(
            "Redis connected"
        )

        # Scheduler
        scheduler_manager.start()

        logger.info(
            "Scheduler started"
        )

        logger.info(
            "Application startup completed"
        )

        yield

    finally:

        logger.info(
            "Stopping application..."
        )

        try:

            scheduler_manager.stop()

            logger.info(
                "Scheduler stopped"
            )

        except Exception as exc:

            logger.exception(
                f"Scheduler shutdown error: {exc}"
            )

        try:

            await redis_manager.disconnect()

            logger.info(
                "Redis disconnected"
            )

        except Exception as exc:

            logger.exception(
                f"Redis shutdown error: {exc}"
            )

        logger.info(
            "Application shutdown completed"
        )


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ============================================================
# Middleware
# ============================================================

app.add_middleware(
    PrometheusMiddleware
)

# ============================================================
# Exception Handlers
# ============================================================


@app.exception_handler(
    RequestValidationError
)
async def validation_exception_handler(
    request,
    exc
):

    logger.warning(
        f"Validation error: {exc}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors()
        }
    )


@app.exception_handler(
    StarletteHTTPException
)
async def http_exception_handler(
    request,
    exc
):

    logger.warning(
        f"HTTP error: {exc.detail}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail
        }
    )


@app.exception_handler(
    Exception
)
async def global_exception_handler(
    request,
    exc
):

    logger.exception(
        f"Unhandled exception: {exc}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error"
        }
    )

# ============================================================
# Routers
# ============================================================

app.include_router(
    health_router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    auth_router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    scheduler_router,
    prefix=settings.API_V1_PREFIX
)

app.include_router(
    metrics_router
)

# ============================================================
# Root Endpoint
# ============================================================


@app.get(
    "/",
    tags=["Root"]
)
async def root():

    return {
        "project": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "running"
    }


@app.get(
    "/ping",
    tags=["Root"]
)
async def ping():

    return {
        "status": "ok"
    }
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="Price Analyzer API",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path:
            path[method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi