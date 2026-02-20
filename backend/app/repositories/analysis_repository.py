"""Repository for analysis-related database operations"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models import (
    AnalysisJob,
    AnalysisResult,
    BrandProfile,
    InfluencerProfile,
)
from typing import Optional, List
import uuid
from datetime import datetime, timedelta
import structlog

logger = structlog.get_logger()


class AnalysisRepository:
    """Repository for analysis job and result operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_job(
        self,
        brand_username: str,
        influencer_usernames: List[str],
        user_id: Optional[uuid.UUID] = None,
    ) -> AnalysisJob:
        """
        Create new analysis job with brand profile.

        Args:
            brand_username: Brand Instagram username
            influencer_usernames: List of influencer usernames
            user_id: Optional user ID

        Returns:
            Created AnalysisJob
        """
        # Get or create brand profile
        brand = await self._get_or_create_brand_profile(brand_username)

        job = AnalysisJob(
            id=uuid.uuid4(),
            user_id=user_id,
            brand_profile_id=brand.id,
            influencer_usernames=influencer_usernames,
            status="queued",
            api_calls_estimated=156,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=90),
        )
        self.db.add(job)
        await self.db.flush()
        return job

    async def get_job(self, job_id: uuid.UUID) -> Optional[AnalysisJob]:
        """
        Get job by ID.

        Args:
            job_id: Job UUID

        Returns:
            AnalysisJob or None if not found
        """
        result = await self.db.execute(
            select(AnalysisJob).where(AnalysisJob.id == job_id)
        )
        return result.scalar_one_or_none()

    async def update_job_status(
        self,
        job_id: uuid.UUID,
        status: str,
        error_message: Optional[str] = None,
        api_calls_used: Optional[int] = None,
    ) -> None:
        """
        Update job status.

        Args:
            job_id: Job UUID
            status: New status (queued, running, done, failed)
            error_message: Optional error message
            api_calls_used: Optional API calls count
        """
        update_data = {"status": status}

        if status == "running":
            update_data["started_at"] = datetime.utcnow()
        elif status in ["done", "failed"]:
            update_data["finished_at"] = datetime.utcnow()

        if error_message:
            update_data["error_message"] = error_message
        if api_calls_used is not None:
            update_data["api_calls_used"] = api_calls_used

        await self.db.execute(
            update(AnalysisJob).where(AnalysisJob.id == job_id).values(**update_data)
        )
        await self.db.commit()

    async def save_results(
        self, job_id: uuid.UUID, results: List[dict]
    ) -> List[AnalysisResult]:
        """
        Save analysis results.

        Args:
            job_id: Job UUID
            results: List of result dictionaries from orchestrator

        Returns:
            List of created AnalysisResult objects
        """
        result_objects = []

        for result_data in results:
            # Get or create influencer profile
            influencer = await self._get_or_create_influencer_profile(
                result_data["username"], result_data
            )

            # Create result
            result = AnalysisResult(
                id=uuid.uuid4(),
                job_id=job_id,
                influencer_profile_id=influencer.id,
                similarity_score=int(result_data["scores"]["similarity_score"]),
                engagement_score=int(result_data["scores"]["engagement_score"]),
                category_score=int(result_data["scores"]["category_score"]),
                final_score=int(result_data["scores"]["final_score"]),
                grade=result_data["scores"]["grade"],
                top_posts=result_data.get("top_posts", []),
                collab_signals=result_data.get("collaboration_signals", []),
                common_hashtags=result_data.get("common_hashtags_with_brand", []),
                created_at=datetime.utcnow(),
            )
            self.db.add(result)
            result_objects.append(result)

        await self.db.commit()
        return result_objects

    async def get_results_by_job(self, job_id: uuid.UUID) -> List[AnalysisResult]:
        """
        Get all results for a job, ordered by score desc.

        Args:
            job_id: Job UUID

        Returns:
            List of AnalysisResult objects
        """
        result = await self.db.execute(
            select(AnalysisResult)
            .where(AnalysisResult.job_id == job_id)
            .order_by(AnalysisResult.final_score.desc())
        )
        return list(result.scalars().all())

    async def _get_or_create_brand_profile(self, username: str) -> BrandProfile:
        """
        Get existing or create placeholder brand profile.

        Args:
            username: Instagram username

        Returns:
            BrandProfile object
        """
        result = await self.db.execute(
            select(BrandProfile).where(BrandProfile.ig_username == username)
        )
        profile = result.scalar_one_or_none()

        if not profile:
            profile = BrandProfile(
                id=uuid.uuid4(),
                ig_username=username,
                followers_count=0,
                media_count=0,
                is_verified=False,
                created_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=90),
            )
            self.db.add(profile)
            await self.db.flush()

        return profile

    async def _get_or_create_influencer_profile(
        self, username: str, data: dict
    ) -> InfluencerProfile:
        """
        Get existing or create new influencer profile.

        Args:
            username: Instagram username
            data: Profile data from orchestrator

        Returns:
            InfluencerProfile object
        """
        result = await self.db.execute(
            select(InfluencerProfile).where(InfluencerProfile.ig_username == username)
        )
        profile = result.scalar_one_or_none()

        if profile:
            # Update existing profile
            profile.followers_count = data["followers_count"]
            profile.media_count = data["media_count"]
            profile.biography = data.get("biography")
            profile.profile_picture_url = data.get("profile_picture_url")
            profile.categories = data.get("categories", [])
            profile.last_fetched_at = datetime.utcnow()
        else:
            # Create new profile
            profile = InfluencerProfile(
                id=uuid.uuid4(),
                ig_username=username,
                name=data.get("name"),
                followers_count=data["followers_count"],
                media_count=data["media_count"],
                biography=data.get("biography"),
                profile_picture_url=data.get("profile_picture_url"),
                categories=data.get("categories", []),
                is_verified=False,
                last_fetched_at=datetime.utcnow(),
                created_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=90),
            )
            self.db.add(profile)

        await self.db.flush()
        return profile
