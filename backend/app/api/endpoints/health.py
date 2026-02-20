from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
from sqlalchemy import text
import redis.asyncio as redis

from app.db.database import get_engine
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "fasion-api"}


@router.get("/ready", response_model=Dict[str, Any])
async def readiness_check():
    """Readiness probe: checks DB and Redis connectivity"""
    checks: Dict[str, str] = {}

    # DB check
    try:
        async with get_engine().begin() as conn:
            await conn.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = "error"

    # Redis check
    try:
        r = redis.from_url(settings.REDIS_URL)
        await r.ping()
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "error"

    all_ok = all(v == "ok" for v in checks.values())
    payload = {"status": "ready" if all_ok else "not_ready", "checks": checks}
    status_code = status.HTTP_200_OK if all_ok else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(content=payload, status_code=status_code)
