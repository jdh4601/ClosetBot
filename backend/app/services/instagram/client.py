"""Instagram Graph API Client

Business Discovery API wrapper for fetching public Instagram profile and media data.
"""

import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime
import structlog

from app.core.config import settings

logger = structlog.get_logger()


class InstagramAPIError(Exception):
    """Base exception for Instagram API errors"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class RateLimitError(InstagramAPIError):
    """Raised when API rate limit is exceeded"""

    def __init__(self, message: str, retry_after: int = 3600):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


class AccountNotFoundError(InstagramAPIError):
    """Raised when the Instagram account is not found or not accessible"""

    def __init__(self, username: str):
        super().__init__(
            f"Account @{username} not found or not accessible", status_code=404
        )
        self.username = username


class PrivateAccountError(InstagramAPIError):
    """Raised when trying to access a private account"""

    def __init__(self, username: str):
        super().__init__(
            f"Account @{username} is private or not a business/creator account",
            status_code=400,
        )
        self.username = username


class InstagramProfile:
    """Represents an Instagram profile from Business Discovery API"""

    def __init__(self, data: Dict[str, Any]):
        self.raw_data = data
        self.id = data.get("id", "")
        self.username = data.get("username", "")
        self.name = data.get("name", "")
        self.followers_count = data.get("followers_count", 0)
        self.follows_count = data.get("follows_count", 0)
        self.media_count = data.get("media_count", 0)
        self.biography = data.get("biography", "")
        self.website = data.get("website", "")
        self.profile_picture_url = data.get("profile_picture_url", "")
        self.is_verified = data.get("is_verified", False)
        self.media: List[InstagramMedia] = []

        # Parse media if present
        if "media" in data and "data" in data["media"]:
            self.media = [InstagramMedia(m) for m in data["media"]["data"]]


class InstagramMedia:
    """Represents an Instagram media post"""

    def __init__(self, data: Dict[str, Any]):
        self.raw_data = data
        self.id = data.get("id", "")
        self.caption = data.get("caption", "")
        self.comments_count = data.get("comments_count", 0)
        self.like_count = data.get("like_count")  # May be None
        self.media_type = data.get("media_type", "")  # IMAGE, VIDEO, CAROUSEL
        self.media_url = data.get("media_url", "")
        self.thumbnail_url = data.get("thumbnail_url", "")
        self.permalink = data.get("permalink", "")
        self.timestamp = data.get("timestamp", "")

    @property
    def posted_at(self) -> Optional[datetime]:
        if self.timestamp:
            try:
                return datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))
            except ValueError:
                return None
        return None


class InstagramGraphAPI:
    """Instagram Graph API Client using Business Discovery"""

    def __init__(
        self,
        access_token: Optional[str] = None,
        business_account_id: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.access_token = access_token or settings.INSTAGRAM_ACCESS_TOKEN
        self.business_account_id = (
            business_account_id or settings.INSTAGRAM_BUSINESS_ACCOUNT_ID
        )
        self.base_url = base_url or settings.INSTAGRAM_API_BASE_URL

        if not self.access_token or not self.business_account_id:
            raise ValueError(
                "Instagram access token and business account ID are required"
            )

    async def get_profile(
        self, username: str, media_limit: int = 20, include_media: bool = True
    ) -> InstagramProfile:
        """
        Fetch a public Instagram profile using Business Discovery API.

        Args:
            username: Instagram username (without @)
            media_limit: Number of recent media posts to fetch (max 25 per call)
            include_media: Whether to include recent media posts

        Returns:
            InstagramProfile object

        Raises:
            AccountNotFoundError: If account doesn't exist or is not accessible
            PrivateAccountError: If account is private or not business/creator
            RateLimitError: If API rate limit is exceeded
            InstagramAPIError: For other API errors
        """
        logger.info("Fetching Instagram profile", username=username)

        # Build fields parameter
        fields = [
            "id",
            "username",
            "name",
            "followers_count",
            "follows_count",
            "media_count",
            "biography",
            "website",
            "profile_picture_url",
            "is_verified",
        ]

        if include_media:
            media_fields = [
                "id",
                "caption",
                "comments_count",
                "like_count",
                "media_type",
                "media_url",
                "thumbnail_url",
                "timestamp",
                "permalink",
            ]
            fields.append(f"media.limit({media_limit}){{{','.join(media_fields)}}}")

        url = f"{self.base_url}/{self.business_account_id}"
        params = {
            "fields": f"business_discovery.username({username}){{{','.join(fields)}}}",
            "access_token": self.access_token,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, params=params)

                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("retry-after", 3600))
                    logger.warning("Rate limit exceeded", retry_after=retry_after)
                    raise RateLimitError(
                        "API rate limit exceeded", retry_after=retry_after
                    )

                # Try to parse body even on HTTP errors to extract Graph error details
                data = None
                try:
                    data = response.json()
                except Exception:
                    data = None

                if data and isinstance(data, dict) and "error" in data:
                    error = data["error"] or {}
                    error_code = error.get("code", "")
                    error_message = error.get("message", "Unknown error")
                    subcode = error.get("error_subcode")

                    # Map common IG errors
                    if error_code == 80004:  # Account not found or not accessible
                        raise AccountNotFoundError(username)
                    elif error_code == 80001:  # Private account
                        raise PrivateAccountError(username)
                    else:
                        raise InstagramAPIError(
                            f"{error_message}",
                            status_code=response.status_code,
                            error_code=str(error_code or subcode or "unknown"),
                        )

                # If no error body, raise for non-2xx
                response.raise_for_status()

                # Extract business discovery data
                business_discovery = data.get("business_discovery", {})
                if not business_discovery:
                    raise AccountNotFoundError(username)

                logger.info("Profile fetched successfully", username=username)
                return InstagramProfile(business_discovery)

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise AccountNotFoundError(username)
                # Try to enrich with body error
                try:
                    body = e.response.json()
                    if isinstance(body, dict) and "error" in body:
                        err = body["error"]
                        msg = err.get("message", str(e))
                        code = err.get("code")
                        raise InstagramAPIError(
                            msg, status_code=e.response.status_code, error_code=str(code)
                        )
                except Exception:
                    pass
                logger.error(
                    "HTTP error", status_code=e.response.status_code, error=str(e)
                )
                raise InstagramAPIError(
                    f"HTTP error: {e}", status_code=e.response.status_code
                )
            except httpx.RequestError as e:
                logger.error("Request error", error=str(e))
                raise InstagramAPIError(f"Request failed: {e}")

    async def validate_account(self, username: str) -> Dict[str, Any]:
        """
        Validate if an account exists and is accessible (business/creator).

        Returns:
            Dict with 'valid' (bool), 'exists' (bool), 'is_business' (bool), 'error' (optional)
        """
        try:
            profile = await self.get_profile(
                username, media_limit=0, include_media=False
            )
            return {
                "valid": True,
                "exists": True,
                "is_business": True,  # Business Discovery only works for business/creator accounts
                "profile": {
                    "username": profile.username,
                    "followers_count": profile.followers_count,
                    "media_count": profile.media_count,
                },
            }
        except AccountNotFoundError:
            return {
                "valid": False,
                "exists": False,
                "is_business": False,
                "error": "Account not found",
            }
        except PrivateAccountError:
            return {
                "valid": False,
                "exists": True,
                "is_business": False,
                "error": "Not a business/creator account",
            }
        except RateLimitError as e:
            return {
                "valid": False,
                "exists": None,
                "is_business": None,
                "error": f"Rate limited. Retry after {e.retry_after}s",
            }
        except InstagramAPIError as e:
            return {
                "valid": False,
                "exists": None,
                "is_business": None,
                "error": e.message,
            }
