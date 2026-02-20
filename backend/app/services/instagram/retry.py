"""Retry logic with exponential backoff for Instagram API calls"""

import asyncio
import random
from typing import TypeVar, Callable, Optional
from functools import wraps
import structlog

from app.services.instagram.client import (
    InstagramAPIError,
    RateLimitError,
    AccountNotFoundError,
    PrivateAccountError,
)

logger = structlog.get_logger()

T = TypeVar("T")


def with_retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    retryable_exceptions: tuple = (InstagramAPIError,),
    non_retryable_exceptions: tuple = (AccountNotFoundError, PrivateAccountError),
):
    """
    Decorator that adds exponential backoff retry logic to async functions.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries (seconds)
        max_delay: Maximum delay between retries (seconds)
        exponential_base: Base for exponential backoff calculation
        retryable_exceptions: Tuple of exceptions that should trigger a retry
        non_retryable_exceptions: Tuple of exceptions that should NOT trigger a retry
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)

                except non_retryable_exceptions as e:
                    # Don't retry for these exceptions
                    logger.debug(
                        "Non-retryable exception", error=str(e), func=func.__name__
                    )
                    raise

                except retryable_exceptions as e:
                    last_exception = e

                    # Don't retry on the last attempt
                    if attempt >= max_retries:
                        logger.warning(
                            "Max retries exceeded",
                            func=func.__name__,
                            attempts=attempt + 1,
                            error=str(e),
                        )
                        raise

                    # Handle rate limit specially
                    if isinstance(e, RateLimitError):
                        delay = min(e.retry_after, max_delay)
                        logger.info(
                            "Rate limited, waiting",
                            func=func.__name__,
                            retry_after=delay,
                        )
                    else:
                        # Calculate exponential backoff with jitter
                        delay = min(base_delay * (exponential_base**attempt), max_delay)
                        # Add jitter (±25%) to prevent thundering herd
                        delay *= 0.75 + random.random() * 0.5

                        logger.info(
                            "Retrying after error",
                            func=func.__name__,
                            attempt=attempt + 1,
                            max_retries=max_retries,
                            delay=delay,
                            error=str(e),
                        )

                    await asyncio.sleep(delay)

            # Should not reach here, but just in case
            raise last_exception or InstagramAPIError("Retry failed")

        return wrapper

    return decorator


class RetryableInstagramClient:
    """
    Wrapper around InstagramGraphAPI with built-in retry logic.

    Usage:
        client = RetryableInstagramClient()
        profile = await client.get_profile("username")
    """

    def __init__(self, *args, **kwargs):
        # Import here to avoid circular dependency
        from app.services.instagram.client import InstagramGraphAPI

        self._client = InstagramGraphAPI(*args, **kwargs)

    @with_retry(
        max_retries=3,
        base_delay=2.0,
        retryable_exceptions=(InstagramAPIError,),
        non_retryable_exceptions=(
            AccountNotFoundError,
            PrivateAccountError,
            RateLimitError,
        ),
    )
    async def get_profile(self, *args, **kwargs):
        """Get profile with retry logic"""
        return await self._client.get_profile(*args, **kwargs)

    @with_retry(
        max_retries=2,
        base_delay=1.0,
        retryable_exceptions=(InstagramAPIError,),
        non_retryable_exceptions=(AccountNotFoundError, PrivateAccountError),
    )
    async def validate_account(self, *args, **kwargs):
        """Validate account with retry logic"""
        return await self._client.validate_account(*args, **kwargs)
