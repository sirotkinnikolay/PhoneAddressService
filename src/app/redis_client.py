from typing import Optional
import redis.asyncio as aioredis
import logging

logger = logging.getLogger("redis-client")

redis_client: Optional[aioredis.Redis] = None

async def init_redis_pool(url: str) -> redis_client:
    """
    Инициализирует глобальный Redis-клиент.
    """
    global redis_client
    if redis_client is None:
        logger.info("Connecting to Redis: %s", url)
        redis_client = aioredis.from_url(url, decode_responses=True)
        try:
            await redis_client.ping()
            logger.info("Connected to Redis")
        except Exception as e:
            logger.exception("Failed to ping Redis: %s", e)
            raise
    return redis_client

async def close_redis_pool():
    """
    Закрывает глобальное Redis-подключение.
    """
    global redis_client
    if redis_client:
        try:
            await redis_client.close()
            await redis_client.connection_pool.disconnect()
        except Exception as e:
            logger.exception("Error closing Redis: %s", e)
        finally:
            redis_client = None

def get_redis() -> Optional[aioredis.Redis]:
    """Возвращает текущий redis client (или None)"""
    return redis_client
