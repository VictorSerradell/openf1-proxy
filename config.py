# archivo: config.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    OPENF1_BASE_URL: str = Field(default="https://api.openf1.org/v1")
    REDIS_URL: str | None = None
    CACHE_LIVE_TTL: int = 10
    CACHE_HISTORICAL_TTL: int = 3600
    API_KEYS: str = ""
    INTERNAL_RATE_LIMIT_PER_SECOND: int = 3
    INTERNAL_RATE_LIMIT_PER_MINUTE: int = 30

    class Config:
        env_file = ".env"

    @property
    def api_keys_list(self) -> List[str]:
        if not self.API_KEYS:
            return []
        return [k.strip() for k in self.API_KEYS.split(",")]


settings = Settings()
