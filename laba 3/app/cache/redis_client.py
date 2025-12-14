import os
from typing import Optional

try:
    import redis.asyncio as redis
except Exception:  # pragma: no cover - redis may not be installed in test env
    redis = None

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def get_redis() -> Optional["redis.Redis"]:
    if redis is None:
        return None
    return redis.from_url(REDIS_URL)
