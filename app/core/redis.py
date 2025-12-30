from redis.asyncio import Redis

redis: Redis | None = None

async def init_redis():
    global redis
    redis = Redis.from_url(
        "redis://localhost:6379/0",
        decode_responses=True
    )

async def close_redis():
    if redis:
        await redis.close()
