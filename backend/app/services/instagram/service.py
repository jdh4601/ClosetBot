"""High-level Instagram service with caching and rate limiting"""

from typing import Optional, Dict, Any
from datetime import datetime
import structlog

from app.services.instagram.client import (
    InstagramGraphAPI,
    InstagramProfile,
    InstagramAPIError,
    AccountNotFoundError,
    PrivateAccountError,
)
from app.services.instagram.rate_limiter import (
    TokenBucketRateLimiter,
    RateLimitExceeded,
)
from app.services.instagram.cache import CacheManager
from app.services.instagram.retry import with_retry

logger = structlog.get_logger()


class InstagramService:
    """
    High-level service for Instagram API operations.

    Features:
    - Rate limiting (200 calls/hour)
    - Caching (profile: 6h, media: 1h)
    - Retry logic with exponential backoff
    - Account validation
    """

    def __init__(
        self,
        access_token: Optional[str] = None,
        business_account_id: Optional[str] = None,
        rate_limiter: Optional[TokenBucketRateLimiter] = None,
        cache: Optional[CacheManager] = None,
    ):
        self.client = InstagramGraphAPI(access_token, business_account_id)
        self.rate_limiter = rate_limiter or TokenBucketRateLimiter()
        self.cache = cache or CacheManager()

    async def get_profile_with_cache(
        self, username: str, media_limit: int = 20, use_cache: bool = True
    ) -> InstagramProfile:
        """
        Get profile with caching and rate limiting.

        Args:
            username: Instagram username
            media_limit: Number of media posts to fetch
            use_cache: Whether to use cached data

        Returns:
            InstagramProfile object
        """
        logger.info("Getting profile", username=username, use_cache=use_cache)

        # Check cache first
        if use_cache:
            cached = await self.cache.get_profile(username)
            if cached:
                logger.info("Using cached profile", username=username)
                return InstagramProfile(cached["data"])

        # Acquire rate limit token
        await self.rate_limiter.acquire(tokens=1)

        # Fetch from API
        profile = await self._fetch_profile(username, media_limit)

        # Cache the result
        if use_cache:
            await self.cache.set_profile(username, profile.raw_data)

        return profile

    @with_retry(max_retries=3, base_delay=2.0)
    async def _fetch_profile(self, username: str, media_limit: int) -> InstagramProfile:
        """Internal method to fetch profile with retry logic"""
        return await self.client.get_profile(username, media_limit)

    async def validate_account(self, username: str) -> Dict[str, Any]:
        """
        Validate if an account is accessible and is a business/creator account.

        Returns:
            Dict with validation result
        """
        logger.info("Validating account", username=username)

        try:
            await self.rate_limiter.acquire(tokens=1)
            result = await self.client.validate_account(username)
            logger.info(
                "Account validation complete",
                username=username,
                valid=result.get("valid"),
            )
            return result
        except RateLimitExceeded as e:
            logger.warning("Rate limit exceeded during validation", username=username)
            return {
                "valid": False,
                "exists": None,
                "is_business": None,
                "error": str(e),
            }

    async def invalidate_cache(self, username: str) -> None:
        """Invalidate cached data for a username"""
        await self.cache.invalidate_profile(username)
        await self.cache.invalidate_media(username)
        logger.info("Cache invalidated", username=username)

    async def get_rate_limit_status(self) -> Dict[str, Any]:
        """Get current rate limit status"""
        return await self.rate_limiter.get_status()

    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return await self.cache.get_stats()
