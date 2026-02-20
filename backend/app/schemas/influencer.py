from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime


class InfluencerProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    ig_username: str
    followers_count: int
    media_count: int
    biography: Optional[str]
    is_verified: bool
    categories: List[str]
    last_fetched_at: datetime


class InfluencerMedia(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    caption: Optional[str]
    comments_count: int
    like_count: Optional[int]
    media_type: str
    permalink: str
    posted_at: datetime


class InfluencerDetail(InfluencerProfile):
    recent_media: List[InfluencerMedia]
    hashtag_distribution: Dict[str, float]
    avg_engagement_rate: float
