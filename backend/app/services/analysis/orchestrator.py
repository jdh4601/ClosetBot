"""Analysis orchestrator - coordinates the entire analysis pipeline"""

from typing import List, Dict, Any
from datetime import datetime
import structlog

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.instagram import InstagramService
from app.services.analysis import (
    TextProcessor,
    CategoryClassifier,
    EngagementCalculator,
    WeightedJaccardSimilarity,
    ScoringEngine,
)

logger = structlog.get_logger()


class AnalysisOrchestrator:
    """
    Orchestrates the entire brand-influencer analysis pipeline.

    Pipeline steps:
    1. Fetch brand profile
    2. Extract brand hashtags/keywords
    3. Classify brand categories
    4. For each influencer:
       a. Fetch profile with cache
       b. Extract hashtags/keywords
       c. Classify categories
       d. Calculate engagement
       e. Detect collaborations
       f. Calculate similarity with brand
       g. Calculate final score
    5. Save results
    """

    def __init__(self, instagram_service: InstagramService, db_session: AsyncSession):
        self.instagram = instagram_service
        self.db = db_session
        self.text_processor = TextProcessor()
        self.category_classifier = CategoryClassifier()
        self.engagement_calculator = EngagementCalculator()
        self.similarity_calculator = WeightedJaccardSimilarity()
        self.scoring_engine = ScoringEngine()

    async def analyze_brand(self, username: str) -> Dict[str, Any]:
        """
        Analyze a brand's Instagram profile.

        Returns:
            Dict with brand analysis data
        """
        logger.info("Analyzing brand", username=username)

        # Fetch brand profile
        profile = await self.instagram.get_profile_with_cache(
            username, media_limit=20, use_cache=True
        )

        # Extract hashtags from all captions
        all_hashtags = []
        all_keywords = []
        captions = []

        for media in profile.media:
            if media.caption:
                hashtags = self.text_processor.extract_hashtags(media.caption)
                keywords = self.text_processor.extract_keywords(media.caption)

                all_hashtags.extend(hashtags)
                all_keywords.extend(keywords)
                captions.append(media.caption)

        # Filter spam hashtags
        filtered_hashtags = self.text_processor.filter_hashtags(all_hashtags)

        # Get hashtag frequency
        hashtag_freq = self.text_processor.analyze_hashtag_frequency(
            filtered_hashtags, top_n=20
        )

        # Classify categories
        category_scores = self.category_classifier.classify(
            filtered_hashtags, all_keywords
        )
        categories = [slug for slug, _ in category_scores[:3]]  # Top 3 categories

        return {
            "username": profile.username,
            "followers_count": profile.followers_count,
            "media_count": profile.media_count,
            "biography": profile.biography,
            "categories": categories,
            "top_hashtags": [{"hashtag": h, "count": c} for h, c in hashtag_freq],
            "keywords": list(set(all_keywords))[:20],  # Top 20 unique keywords
            "hashtags": filtered_hashtags,
        }

    async def analyze_influencer(
        self, username: str, brand_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze an influencer and calculate fit score with brand.

        Args:
            username: Influencer Instagram username
            brand_data: Pre-analyzed brand data

        Returns:
            Dict with influencer analysis and scores
        """
        logger.info("Analyzing influencer", username=username)

        # Fetch influencer profile
        profile = await self.instagram.get_profile_with_cache(
            username, media_limit=20, use_cache=True
        )

        # Extract hashtags and keywords
        all_hashtags = []
        all_keywords = []
        captions = []
        posts_data = []

        for media in profile.media:
            if media.caption:
                hashtags = self.text_processor.extract_hashtags(media.caption)
                keywords = self.text_processor.extract_keywords(media.caption)

                all_hashtags.extend(hashtags)
                all_keywords.extend(keywords)
                captions.append(media.caption)

            posts_data.append(
                {
                    "id": media.id,
                    "caption": media.caption,
                    "comments_count": media.comments_count,
                    "like_count": media.like_count,
                    "permalink": media.permalink,
                    "posted_at": media.timestamp,
                }
            )

        # Filter hashtags
        filtered_hashtags = self.text_processor.filter_hashtags(all_hashtags)

        # Classify categories
        category_scores = self.category_classifier.classify(
            filtered_hashtags, all_keywords
        )
        categories = [slug for slug, _ in category_scores[:3]]

        # Calculate engagement
        engagement_metrics = self.engagement_calculator.analyze_engagement(
            posts_data, profile.followers_count
        )

        # Detect collaborations
        collab_signals = []
        for media in profile.media:
            if media.caption:
                signals = self.text_processor.detect_collaboration_signals(
                    media.caption
                )
                if signals["is_collaboration"]:
                    for mention in signals["mentions"]:
                        collab_signals.append(
                            {
                                "brand_username": mention,
                                "collaboration_type": signals["collaboration_type"]
                                or "mention",
                                "post_permalink": media.permalink,
                                "posted_at": media.timestamp,
                            }
                        )

        # Get top 3 posts by engagement
        top_posts = self.engagement_calculator.get_top_posts(
            posts_data, profile.followers_count, n=3
        )

        # Calculate similarity with brand
        similarity_result = self.similarity_calculator.calculate(
            brand_data["hashtags"],
            brand_data["keywords"],
            filtered_hashtags,
            all_keywords,
        )

        # Calculate category fit
        category_score = self.scoring_engine.calculate_category_score(
            brand_data["categories"], categories
        )

        # Calculate engagement quality score
        engagement_score = self.scoring_engine.calculate_engagement_score(
            engagement_metrics.avg_engagement_rate, profile.followers_count
        )

        # Calculate final score
        score_breakdown = self.scoring_engine.calculate_score(
            similarity_score=similarity_result["similarity_score"],
            engagement_score=engagement_score,
            category_score=category_score,
        )

        # Get hashtag distribution
        hashtag_dist = dict(
            self.text_processor.analyze_hashtag_frequency(filtered_hashtags, top_n=10)
        )

        return {
            "username": profile.username,
            "profile_picture_url": profile.profile_picture_url,
            "followers_count": profile.followers_count,
            "media_count": profile.media_count,
            "biography": profile.biography,
            "avg_engagement_rate": engagement_metrics.avg_engagement_rate,
            "scores": {
                "similarity_score": similarity_result["similarity_score"],
                "engagement_score": engagement_score,
                "category_score": category_score,
                "final_score": score_breakdown.final_score,
                "grade": score_breakdown.grade,
            },
            "categories": categories,
            "top_posts": top_posts,
            "collaboration_signals": collab_signals[:10],  # Limit to 10
            "hashtag_distribution": hashtag_dist,
            "common_hashtags_with_brand": similarity_result["common_hashtags"],
        }
