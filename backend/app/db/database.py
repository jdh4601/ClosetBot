from typing import Optional
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from app.core.config import settings


# Lazy engine/session initialization to avoid hard failures at import time
_engine: Optional[AsyncEngine] = None
_sessionmaker: Optional[async_sessionmaker] = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        db_url = settings.DATABASE_URL.replace(
            "postgresql://", "postgresql+asyncpg://"
        )
        # Supabase DSN 종종 sslmode=require를 사용함. asyncpg는 ssl 파라미터를 선호하므로 변환.
        if "postgresql+asyncpg://" in db_url:
            db_url = db_url.replace("?sslmode=require", "?ssl=true").replace(
                "&sslmode=require", "&ssl=true"
            )
        _engine = create_async_engine(
            db_url,
            echo=settings.DEBUG,
            poolclass=NullPool if settings.DEBUG else None,
        )
    return _engine


def get_sessionmaker() -> async_sessionmaker:
    global _sessionmaker
    if _sessionmaker is None:
        _sessionmaker = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
    return _sessionmaker


# Base class for models
Base = declarative_base()


async def get_db():
    """Dependency for getting async database session"""
    SessionLocal = get_sessionmaker()
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def dispose_engine_if_exists() -> None:
    """Dispose the engine if it has been initialized."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
