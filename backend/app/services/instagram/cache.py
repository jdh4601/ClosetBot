"""Redis Cache Manager for Instagram API responses

Implements caching strategy:
- Profile data: 6 hours TTL
- Media data: 1 hour TTL
"""

import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import redis.asyncio as redis
import structlog

from app.core.config import settings

logger = structlog.get_logger()


class CacheManager:
    """Redis-based cache manager for Instagram API responses"""

    def __init__(
        self,
        redis_client: Optional[redis.Redis] = None,
        profile_ttl_hours: int = 6,
        media_ttl_hours: int = 1,
    ):
        self.redis = redis_client
        self.profile_ttl = profile_ttl_hours * 3600  # Convert to seconds
        self.media_ttl = media_ttl_hours * 3600

    async def _get_redis(self) -> redis.Redis:
        """Get or create Redis connection"""
        if self.redis is None:
            self.redis = redis.from_url(settings.REDIS_URL)
        return self.redis

    def _make_key(self, key_type: str, identifier: str) -> str:
        """Create cache key with prefix"""
        return f"ig:{key_type}:{identifier.lower()}"

    async def get_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get cached profile data.

        Returns:
            Profile data dict or None if not cached
        """
        key = self._make_key("profile", username)
        try:
            r = await self._get_redis()
            data = await r.get(key)
            if data:
                logger.debug("Profile cache hit", username=username)
                return json.loads(data)
            logger.debug("Profile cache miss", username=username)
            return None
        except redis.ConnectionError:
            logger.warning("Redis unavailable, cache miss")
            return None

    async def set_profile(self, username: str, data: Dict[str, Any]) -> bool:
        """
        Cache profile data.

        Args:
            username: Instagram username
            data: Profile data to cache

        Returns:
            True if cached successfully
        """
        key = self._make_key("profile", username)
        try:
            r = await self._get_redis()
            # Add cache metadata
            cache_data = {
                "data": data,
                "cached_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(hours=6)).isoformat(),
            }
            await r.setex(key, self.profile_ttl, json.dumps(cache_data))
            logger.debug("Profile cached", username=username, ttl_hours=6)
            return True
        except redis.ConnectionError:
            logger.warning("Redis unavailable, cache skipped")
            return False

    async def get_media(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get cached media data.

        Returns:
            Media data dict or None if not cached
        """
        key = self._make_key("media", username)
        try:
            r = await self._get_redis()
            data = await r.get(key)
            if data:
                logger.debug("Media cache hit", username=username)
                return json.loads(data)
            logger.debug("Media cache miss", username=username)
            return None
        except redis.ConnectionError:
            logger.warning("Redis unavailable, cache miss")
            return None

    async def set_media(self, username: str, data: Dict[str, Any]) -> bool:
        """
        Cache media data.

        Args:
            username: Instagram username
            data: Media data to cache

        Returns:
            True if cached successfully
        """
        key = self._make_key("media", username)
        try:
            r = await self._get_redis()
            cache_data = {
                "data": data,
                "cached_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
            }
            await r.setex(key, self.media_ttl, json.dumps(cache_data))
            logger.debug("Media cached", username=username, ttl_hours=1)
            return True
        except redis.ConnectionError:
            logger.warning("Redis unavailable, cache skipped")
            return False

    async def invalidate_profile(self, username: str) -> bool:
        """Invalidate cached profile data"""
        key = self._make_key("profile", username)
        try:
            r = await self._get_redis()
            await r.delete(key)
            logger.debug("Profile cache invalidated", username=username)
            return True
        except redis.ConnectionError:
            return False

    async def invalidate_media(self, username: str) -> bool:
        """Invalidate cached media data"""
        key = self._make_key("media", username)
        try:
            r = await self._get_redis()
            await r.delete(key)
            logger.debug("Media cache invalidated", username=username)
            return True
        except redis.ConnectionError:
            return False

    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            r = await self._get_redis()
            # Count keys by pattern
            profile_keys = await r.keys("ig:profile:*")
            media_keys = await r.keys("ig:media:*")

            return {
                "profile_cache_entries": len(profile_keys),
                "media_cache_entries": len(media_keys),
                "profile_ttl_hours": 6,
                "media_ttl_hours": 1,
            }
        except redis.ConnectionError:
            return {
                "profile_cache_entries": 0,
                "media_cache_entries": 0,
                "error": "Redis unavailable",
            }
