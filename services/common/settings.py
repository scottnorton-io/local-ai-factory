from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings


class FactorySettings(BaseSettings):
    """Shared configuration for Local AI Factory services.

    Values are loaded from environment variables with the FACTORY_ prefix
    (for example, FACTORY_DB_HOST, FACTORY_ENV, etc.).
    """

    env: str = "local"  # local | demo | test

    db_host: str = "db"
    db_port: int = 5432
    db_name: str = "factory"
    db_user: str = "factory"
    db_password: str = "factory"

    ollama_host: str = "host.docker.internal"
    ollama_port: int = 11434

    class Config:
        env_prefix = "FACTORY_"


@lru_cache(maxsize=1)
def get_settings() -> FactorySettings:
    return FactorySettings()
    
