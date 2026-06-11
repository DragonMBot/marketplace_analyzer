import redis.asyncio as redis

from app.core.logger import logger


class RedisManager:
    """
    Central Redis connection manager.
    """

    def __init__(self, url: str):

        self.url = url
        self.redis: redis.Redis | None = None

    # ============================================================
    # CONNECTION LIFECYCLE
    # ============================================================

    async def connect(self) -> None:
        """
        Create Redis connection.
        """

        try:

            self.redis = redis.from_url(
                self.url,
                encoding="utf-8",
                decode_responses=True
            )

            # health check
            await self.redis.ping()

            logger.info(
                "Redis connection established"
            )

        except Exception as exc:

            logger.exception(
                f"Redis connection failed: {exc}"
            )

            raise

    async def disconnect(self) -> None:
        """
        Close Redis connection.
        """

        try:

            if self.redis:
                await self.redis.close()

                logger.info(
                    "Redis connection closed"
                )

        except Exception as exc:

            logger.exception(
                f"Redis disconnect error: {exc}"
            )

    # ============================================================
    # BASIC OPERATIONS
    # ============================================================

    async def get(self, key: str):

        try:
            return await self.redis.get(key)

        except Exception as exc:

            logger.exception(
                f"Redis GET error: {key} -> {exc}"
            )

            return None

    async def set(
        self,
        key: str,
        value: str,
        ttl: int | None = None
    ) -> bool:

        try:

            return await self.redis.set(
                key,
                value,
                ex=ttl
            )

        except Exception as exc:

            logger.exception(
                f"Redis SET error: {key} -> {exc}"
            )

            return False

    async def delete(self, key: str) -> None:

        try:
            await self.redis.delete(key)

        except Exception as exc:

            logger.exception(
                f"Redis DELETE error: {key} -> {exc}"
            )

    # ============================================================
    # LOCKS (USED IN PARSERS)
    # ============================================================

    async def acquire_lock(
        self,
        key: str,
        ttl: int = 120
    ) -> bool:
        """
        Distributed lock using SET NX EX.
        """

        try:

            result = await self.redis.set(
                key,
                "1",
                nx=True,
                ex=ttl
            )

            return bool(result)

        except Exception as exc:

            logger.exception(
                f"Redis LOCK acquire failed: {key} -> {exc}"
            )

            return False

    async def release_lock(self, key: str) -> None:

        try:
            await self.redis.delete(key)

        except Exception as exc:

            logger.exception(
                f"Redis LOCK release failed: {key} -> {exc}"
            )


# ============================================================
# GLOBAL SINGLETON
# ============================================================

from app.core.config import settings

redis_manager = RedisManager(
    url=settings.REDIS_URL
)