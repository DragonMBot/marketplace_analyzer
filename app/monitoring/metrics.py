from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    Summary
)

# ============================================================
# HTTP
# ============================================================

http_requests_total = Counter(
    name="http_requests_total",
    documentation="Total HTTP requests",
    labelnames=[
        "method",
        "endpoint",
        "status"
    ]
)

http_request_duration_seconds = Histogram(
    name="http_request_duration_seconds",
    documentation="HTTP request duration",
    labelnames=[
        "method",
        "endpoint"
    ],
    buckets=(
        0.005,
        0.01,
        0.025,
        0.05,
        0.1,
        0.25,
        0.5,
        1.0,
        2.5,
        5.0,
        10.0
    )
)

active_http_requests = Gauge(
    name="active_http_requests",
    documentation="Current active HTTP requests"
)

# ============================================================
# AUTH
# ============================================================

user_logins_total = Counter(
    name="user_logins_total",
    documentation="Successful user logins"
)

user_login_failed_total = Counter(
    name="user_login_failed_total",
    documentation="Failed login attempts"
)

jwt_tokens_created_total = Counter(
    name="jwt_tokens_created_total",
    documentation="Created JWT tokens",
    labelnames=["token_type"]
)

jwt_tokens_revoked_total = Counter(
    name="jwt_tokens_revoked_total",
    documentation="Revoked JWT tokens"
)

# ============================================================
# PARSERS
# ============================================================

parser_runs_total = Counter(
    name="parser_runs_total",
    documentation="Total parser executions",
    labelnames=["marketplace"]
)

parser_errors_total = Counter(
    name="parser_errors_total",
    documentation="Total parser errors",
    labelnames=["marketplace"]
)

parser_duration_seconds = Histogram(
    name="parser_duration_seconds",
    documentation="Parser execution duration",
    labelnames=["marketplace"],
    buckets=(
        0.1,
        0.5,
        1.0,
        2.0,
        5.0,
        10.0,
        20.0,
        30.0,
        60.0
    )
)

active_parsers = Gauge(
    name="active_parsers",
    documentation="Currently active parsers"
)

# ============================================================
# PRODUCTS
# ============================================================

products_processed_total = Counter(
    name="products_processed_total",
    documentation="Successfully processed products"
)

products_failed_total = Counter(
    name="products_failed_total",
    documentation="Failed products processing"
)

product_price_updates_total = Counter(
    name="product_price_updates_total",
    documentation="Product price updates"
)

tracked_products_total = Gauge(
    name="tracked_products_total",
    documentation="Currently tracked products"
)

# ============================================================
# PRICE HISTORY
# ============================================================

price_history_records_total = Counter(
    name="price_history_records_total",
    documentation="Price history records created"
)

# ============================================================
# SCHEDULER
# ============================================================

scheduler_runs_total = Counter(
    name="scheduler_runs_total",
    documentation="Scheduler executions"
)

scheduler_errors_total = Counter(
    name="scheduler_errors_total",
    documentation="Scheduler execution errors"
)

scheduler_duration_seconds = Histogram(
    name="scheduler_duration_seconds",
    documentation="Scheduler execution duration",
    buckets=(
        1,
        5,
        10,
        30,
        60,
        120,
        300,
        600
    )
)

# ============================================================
# DATABASE
# ============================================================

database_queries_total = Counter(
    name="database_queries_total",
    documentation="Database queries executed"
)

database_errors_total = Counter(
    name="database_errors_total",
    documentation="Database errors"
)

database_commit_total = Counter(
    name="database_commit_total",
    documentation="Database commits"
)

database_rollback_total = Counter(
    name="database_rollback_total",
    documentation="Database rollbacks"
)

database_query_duration_seconds = Histogram(
    name="database_query_duration_seconds",
    documentation="Database query duration",
    buckets=(
        0.001,
        0.005,
        0.01,
        0.05,
        0.1,
        0.5,
        1.0,
        2.0
    )
)

# ============================================================
# REDIS
# ============================================================

redis_cache_hits_total = Counter(
    name="redis_cache_hits_total",
    documentation="Redis cache hits"
)

redis_cache_misses_total = Counter(
    name="redis_cache_misses_total",
    documentation="Redis cache misses"
)

redis_operations_total = Counter(
    name="redis_operations_total",
    documentation="Redis operations",
    labelnames=["operation"]
)

redis_errors_total = Counter(
    name="redis_errors_total",
    documentation="Redis operation errors"
)

active_redis_locks = Gauge(
    name="active_redis_locks",
    documentation="Current active Redis locks"
)

# ============================================================
# PLAYWRIGHT
# ============================================================

playwright_browser_launch_total = Counter(
    name="playwright_browser_launch_total",
    documentation="Playwright browser launches"
)

playwright_browser_errors_total = Counter(
    name="playwright_browser_errors_total",
    documentation="Playwright browser errors"
)

playwright_page_load_seconds = Histogram(
    name="playwright_page_load_seconds",
    documentation="Page load duration",
    labelnames=["marketplace"],
    buckets=(
        0.5,
        1,
        2,
        3,
        5,
        10,
        20,
        30
    )
)

# ============================================================
# BACKGROUND TASKS
# ============================================================

background_tasks_total = Counter(
    name="background_tasks_total",
    documentation="Background tasks executed",
    labelnames=["task"]
)

background_tasks_errors_total = Counter(
    name="background_tasks_errors_total",
    documentation="Background task errors",
    labelnames=["task"]
)

active_background_tasks = Gauge(
    name="active_background_tasks",
    documentation="Currently running background tasks"
)

# ============================================================
# SYSTEM
# ============================================================

application_uptime_seconds = Gauge(
    name="application_uptime_seconds",
    documentation="Application uptime"
)

application_startups_total = Counter(
    name="application_startups_total",
    documentation="Application startups"
)

application_shutdowns_total = Counter(
    name="application_shutdowns_total",
    documentation="Application shutdowns"
)

# ============================================================
# CUSTOM BUSINESS METRICS
# ============================================================

marketplace_products_total = Gauge(
    name="marketplace_products_total",
    documentation="Products by marketplace",
    labelnames=["marketplace"]
)

marketplace_price_changes_total = Counter(
    name="marketplace_price_changes_total",
    documentation="Price changes by marketplace",
    labelnames=["marketplace"]
)

price_drop_events_total = Counter(
    name="price_drop_events_total",
    documentation="Detected price drops"
)

price_increase_events_total = Counter(
    name="price_increase_events_total",
    documentation="Detected price increases"
)

# ============================================================
# HELPERS
# ============================================================

def increment_parser_run(
    marketplace: str
) -> None:
    parser_runs_total.labels(
        marketplace=marketplace
    ).inc()


def increment_parser_error(
    marketplace: str
) -> None:
    parser_errors_total.labels(
        marketplace=marketplace
    ).inc()


def observe_parser_duration(
    marketplace: str,
    duration: float
) -> None:
    parser_duration_seconds.labels(
        marketplace=marketplace
    ).observe(duration)


def increment_scheduler_run() -> None:
    scheduler_runs_total.inc()


def increment_product_processed() -> None:
    products_processed_total.inc()


def increment_product_failed() -> None:
    products_failed_total.inc()


def increment_price_update() -> None:
    product_price_updates_total.inc()


def increment_cache_hit() -> None:
    redis_cache_hits_total.inc()


def increment_cache_miss() -> None:
    redis_cache_misses_total.inc()