# archivo: utils/cache.py
import asyncio
import time
from typing import Any, Dict, Optional
import redis.asyncio as redis
from config import settings


class InMemoryTTLCache:
    def __init__(self):
        self._store: Dict[str, tuple[Any, float]] = {}

    async def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None
        value, expires_at = self._store[key]
        if time.time() > expires_at:
            del self._store[key]
            return None
        return value

    async def set(self, key: str, value: Any, ttl: int):
        self._store[key] = (value, time.time() + ttl)


class Cache:
    def __init__(self):
        self.redis = None
        self.memory = InMemoryTTLCache()

    async def init(self):
        if settings.REDIS_URL:
            self.redis = redis.from_url(settings.REDIS_URL)

    async def get(self, key: str) -> Optional[Any]:
        if self.redis:
            value = await self.redis.get(key)
            return value
        return await self.memory.get(key)

    async def set(self, key: str, value: Any, ttl: int):
        if self.redis:
            await self.redis.set(key, value, ex=ttl)
        else:
            await self.memory.set(key, value, ttl)


cache = Cache()
