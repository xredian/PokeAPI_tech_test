from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    pokeapi: str
    cache_key_stats: str
    cache_key_names: str
    cache_ttl: int
    redis_host: str
    redis_port: int
    redis_db: int

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings()
