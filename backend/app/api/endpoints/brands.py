from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.brand import BrandProfile, BrandCreate

router = APIRouter()


@router.post("/analyze", response_model=BrandProfile)
async def analyze_brand(request: BrandCreate, db: AsyncSession = Depends(get_db)):
    """
    브랜드 Instagram 계정을 분석하여 프로필을 생성합니다.

    - Business/Creator 계정만 분석 가능
    - 최근 20개 게시물의 해시태그와 캡션을 분석
    - 카테고리 분류 결과 반환
    """
    # TODO: Implement brand analysis
    # 1. Validate account type
    # 2. Fetch from Instagram API (or cache)
    # 3. Analyze hashtags and captions
    # 4. Store in database
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Brand analysis not yet implemented",
    )


@router.get("/{username}", response_model=BrandProfile)
async def get_brand_profile(username: str, db: AsyncSession = Depends(get_db)):
    """
    캐시된 브랜드 프로필을 조회합니다.
    """
    # TODO: Implement profile retrieval
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Brand @{username} not found"
    )
