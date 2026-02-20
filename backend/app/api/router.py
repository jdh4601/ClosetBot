from fastapi import APIRouter

from app.api.endpoints import analysis, influencers, brands, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(
    influencers.router, prefix="/influencers", tags=["influencers"]
)
api_router.include_router(brands.router, prefix="/brands", tags=["brands"])
