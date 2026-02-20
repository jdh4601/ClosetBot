"""API dependencies for authentication and database"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.core.security import decode_access_token, TokenData

# HTTP Bearer token scheme
security_scheme = HTTPBearer(auto_error=False)


async def get_db() -> Generator:
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> TokenData:
    """
    Get current user from JWT token.

    Args:
        credentials: HTTP Authorization credentials

    Returns:
        TokenData containing user information

    Raises:
        HTTPException: If token is invalid or missing
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    token_data = decode_access_token(token)

    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_data


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> Optional[TokenData]:
    """
    Get current user if authenticated, otherwise return None.
    Used for endpoints that work with or without authentication.
    """
    if not credentials:
        return None

    token = credentials.credentials
    return decode_access_token(token)


# Common dependency aliases
CurrentUser = Depends(get_current_user)
OptionalCurrentUser = Depends(get_current_user_optional)
DBSession = Depends(get_db)
