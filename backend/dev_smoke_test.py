"""
MVP 스모크 테스트:
- FastAPI 기본 엔드포인트 확인 (/ and /api/v1/health)
- AnalysisOrchestrator 파이프라인을 InstagramService 모의 객체로 테스트

실행: python backend/dev_smoke_test.py
"""

from fastapi.testclient import TestClient
from typing import Any, Dict, List
from datetime import datetime, timedelta

from app.services.analysis.orchestrator import AnalysisOrchestrator
from app.services.instagram.client import InstagramProfile
from app.db.database import AsyncSession


# ----------------------
# FastAPI smoke tests
# ----------------------
def test_fastapi_health() -> None:
    from main import app

    client = TestClient(app)
    r_root = client.get("/")
    assert r_root.status_code == 200, r_root.text

    r_health = client.get("/api/v1/health")
    assert r_health.status_code == 200, r_health.text
    data = r_health.json()
    assert data.get("status") == "ok" or data.get("status") == "healthy"


# ----------------------
# Orchestrator smoke test
# ----------------------
class FakeInstagramService:
    def __init__(self) -> None:
        now = datetime.utcnow()
        # 브랜드 프로필(해시태그 분포 유도용)
        self.brand_profile = InstagramProfile(
            {
                "id": "b1",
                "username": "brandx",
                "followers_count": 12000,
                "media_count": 50,
                "biography": "Sustainable minimal fashion",
                "media": {
                    "data": [
                        {
                            "id": "bm1",
                            "caption": "Love #fashion #minimal #eco",
                            "comments_count": 10,
                            "like_count": 200,
                            "media_type": "IMAGE",
                            "permalink": "https://ig/bm1",
                            "timestamp": now.isoformat() + "Z",
                        },
                        {
                            "id": "bm2",
                            "caption": "Our new drop #sustainable #fashion",
                            "comments_count": 5,
                            "like_count": 120,
                            "media_type": "IMAGE",
                            "permalink": "https://ig/bm2",
                            "timestamp": (now - timedelta(days=1)).isoformat() + "Z",
                        },
                    ]
                },
            }
        )

        # 인플루언서 프로필(브랜드와 일부 해시태그 겹치도록)
        self.influencer_profile = InstagramProfile(
            {
                "id": "i1",
                "username": "influencer_a",
                "followers_count": 45000,
                "media_count": 1000,
                "biography": "Fashion influencer in Seoul",
                "media": {
                    "data": [
                        {
                            "id": "im1",
                            "caption": "OOTD #fashion #minimal",
                            "comments_count": 50,
                            "like_count": 1000,
                            "media_type": "IMAGE",
                            "permalink": "https://ig/im1",
                            "timestamp": now.isoformat() + "Z",
                        },
                        {
                            "id": "im2",
                            "caption": "Eco vibes #sustainable #green",
                            "comments_count": 20,
                            "like_count": 600,
                            "media_type": "IMAGE",
                            "permalink": "https://ig/im2",
                            "timestamp": (now - timedelta(days=2)).isoformat() + "Z",
                        },
                    ]
                },
            }
        )

    async def get_profile_with_cache(self, username: str, media_limit: int = 20, use_cache: bool = True) -> InstagramProfile:
        if username == "brandx":
            return self.brand_profile
        return self.influencer_profile


def test_orchestrator_pipeline() -> None:
    fake_ig = FakeInstagramService()

    async def run() -> Dict[str, Any]:
        # db 세션은 orchestrator 내에서 사용하지 않으므로, 더미 객체 전달
        class DummySession(AsyncSession):
            pass

        orch = AnalysisOrchestrator(fake_ig, db_session=None)  # type: ignore
        brand = await orch.analyze_brand("brandx")
        infl = await orch.analyze_influencer("influencer_a", brand)
        return {"brand": brand, "influencer": infl}

    import asyncio

    data = asyncio.run(run())
    infl = data["influencer"]
    # 핵심 필드 확인
    assert infl["username"] == "influencer_a"
    assert "scores" in infl and "final_score" in infl["scores"]
    assert infl["avg_engagement_rate"] is not None
    assert 0 <= infl["scores"]["final_score"] <= 100


if __name__ == "__main__":
    print("[SMOKE] FastAPI health...")
    test_fastapi_health()
    print("[OK] Health endpoints")

    print("[SMOKE] Orchestrator pipeline...")
    test_orchestrator_pipeline()
    print("[OK] Orchestrator")

    print("All smoke tests passed.")

