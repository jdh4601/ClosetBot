from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    Boolean,
    Text,
    ForeignKey,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Optional for MVP
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BrandProfile(Base):
    __tablename__ = "brand_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    ig_username = Column(String(30), unique=True, nullable=False, index=True)
    ig_id = Column(String(50), nullable=True)
    name = Column(String(100), nullable=True)
    followers_count = Column(Integer, default=0)
    media_count = Column(Integer, default=0)
    biography = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    profile_picture_url = Column(String(500), nullable=True)
    is_verified = Column(Boolean, default=False)
    categories = Column(JSONB, default=list)
    extracted_keywords = Column(JSONB, default=list)
    last_fetched_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))  # 90 days retention


class InfluencerProfile(Base):
    __tablename__ = "influencer_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ig_username = Column(String(30), unique=True, nullable=False, index=True)
    ig_id = Column(String(50), nullable=True)
    name = Column(String(100), nullable=True)
    followers_count = Column(Integer, default=0)
    follows_count = Column(Integer, default=0)
    media_count = Column(Integer, default=0)
    biography = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    profile_picture_url = Column(String(500), nullable=True)
    is_verified = Column(Boolean, default=False)
    categories = Column(JSONB, default=list)
    avg_engagement_rate = Column(
        Integer, nullable=True
    )  # Stored as basis points (e.g., 520 = 5.2%)
    last_fetched_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))  # 90 days retention


class MediaSnapshot(Base):
    __tablename__ = "media_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), nullable=False)
    profile_type = Column(String(10), nullable=False)  # 'brand' or 'influencer'
    ig_media_id = Column(String(50), nullable=False)
    caption = Column(Text, nullable=True)
    comments_count = Column(Integer, default=0)
    like_count = Column(Integer, nullable=True)
    media_type = Column(String(20), nullable=True)  # IMAGE, VIDEO, CAROUSEL
    permalink = Column(String(500), nullable=True)
    posted_at = Column(DateTime(timezone=True))
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))  # 90 days retention


class HashtagAggregate(Base):
    __tablename__ = "hashtag_aggregates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), nullable=False)
    profile_type = Column(String(10), nullable=False)  # 'brand' or 'influencer'
    hashtag = Column(String(100), nullable=False, index=True)
    count = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    brand_profile_id = Column(UUID(as_uuid=True), ForeignKey("brand_profiles.id"))
    influencer_usernames = Column(JSONB, nullable=False)  # List of usernames
    status = Column(String(20), default="queued")  # queued, running, done, failed
    api_calls_used = Column(Integer, default=0)
    api_calls_estimated = Column(Integer, default=156)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))  # 90 days retention


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("analysis_jobs.id"))
    influencer_profile_id = Column(
        UUID(as_uuid=True), ForeignKey("influencer_profiles.id")
    )
    similarity_score = Column(Integer, nullable=True)  # 0-100
    engagement_score = Column(Integer, nullable=True)  # 0-100
    category_score = Column(Integer, nullable=True)  # 0-100
    final_score = Column(Integer, nullable=True)  # 0-100
    grade = Column(String(1), nullable=True)  # A, B, C, D
    top_posts = Column(JSONB, default=list)
    collab_signals = Column(JSONB, default=list)
    common_hashtags = Column(JSONB, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CategoryTaxonomy(Base):
    __tablename__ = "category_taxonomy"

    slug = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    keywords = Column(JSONB, default=list)  # List of related hashtags
    weight = Column(Integer, default=100)  # For prioritization
    parent_slug = Column(
        String(50), ForeignKey("category_taxonomy.slug"), nullable=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
