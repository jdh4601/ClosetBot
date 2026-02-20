from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.middleware import (
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
    RequestLoggingMiddleware,
)
from app.api.router import api_router
from app.db.database import get_engine, dispose_engine_if_exists, Base
import structlog

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    # Startup
    logger.info("Starting up Fashion Influencer Matcher API")
    # Avoid forcing a DB connection at startup to prevent boot failures
    # in local/dev without Postgres running. Use readiness probes instead.
    try:
        # Optionally, perform a lightweight DB ping when explicitly enabled
        import os
        if os.getenv("DB_EAGER_INIT", "false").lower() in {"1", "true", "yes"}:
            async with get_engine().begin() as conn:
                pass
    except Exception as e:
        logger.warning("Database not ready at startup", error=str(e))

    yield
    # Shutdown
    logger.info("Shutting down API")
    try:
        await dispose_engine_if_exists()
    except Exception as e:
        logger.warning("Error disposing engine", error=str(e))


app = FastAPI(
    title="Fashion Influencer Matcher API",
    description="SaaS for matching fashion brands with influencers using Instagram data",
    version="1.0.0",
    lifespan=lifespan,
)

# Security middleware (order matters)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    return {
        "name": "Fashion Influencer Matcher API",
        "version": "1.0.0",
        "status": "healthy",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
