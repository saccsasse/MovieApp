import json
from typing import Any
from app.core.redis import redis


async def get_cache(key: str) -> Any | None:
    if not redis:
        return None
    try:
        data = await redis.get(key)
        return json.loads(data) if data else None
    except Exception:
        return None


async def set_cache(key:str, value: Any, ttl: int = 60) -> None:
    if not redis:
        return None
    try:
        await redis.set(key, json.dumps(value), ex=ttl)
    except Exception:
        return None


async def delete_cache(key: str) -> None:
    if not redis:
        return None
    try:
        await redis.delete(key)
    except Exception:
        return None
