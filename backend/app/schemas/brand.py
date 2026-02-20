from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime


class BrandCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Brand Instagram username (without @)",
    )


class BrandProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    ig_username: str
    followers_count: int
    media_count: int
    biography: Optional[str]
    categories: List[str]
    top_hashtags: List[Dict[str, Any]]  # [{"hashtag": "fashion", "count": 15}, ...]
    keywords: List[str]
    last_fetched_at: datetime
