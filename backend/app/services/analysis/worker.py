"""Celery tasks for analysis"""

from typing import List
from celery import shared_task
import structlog

logger = structlog.get_logger()


@shared_task(bind=True, max_retries=3)
def analyze_influencers_task(
    self, job_id: str, brand_username: str, influencer_usernames: List[str]
):
    """
    Celery task to analyze influencers.

    Args:
        job_id: Analysis job ID
        brand_username: Brand Instagram username
        influencer_usernames: List of influencer usernames to analyze
    """
    import asyncio
    from sqlalchemy import select, update
    from sqlalchemy.ext.asyncio import AsyncSession
    from datetime import datetime, timedelta

    from app.db.database import get_sessionmaker, get_engine, Base
    from app.models import AnalysisJob, AnalysisResult, InfluencerProfile, BrandProfile
    from app.services.instagram import InstagramService
    from app.services.analysis.orchestrator import AnalysisOrchestrator

    logger.info(
        "Starting analysis task",
        job_id=job_id,
        brand=brand_username,
        influencers_count=len(influencer_usernames),
    )

    async def run_analysis():
        # Ensure tables exist (dev convenience; safe no-op if already created)
        try:
            async with get_engine().begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            logger.warning("create_all failed (continuing)", error=str(e))

        SessionLocal = get_sessionmaker()
        async with SessionLocal() as db:
            instagram_service = InstagramService()
            orchestrator = AnalysisOrchestrator(instagram_service, db)

            try:
                # Mark job as running
                await _mark_job_running(db, job_id)

                # 1. Analyze brand
                logger.info("Analyzing brand", job_id=job_id, brand=brand_username)
                brand_data = await orchestrator.analyze_brand(brand_username)

                # Upsert brand profile minimal info
                brand_profile = await _upsert_brand_profile(db, brand_data)

                # 2. Analyze each influencer
                results = []
                total = len(influencer_usernames)

                for idx, username in enumerate(influencer_usernames):
                    # Update progress
                    progress = int((idx / total) * 100)
                    logger.info(
                        "Analyzing influencer",
                        job_id=job_id,
                        username=username,
                        progress=progress,
                    )

                    try:
                        result = await orchestrator.analyze_influencer(
                            username, brand_data
                        )
                        results.append(result)

                        # Upsert influencer profile and persist analysis result
                        influencer = await _upsert_influencer_profile(db, result)
                        await _store_analysis_result(db, job_id, influencer.id, result)
                    except Exception as e:
                        logger.error(
                            "Failed to analyze influencer",
                            job_id=job_id,
                            username=username,
                            error=str(e),
                        )
                        # Continue with other influencers

                # Sort by final score descending
                results.sort(key=lambda x: x["scores"]["final_score"], reverse=True)

                logger.info(
                    "Analysis completed", job_id=job_id, results_count=len(results)
                )

                # Mark job as done
                await _mark_job_done(db, job_id, api_calls_used=None)

                return {
                    "job_id": job_id,
                    "brand_username": brand_username,
                    "results": results,
                    "status": "done",
                }

            except Exception as e:
                logger.error("Analysis failed", job_id=job_id, error=str(e))
                raise

    # Run async function in sync Celery task
    try:
        result = asyncio.run(run_analysis())
        return result
    except Exception as exc:
        logger.error("Task failed, retrying", error=str(exc))
        raise self.retry(exc=exc, countdown=60)


@shared_task
def cleanup_expired_data():
    """Periodic task to clean up expired data (runs daily)"""
    import asyncio
    from sqlalchemy import text
    from app.db.database import AsyncSessionLocal
    from datetime import datetime, timedelta

    logger.info("Starting cleanup of expired data")

    async def cleanup():
        async with AsyncSessionLocal() as db:
            # Delete data older than 90 days
            cutoff_date = datetime.utcnow() - timedelta(days=90)

            # This is a simplified version - in production, use proper ORM queries
            tables = [
                "brand_profiles",
                "influencer_profiles",
                "media_snapshots",
                "analysis_jobs",
                "analysis_results",
            ]

            for table in tables:
                query = text(f"""
                    DELETE FROM {table}
                    WHERE expires_at < :cutoff_date
                """)
                await db.execute(query, {"cutoff_date": cutoff_date})

            await db.commit()

    asyncio.run(cleanup())
    logger.info("Cleanup completed")


# --------------------
# Helper async functions
# --------------------

