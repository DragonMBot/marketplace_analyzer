import time
from typing import Callable

from starlette.middleware.base import (
    BaseHTTPMiddleware
)

from starlette.requests import Request
from starlette.responses import Response

from app.monitoring.metrics import (
    http_requests_total,
    http_request_duration_seconds,
    active_http_requests
)

from app.core.logger import logger


class PrometheusMiddleware(BaseHTTPMiddleware):
    """
    Middleware for Prometheus HTTP metrics.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:

        method = request.method
        endpoint = request.url.path

        start_time = time.perf_counter()

        active_http_requests.inc()

        response = None

        try:

            response = await call_next(request)

            return response

        except Exception as exc:

            logger.exception(
                f"HTTP middleware error: {exc}"
            )

            raise

        finally:

            duration = (
                time.perf_counter() - start_time
            )

            status_code = (
                response.status_code
                if response is not None
                else 500
            )

            # ====================================================
            # Prometheus metrics
            # ====================================================

            http_requests_total.labels(
                method=method,
                endpoint=endpoint,
                status=status_code
            ).inc()

            http_request_duration_seconds.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)

            active_http_requests.dec()

            # ====================================================
            # Logging
            # ====================================================

            logger.debug(
                f"{method} {endpoint} "
                f"-> {status_code} "
                f"in {duration:.4f}s"
            )