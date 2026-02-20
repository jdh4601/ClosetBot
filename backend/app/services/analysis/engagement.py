"""Engagement rate calculation and analysis"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import structlog

logger = structlog.get_logger()


@dataclass
class EngagementMetrics:
    """Engagement metrics for an influencer"""

    avg_engagement_rate: float
    avg_likes: float
    avg_comments: float
    total_posts_analyzed: int

    # Percentile within follower tier
    tier_percentile: Optional[float] = None

    # Quality score (0-100)
    quality_score: Optional[float] = None


class EngagementCalculator:
    """Calculate engagement rates and quality scores"""

    # Follower tiers
    TIERS = {
        "nano": (1_000, 10_000),
        "micro": (10_000, 50_000),
        "mid": (50_000, 200_000),
        "macro": (200_000, float("inf")),
    }

    # Benchmark engagement rates by tier (based on industry standards)
    BENCHMARKS = {
        "nano": {"low": 3.0, "avg": 5.0, "high": 8.0},
        "micro": {"low": 2.0, "avg": 3.5, "high": 6.0},
        "mid": {"low": 1.5, "avg": 2.5, "high": 4.0},
        "macro": {"low": 1.0, "avg": 1.8, "high": 3.0},
    }

    @staticmethod
    def calculate_engagement_rate(likes: int, comments: int, followers: int) -> float:
        """
        Calculate engagement rate for a single post.

        Args:
            likes: Number of likes
            comments: Number of comments
            followers: Total followers

        Returns:
            Engagement rate as percentage (e.g., 5.2 for 5.2%)
        """
        if followers == 0:
            return 0.0

        # Use comments as engagement if likes not available (Business Discovery limitation)
        total_engagement = (
            likes if likes is not None else comments * 3
        )  # Estimate: 1 comment ≈ 3 likes

        rate = (total_engagement / followers) * 100
        return round(rate, 2)

    @classmethod
    def calculate_average_metrics(
        cls, posts: List[Dict], followers: int
    ) -> EngagementMetrics:
        """
        Calculate average engagement metrics from a list of posts.

        Args:
            posts: List of post dicts with 'likes_count' and 'comments_count'
            followers: Total follower count

        Returns:
            EngagementMetrics object
        """
        if not posts:
            return EngagementMetrics(
                avg_engagement_rate=0.0,
                avg_likes=0.0,
                avg_comments=0.0,
                total_posts_analyzed=0,
            )

        rates = []
        likes_list = []
        comments_list = []

        for post in posts:
            likes = post.get("likes_count") or 0
            comments = post.get("comments_count") or 0

            rate = cls.calculate_engagement_rate(likes, comments, followers)
            rates.append(rate)
            likes_list.append(likes)
            comments_list.append(comments)

        avg_rate = sum(rates) / len(rates)
        avg_likes = sum(likes_list) / len(likes_list)
        avg_comments = sum(comments_list) / len(comments_list)

        return EngagementMetrics(
            avg_engagement_rate=round(avg_rate, 2),
            avg_likes=round(avg_likes, 0),
            avg_comments=round(avg_comments, 0),
            total_posts_analyzed=len(posts),
        )

    @classmethod
    def get_follower_tier(cls, followers: int) -> str:
        """
        Get follower tier based on count.

        Returns:
            Tier name: 'nano', 'micro', 'mid', 'macro'
        """
        for tier, (min_f, max_f) in cls.TIERS.items():
            if min_f <= followers < max_f:
                return tier
        return "nano"  # Default for < 1K

    @classmethod
    def calculate_tier_percentile(cls, engagement_rate: float, followers: int) -> float:
        """
        Calculate percentile within follower tier.

        Returns:
            Percentile (0-100) where 50 is average
        """
        tier = cls.get_follower_tier(followers)
        benchmark = cls.BENCHMARKS[tier]

        low = benchmark["low"]
        avg = benchmark["avg"]
        high = benchmark["high"]

        # Calculate percentile based on engagement rate
        if engagement_rate <= low:
            # Below low: 0-25th percentile
            percentile = (engagement_rate / low) * 25
        elif engagement_rate <= avg:
            # Between low and avg: 25-50th percentile
            percentile = 25 + ((engagement_rate - low) / (avg - low)) * 25
        elif engagement_rate <= high:
            # Between avg and high: 50-75th percentile
            percentile = 50 + ((engagement_rate - avg) / (high - avg)) * 25
        else:
            # Above high: 75-100th percentile (capped at 100)
            excess = engagement_rate - high
            percentile = min(100, 75 + (excess / high) * 25)

        return round(percentile, 1)

    @classmethod
    def calculate_quality_score(cls, engagement_rate: float, followers: int) -> float:
        """
        Calculate engagement quality score (0-100).

        Based on:
        - Engagement rate relative to follower tier
        - Tier percentile

        Returns:
            Quality score 0-100
        """
        tier = cls.get_follower_tier(followers)
        benchmark = cls.BENCHMARKS[tier]

        # Base score from engagement rate
        if engagement_rate >= benchmark["high"]:
            base_score = 90
        elif engagement_rate >= benchmark["avg"]:
            # Interpolate between 60-90
            ratio = (engagement_rate - benchmark["avg"]) / (
                benchmark["high"] - benchmark["avg"]
            )
            base_score = 60 + (ratio * 30)
        elif engagement_rate >= benchmark["low"]:
            # Interpolate between 30-60
            ratio = (engagement_rate - benchmark["low"]) / (
                benchmark["avg"] - benchmark["low"]
            )
            base_score = 30 + (ratio * 30)
        else:
            # Below low: 0-30
            ratio = min(1.0, engagement_rate / benchmark["low"])
            base_score = ratio * 30

        # Add small bonus for consistency (can be calculated from variance)
        # For now, just round
        score = round(base_score, 0)
        return min(100, max(0, score))

    @classmethod
    def analyze_engagement(cls, posts: List[Dict], followers: int) -> EngagementMetrics:
        """
        Full engagement analysis with tier percentile and quality score.

        Args:
            posts: List of posts with engagement data
            followers: Total follower count

        Returns:
            Complete EngagementMetrics
        """
        metrics = cls.calculate_average_metrics(posts, followers)

        # Calculate tier percentile
        metrics.tier_percentile = cls.calculate_tier_percentile(
            metrics.avg_engagement_rate, followers
        )

        # Calculate quality score
        metrics.quality_score = cls.calculate_quality_score(
            metrics.avg_engagement_rate, followers
        )

        return metrics

    @classmethod
    def get_top_posts(cls, posts: List[Dict], followers: int, n: int = 3) -> List[Dict]:
        """
        Get top N posts by engagement rate.

        Args:
            posts: List of posts
            followers: Total followers
            n: Number of top posts to return

        Returns:
            Top N posts sorted by engagement rate
        """
        # Calculate engagement rate for each post
        posts_with_rate = []
        for post in posts:
            likes = post.get("likes_count") or 0
            comments = post.get("comments_count") or 0
            rate = cls.calculate_engagement_rate(likes, comments, followers)

            post_copy = post.copy()
            post_copy["engagement_rate"] = rate
            posts_with_rate.append(post_copy)

        # Sort by engagement rate descending
        posts_with_rate.sort(key=lambda x: x["engagement_rate"], reverse=True)

        return posts_with_rate[:n]
