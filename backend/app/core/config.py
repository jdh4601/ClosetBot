from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    # pydantic-settings v2 config
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",  # ignore unknown env vars like APP_ENV, FRONTEND_URL
    )
    # Application
    APP_NAME: str = "Fashion Influencer Matcher"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/fasion"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Instagram Graph API
    INSTAGRAM_ACCESS_TOKEN: str = ""
    INSTAGRAM_BUSINESS_ACCOUNT_ID: str = ""
    INSTAGRAM_API_BASE_URL: str = "https://graph.facebook.com/v18.0"
    INSTAGRAM_RATE_LIMIT_PER_HOUR: int = 200

    # Security
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Analysis Settings
    ANALYSIS_MAX_INFLUENCERS: int = 5
    ANALYSIS_MEDIA_LIMIT: int = 20
    CACHE_TTL_PROFILE_HOURS: int = 6
    CACHE_TTL_MEDIA_HOURS: int = 1

settings = Settings()
