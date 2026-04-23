"""
Cache Manager — Redis with in-memory fallback.
Provides TTL-based caching for SERP results, graph data, analysis results.
"""
import json
import time
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class InMemoryCache:
    """Simple in-memory TTL cache when Redis is unavailable."""

    def __init__(self):
        self._store: dict = {}

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if time.time() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl: int = 3600):
        self._store[key] = (value, time.time() + ttl)

    def delete(self, key: str):
        self._store.pop(key, None)

    def flush(self):
        self._store.clear()

    def info(self) -> dict:
        now = time.time()
        active = sum(1 for _, (_, exp) in self._store.items() if exp > now)
        return {"type": "in-memory", "active_keys": active, "total_keys": len(self._store)}


class CacheManager:
    """
    Unified cache interface.
    Tries Redis first; falls back to in-memory dict.
    """

    def __init__(self):
        self._redis = None
        self._memory = InMemoryCache()
        self._using_redis = False
        self._initialized = False

    async def initialize(self, redis_url: Optional[str] = None):
        """Attempt to connect to Redis; fall back to memory cache."""
        if redis_url:
            try:
                import redis.asyncio as aioredis
                self._redis = aioredis.from_url(redis_url, decode_responses=True)
                await self._redis.ping()
                self._using_redis = True
                logger.info(f"✓ Redis cache connected: {redis_url}")
            except Exception as e:
                logger.warning(f"Redis unavailable ({e}). Using in-memory cache.")
                self._redis = None
                self._using_redis = False
        else:
            logger.info("Redis URL not configured. Using in-memory cache.")
        self._initialized = True

    async def get(self, key: str) -> Optional[Any]:
        if self._using_redis and self._redis:
            try:
                raw = await self._redis.get(key)
                if raw:
                    return json.loads(raw)
                return None
            except Exception:
                pass
        return self._memory.get(key)

    async def set(self, key: str, value: Any, ttl: int = 3600):
        if self._using_redis and self._redis:
            try:
                await self._redis.setex(key, ttl, json.dumps(value))
                return
            except Exception:
                pass
        self._memory.set(key, value, ttl)

    async def delete(self, key: str):
        if self._using_redis and self._redis:
            try:
                await self._redis.delete(key)
                return
            except Exception:
                pass
        self._memory.delete(key)

    async def flush(self):
        if self._using_redis and self._redis:
            try:
                await self._redis.flushdb()
                return
            except Exception:
                pass
        self._memory.flush()

    async def info(self) -> dict:
        if self._using_redis and self._redis:
            try:
                info = await self._redis.info()
                return {
                    "type": "redis",
                    "connected": True,
                    "used_memory_human": info.get("used_memory_human", "?"),
                    "connected_clients": info.get("connected_clients", 0),
                }
            except Exception:
                pass
        return self._memory.info()

    @property
    def backend(self) -> str:
        return "redis" if self._using_redis else "in-memory"


# Singleton instance
cache_manager = CacheManager()
