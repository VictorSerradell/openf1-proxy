# archivo: utils/circuit_breaker.py
import time
from typing import Callable, Awaitable, Any


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED | OPEN | HALF_OPEN

    async def call(self, func: Callable[..., Awaitable[Any]], *args, **kwargs):
        now = time.time()

        if self.state == "OPEN":
            if now - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker OPEN")

        try:
            result = await func(*args, **kwargs)
            self.failures = 0
            self.state = "CLOSED"
            return result

        except Exception:
            self.failures += 1
            self.last_failure_time = now

            if self.failures >= self.failure_threshold:
                self.state = "OPEN"

            raise
