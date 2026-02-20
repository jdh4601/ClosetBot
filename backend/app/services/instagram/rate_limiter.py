"""Token Bucket Rate Limiter for Instagram API

Implements a distributed rate limiter using Redis to ensure we stay within
Instagram's 200 calls/hour limit across all workers.
"""

import asyncio
import time
from typing import Optional
from datetime import datetime, timedelta
import redis.asyncio as redis
import structlog

from app.core.config import settings

logger = structlog.get_logger()


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded and no capacity available"""

    pass


class TokenBucketRateLimiter:
    """
    Token bucket rate limiter using Redis for distributed coordination.

    Instagram Graph API limit: 200 calls per hour per app.
    We use a conservative limit of 180 calls/hour to have a safety buffer.
    """

    def __init__(
        self,
        redis_client: Optional[redis.Redis] = None,
        max_calls_per_hour: int = 180,  # Conservative limit (200 - 20 buffer)
        bucket_key: str = "instagram_api_rate_limit",
    ):
        self.redis = redis_client
        self.max_calls = max_calls_per_hour
        self.bucket_key = bucket_key
        self.window_seconds = 3600  # 1 hour

        # Local fallback for when Redis is not available (single instance only)
        self._local_tokens = max_calls_per_hour
        self._local_last_refill = time.time()

    async def _get_redis(self) -> redis.Redis:
        """Get or create Redis connection"""
        if self.redis is None:
            self.redis = redis.from_url(settings.REDIS_URL)
        return self.redis

    async def acquire(
        self, tokens: int = 1, block: bool = True, timeout: Optional[float] = None
    ) -> bool:
        """
        Attempt to acquire tokens from the bucket.

        Args:
            tokens: Number of tokens to acquire (usually 1 per API call)
            block: If True, wait until tokens are available
            timeout: Maximum time to wait (seconds)

        Returns:
            True if tokens were acquired, False otherwise

        Raises:
            RateLimitExceeded: If tokens cannot be acquired and block=False
        """
        start_time = time.time()

        while True:
            available, retry_after = await self._check_and_consume(tokens)

            if available:
                return True

            if not block:
                raise RateLimitExceeded(
                    f"Rate limit exceeded. Try again in {retry_after} seconds"
                )

            if timeout and (time.time() - start_time) >= timeout:
                raise RateLimitExceeded("Timeout waiting for rate limit")

            # Wait before retrying
            wait_time = min(retry_after, 10)  # Max 10 second wait between checks
            logger.debug("Rate limit reached, waiting", wait_seconds=wait_time)
            await asyncio.sleep(wait_time)

    async def _check_and_consume(self, tokens: int) -> tuple[bool, int]:
        """
        Check availability and consume tokens if available.

        Returns:
            Tuple of (success: bool, retry_after_seconds: int)
        """
        try:
            r = await self._get_redis()
            now = time.time()

            # Use Redis Lua script for atomic operation
            lua_script = """
            local key = KEYS[1]
            local max_tokens = tonumber(ARGV[1])
            local window = tonumber(ARGV[2])
            local requested = tonumber(ARGV[3])
            local now = tonumber(ARGV[4])
            
            -- Get current state
            local state = redis.call('HMGET', key, 'tokens', 'last_refill')
            local current_tokens = tonumber(state[1]) or max_tokens
            local last_refill = tonumber(state[2]) or now
            
            -- Calculate tokens to add based on time passed
            local time_passed = now - last_refill
            local tokens_to_add = (time_passed / window) * max_tokens
            current_tokens = math.min(max_tokens, current_tokens + tokens_to_add)
            
            -- Check if we can fulfill the request
            if current_tokens >= requested then
                current_tokens = current_tokens - requested
                redis.call('HMSET', key, 'tokens', current_tokens, 'last_refill', now)
                redis.call('EXPIRE', key, window)
                return {1, 0}  -- Success, no retry needed
            else
                -- Calculate retry after
                local tokens_needed = requested - current_tokens
                local retry_after = math.ceil((tokens_needed / max_tokens) * window)
                redis.call('HMSET', key, 'tokens', current_tokens, 'last_refill', now)
                redis.call('EXPIRE', key, window)
                return {0, retry_after}  -- Failed, return retry_after
            end
            """

            result = await r.eval(
                lua_script,
                1,  # Number of keys
                self.bucket_key,
                self.max_calls,
                self.window_seconds,
                tokens,
                now,
            )

            success = result[0] == 1
            retry_after = result[1]

            return success, retry_after

        except redis.ConnectionError:
            # Fallback to local rate limiting if Redis is unavailable
            logger.warning("Redis unavailable, using local rate limiter")
            return self._local_check_and_consume(tokens)

    def _local_check_and_consume(self, tokens: int) -> tuple[bool, int]:
        """Local in-memory rate limiting (fallback)"""
        now = time.time()
        time_passed = now - self._local_last_refill

        # Refill tokens
        tokens_to_add = (time_passed / self.window_seconds) * self.max_calls
        self._local_tokens = min(self.max_calls, self._local_tokens + tokens_to_add)
        self._local_last_refill = now

        if self._local_tokens >= tokens:
            self._local_tokens -= tokens
            return True, 0
        else:
            tokens_needed = tokens - self._local_tokens
            retry_after = int((tokens_needed / self.max_calls) * self.window_seconds)
            return False, retry_after

    async def get_status(self) -> dict:
        """Get current rate limit status"""
        try:
            r = await self._get_redis()
            state = await r.hmget(self.bucket_key, "tokens", "last_refill")

            if state[0] is None:
                return {
                    "available_calls": self.max_calls,
                    "max_calls": self.max_calls,
                    "used_calls": 0,
                    "reset_time": datetime.utcnow()
                    + timedelta(seconds=self.window_seconds),
                }

            tokens = float(state[0])
            last_refill = float(state[1])
            now = time.time()

            # Calculate current available tokens
            time_passed = now - last_refill
            tokens_to_add = (time_passed / self.window_seconds) * self.max_calls
            available = min(self.max_calls, tokens + tokens_to_add)

            return {
                "available_calls": int(available),
                "max_calls": self.max_calls,
                "used_calls": self.max_calls - int(available),
                "reset_time": datetime.utcnow()
                + timedelta(seconds=self.window_seconds),
            }
        except redis.ConnectionError:
            return {
                "available_calls": int(self._local_tokens),
                "max_calls": self.max_calls,
                "used_calls": self.max_calls - int(self._local_tokens),
                "reset_time": datetime.utcnow()
                + timedelta(seconds=self.window_seconds),
                "fallback": "local",
            }

    async def reset(self):
        """Reset the rate limiter (for testing)"""
        try:
            r = await self._get_redis()
            await r.delete(self.bucket_key)
        except redis.ConnectionError:
            pass

        self._local_tokens = self.max_calls
        self._local_last_refill = time.time()
