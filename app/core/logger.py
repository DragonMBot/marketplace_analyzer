from pathlib import Path

from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

logger.add(
    LOG_DIR / "app.log",
    rotation="100 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    level="INFO"
)

logger.add(
    LOG_DIR / "error.log",
    rotation="100 MB",
    retention="90 days",
    compression="zip",
    level="ERROR",
    enqueue=True
)

logger.add(
    sink=lambda msg: print(msg, end=""),
    level="INFO"
)