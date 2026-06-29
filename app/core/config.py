from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ARTIC_API_BASE_URL: str
    ARTIC_CACHE_TTL: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