async def _mark_job_running(db: AsyncSession, job_id: str) -> None:
    from sqlalchemy import update
    from app.models import AnalysisJob
    from datetime import datetime

    await db.execute(
        update(AnalysisJob)
        .where(AnalysisJob.id == job_id)
        .values(status="running", started_at=datetime.utcnow())
    )
    await db.commit()


async def _mark_job_done(db: AsyncSession, job_id: str, api_calls_used: int | None) -> None:
    from sqlalchemy import update
    from app.models import AnalysisJob
    from datetime import datetime

    values = {"status": "done", "finished_at": datetime.utcnow()}
    if api_calls_used is not None:
        values["api_calls_used"] = api_calls_used
    await db.execute(update(AnalysisJob).where(AnalysisJob.id == job_id).values(**values))
    await db.commit()


async def _upsert_brand_profile(db: AsyncSession, brand_data: dict):
    from sqlalchemy import select
    from app.models import BrandProfile
    from datetime import datetime, timedelta

    username = brand_data.get("username")
    result = await db.execute(
        select(BrandProfile).where(BrandProfile.ig_username == username)
    )
    brand = result.scalar_one_or_none()
    if brand is None:
        brand = BrandProfile(
            ig_username=username,
            followers_count=brand_data.get("followers_count", 0),
            media_count=brand_data.get("media_count", 0),
            biography=brand_data.get("biography"),
            categories=brand_data.get("categories", []),
            profile_picture_url=None,
            last_fetched_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=90),
        )
        db.add(brand)
        await db.flush()
    else:
        brand.followers_count = brand_data.get("followers_count", brand.followers_count)
        brand.media_count = brand_data.get("media_count", brand.media_count)
        brand.biography = brand_data.get("biography", brand.biography)
        brand.categories = brand_data.get("categories", brand.categories)
        brand.last_fetched_at = datetime.utcnow()
    await db.commit()
    return brand


async def _upsert_influencer_profile(db: AsyncSession, infl_data: dict):
    from sqlalchemy import select
    from app.models import InfluencerProfile
    from datetime import datetime, timedelta

    username = infl_data.get("username")
    result = await db.execute(
        select(InfluencerProfile).where(InfluencerProfile.ig_username == username)
    )
    influencer = result.scalar_one_or_none()
    if influencer is None:
        influencer = InfluencerProfile(
            ig_username=username,
            followers_count=infl_data.get("followers_count", 0),
            media_count=infl_data.get("media_count", 0),
            biography=infl_data.get("biography"),
            profile_picture_url=infl_data.get("profile_picture_url"),
            is_verified=False,
            categories=infl_data.get("categories", []),
            avg_engagement_rate=int(round((infl_data.get("avg_engagement_rate", 0.0) or 0.0) * 100)),
            last_fetched_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=90),
        )
        db.add(influencer)
        await db.flush()
    else:
        influencer.followers_count = infl_data.get("followers_count", influencer.followers_count)
        influencer.media_count = infl_data.get("media_count", influencer.media_count)
        influencer.biography = infl_data.get("biography", influencer.biography)
        influencer.profile_picture_url = infl_data.get(
            "profile_picture_url", influencer.profile_picture_url
        )
        influencer.categories = infl_data.get("categories", influencer.categories)
        if infl_data.get("avg_engagement_rate") is not None:
            influencer.avg_engagement_rate = int(round(infl_data["avg_engagement_rate"] * 100))
        influencer.last_fetched_at = datetime.utcnow()
    await db.commit()
    return influencer


async def _store_analysis_result(
    db: AsyncSession, job_id: str, influencer_id, infl_data: dict
) -> None:
    from app.models import AnalysisResult

    scores = infl_data.get("scores", {})
    top_posts = infl_data.get("top_posts", [])
    collabs = infl_data.get("collaboration_signals", [])
    common_tags = infl_data.get("common_hashtags_with_brand", [])

    result = AnalysisResult(
        job_id=job_id,
        influencer_profile_id=influencer_id,
        similarity_score=int(round(scores.get("similarity_score", 0))),
        engagement_score=int(round(scores.get("engagement_score", 0))),
        category_score=int(round(scores.get("category_score", 0))),
        final_score=int(round(scores.get("final_score", 0))),
        grade=scores.get("grade"),
        top_posts=top_posts,
        collab_signals=collabs,
        common_hashtags=common_tags,
    )
    db.add(result)
    await db.commit()
