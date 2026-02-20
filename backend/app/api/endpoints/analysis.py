from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid
from datetime import datetime

from app.db.database import get_db, get_engine, Base
from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisJobResponse,
    AnalysisResultResponse,
    JobStatus,
)
from app.models import AnalysisJob, AnalysisResult, BrandProfile, InfluencerProfile
from app.core.celery import celery_app
import structlog

logger = structlog.get_logger()

router = APIRouter()


@router.post(
    "/jobs", response_model=AnalysisJobResponse, status_code=status.HTTP_202_ACCEPTED
)
async def create_analysis_job(
    request: AnalysisRequest, db: AsyncSession = Depends(get_db)
):
    """
    새로운 인플루언서 분석 작업을 생성합니다.

    - 브랜드 1개와 인플루언서 최대 5명을 분석합니다
    - 작업은 큐에 등록되며 비동기로 처리됩니다
    - Rate limit(200콜/시간)을 고려하여 순차 처리됩니다
    """
    # Ensure tables exist (dev convenience)
    try:
        async with get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logger.warning("create_all failed (continuing)", error=str(e))

    brand_username = request.brand_username.strip().lower()
    influencers = [u.strip().lower() for u in request.influencer_usernames if u.strip()]
    if not influencers:
        raise HTTPException(status_code=400, detail="influencer_usernames required")
    if len(influencers) > 5:
        raise HTTPException(status_code=400, detail="Up to 5 influencers allowed")

    # Upsert placeholder brand profile (will be populated by worker)
    existing = await db.execute(
        select(BrandProfile).where(BrandProfile.ig_username == brand_username)
    )
    brand = existing.scalar_one_or_none()
    if brand is None:
        brand = BrandProfile(ig_username=brand_username)
        db.add(brand)
        await db.flush()

    # Create AnalysisJob
    job_uuid = uuid.uuid4()
    job = AnalysisJob(
        id=job_uuid,
        brand_profile_id=brand.id,
        influencer_usernames=influencers,
        status="queued",
        api_calls_estimated=156,
        created_at=datetime.utcnow(),
    )
    db.add(job)
    await db.commit()

    # Enqueue Celery task
    celery_app.send_task(
        "app.services.analysis.worker.analyze_influencers_task",
        args=[str(job_uuid), brand_username, influencers],
        queue="analysis",
    )

    return AnalysisJobResponse(
        job_id=job_uuid,
        status=JobStatus.QUEUED,
        message="Analysis job created successfully",
        estimated_completion_minutes=5,
        created_at=job.created_at,
    )


@router.get("/jobs/{job_id}", response_model=AnalysisJobResponse)
async def get_job_status(job_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    분석 작업의 현재 상태를 조회합니다.
    """
    result = await db.execute(select(AnalysisJob).where(AnalysisJob.id == job_id))
    job = result.scalar_one_or_none()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    # Progress is not persisted; approximate based on status
    progress = 50 if job.status == "running" else (0 if job.status == "queued" else 100)

    return AnalysisJobResponse(
        job_id=job.id,
        status=JobStatus(job.status),
        progress_percent=progress if job.status in {"queued", "running"} else None,
        estimated_completion_minutes=2 if job.status in {"queued", "running"} else None,
        created_at=job.created_at,
        started_at=job.started_at,
        finished_at=job.finished_at,
        error_message=job.error_message,
    )


@router.get("/jobs/{job_id}/results", response_model=AnalysisResultResponse)
async def get_analysis_results(job_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    완료된 분석 작업의 결과를 조회합니다.
    """
    # Load job
    job_q = await db.execute(select(AnalysisJob).where(AnalysisJob.id == job_id))
    job = job_q.scalar_one_or_none()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != "done":
        raise HTTPException(
            status_code=404, detail="Job not found or not yet complete"
        )

    # Load brand username
    brand_q = await db.execute(
        select(BrandProfile).where(BrandProfile.id == job.brand_profile_id)
    )
    brand = brand_q.scalar_one_or_none()
    brand_username = brand.ig_username if brand else ""

    # Load results joined with influencer profile
    results_q = await db.execute(
        select(AnalysisResult, InfluencerProfile)
        .where(AnalysisResult.job_id == job_id)
        .where(InfluencerProfile.id == AnalysisResult.influencer_profile_id)
    )
    rows = results_q.fetchall()
    # Sort by final_score desc
    rows.sort(key=lambda r: (r[0].final_score or 0), reverse=True)

    results_payload = []
    for res, infl in rows:
        results_payload.append(
            {
                "username": infl.ig_username,
                "profile_picture_url": getattr(infl, "profile_picture_url", None),
                "followers_count": infl.followers_count or 0,
                "media_count": infl.media_count or 0,
                "biography": infl.biography,
                "avg_engagement_rate": (infl.avg_engagement_rate or 0) / 100.0,
                "scores": {
                    "similarity_score": float(res.similarity_score or 0),
                    "engagement_score": float(res.engagement_score or 0),
                    "category_score": float(res.category_score or 0),
                    "final_score": float(res.final_score or 0),
                    "grade": res.grade or "D",
                },
                "top_posts": [
                    {
                        "permalink": p.get("permalink"),
                        "caption_preview": (p.get("caption") or "")[:80],
                        "engagement_rate": p.get("engagement_rate", 0.0),
                        "likes_count": p.get("likes_count"),
                        "comments_count": p.get("comments_count", 0),
                        "posted_at": p.get("posted_at"),
                    }
                    for p in (res.top_posts or [])
                ],
                "collaboration_signals": [
                    {
                        "brand_username": c.get("brand_username"),
                        "collaboration_type": c.get("collaboration_type"),
                        "post_permalink": c.get("post_permalink"),
                        "posted_at": c.get("posted_at"),
                    }
                    for c in (res.collab_signals or [])
                ],
                # Optional: distribution not stored; leave empty or compute later
                "hashtag_distribution": {},
                "common_hashtags_with_brand": res.common_hashtags or [],
            }
        )

    total_api_calls = job.api_calls_used or job.api_calls_estimated or 0

    return AnalysisResultResponse(
        job_id=job.id,
        brand_username=brand_username,
        status=JobStatus.DONE,
        results=results_payload,
        total_api_calls=total_api_calls,
        created_at=job.created_at,
        completed_at=job.finished_at,
    )
