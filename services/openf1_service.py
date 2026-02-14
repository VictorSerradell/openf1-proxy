# archivo: services/openf1_service.py
# (VERSIÓN ACTUALIZADA ENTERPRISE)

import httpx
import asyncio
import time
import hashlib
from typing import Any, Dict
from config import settings
from utils.cache import cache
from utils.circuit_breaker import CircuitBreaker
from utils.metrics import REQUEST_COUNTER, REQUEST_LATENCY

breaker = CircuitBreaker()


class OpenF1Service:
    def __init__(self):
        limits = httpx.Limits(
            max_keepalive_connections=20,
            max_connections=100,
        )
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(10.0),
            limits=limits,
        )

    def _generate_etag(self, data: Any) -> str:
        return hashlib.md5(str(data).encode()).hexdigest()

    async def fetch(self, endpoint: str, params: Dict[str, Any], ttl: int):
        cache_key = f"{endpoint}:{str(params)}"
        cached = await cache.get(cache_key)

        if cached:
            return cached

        async def upstream_call():
            with REQUEST_LATENCY.labels(endpoint=endpoint).time():
                response = await self.client.get(
                    f"{settings.OPENF1_BASE_URL}/{endpoint}",
                    params=params,
                )
                response.raise_for_status()
                return response.json()

        try:
            REQUEST_COUNTER.labels(endpoint=endpoint).inc()
            data = await breaker.call(upstream_call)
            await cache.set(cache_key, data, ttl)
            return data

        except Exception:
            if cached:
                return cached
            raise


service = OpenF1Service()
