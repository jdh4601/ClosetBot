from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.database import get_db
from app.schemas.influencer import InfluencerProfile, InfluencerDetail
from app.services.instagram import InstagramService

router = APIRouter()


@router.get("/search", response_model=List[InfluencerProfile])
async def search_influencers(
    username: Optional[str] = Query(None, description="Instagram username to search"),
    db: AsyncSession = Depends(get_db),
):
    """
    인플루언서를 검색합니다 (캐시된 데이터 기준).
    """
    # TODO: Implement search from cached profiles
    return []


@router.get("/validate")
async def validate_influencer_account(
    username: str = Query(..., description="Instagram username")
):
    """Validate if an Instagram account exists and is accessible (business/creator)."""
    service = InstagramService()
    result = await service.validate_account(username)
    return result


@router.get("/{username}", response_model=InfluencerDetail)
async def get_influencer_detail(username: str, db: AsyncSession = Depends(get_db)):
    """
    특정 인플루언서의 상세 정보를 조회합니다.
    """
    # TODO: Implement detail retrieval with media data
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Influencer @{username} not found",
    )
