from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


class AnalysisRequest(BaseModel):
    brand_username: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Brand Instagram username (without @)",
    )
    influencer_usernames: List[str] = Field(
        ...,
        min_length=1,
        max_length=5,
        description="List of influencer usernames to analyze (1-5)",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "brand_username": "myfashionbrand",
                "influencer_usernames": ["influencer1", "influencer2", "influencer3"],
            }
        }
    )


class AnalysisJobResponse(BaseModel):
    job_id: uuid.UUID
    status: JobStatus
    message: Optional[str] = None
    progress_percent: Optional[int] = Field(None, ge=0, le=100)
    estimated_completion_minutes: Optional[int] = None
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    error_message: Optional[str] = None


class ScoreBreakdown(BaseModel):
    similarity_score: float = Field(
        ..., ge=0, le=100, description="Brand similarity (40%)"
    )
    engagement_score: float = Field(
        ..., ge=0, le=100, description="Engagement quality (35%)"
    )
    category_score: float = Field(..., ge=0, le=100, description="Category fit (25%)")
    final_score: float = Field(..., ge=0, le=100)
    grade: str = Field(..., pattern=r"^[A-D]$")


class CollaborationSignal(BaseModel):
    brand_username: str
    collaboration_type: str  # ad, sponsored, gifted, etc.
    post_permalink: str
    posted_at: datetime


class TopPost(BaseModel):
    permalink: str
    caption_preview: str
    engagement_rate: float
    likes_count: Optional[int]
    comments_count: int
    posted_at: datetime


class InfluencerResult(BaseModel):
    username: str
    profile_picture_url: Optional[str]
    followers_count: int
    media_count: int
    biography: Optional[str]
    avg_engagement_rate: Optional[float] = None
    scores: ScoreBreakdown
    top_posts: List[TopPost]
    collaboration_signals: List[CollaborationSignal]
    hashtag_distribution: Dict[str, float]
    common_hashtags_with_brand: List[str]


class AnalysisResultResponse(BaseModel):
    job_id: uuid.UUID
    brand_username: str
    status: JobStatus
    results: List[InfluencerResult]
    total_api_calls: int
    created_at: datetime
    completed_at: Optional[datetime]
