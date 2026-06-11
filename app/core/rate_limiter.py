import time
from fastapi import Request, HTTPException

from app.cache.redis import redis_manager


class RateLimiter:
    """
    Simple Redis-based sliding window rate limiter.
    """

    def __init__(self, limit: int = 60, window: int = 60):
        self.limit = limit
        self.window = window

    async def __call__(self, request: Request):

        ip = request.client.host
        key = f"rate_limit:{ip}"

        now = int(time.time())

        redis = redis_manager.redis

        # current requests count
        current = await redis.get(key)

        if current and int(current) >= self.limit:
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )

        pipe = redis.pipeline()

        pipe.incr(key)
        pipe.expire(key, self.window)

        await pipe.execute()