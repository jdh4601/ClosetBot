"""Scoring engine for brand-influencer matching"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import structlog

from app.services.analysis.engagement import EngagementCalculator

logger = structlog.get_logger()


@dataclass
class ScoreBreakdown:
    """Detailed scoring breakdown"""

    similarity_score: float  # 0-100
    engagement_score: float  # 0-100
    category_score: float  # 0-100
    final_score: float  # 0-100
    grade: str  # A, B, C, D

    # Component weights
    similarity_weight: float = 0.40
    engagement_weight: float = 0.35
    category_weight: float = 0.25


class ScoringEngine:
    """
    Calculate final fit score for brand-influencer matching.

    Score Components:
    - Brand Similarity: 40% (hashtags, keywords, tone)
    - Engagement Quality: 35% (rate relative to follower tier)
    - Category Fit: 25% (category overlap)

    Grade Scale:
    - A: 80-100 (Strongly Recommended)
    - B: 60-79 (Recommended)
    - C: 40-59 (Average)
    - D: 0-39 (Not Recommended)
    """

    GRADES = {
        "A": (80, 100, "강력 추천"),
        "B": (60, 79, "추천"),
        "C": (40, 59, "보통"),
        "D": (0, 39, "부적합"),
    }

    @classmethod
    def calculate_score(
        cls,
        similarity_score: float,
        engagement_score: float,
        category_score: float,
        similarity_weight: float = 0.40,
        engagement_weight: float = 0.35,
        category_weight: float = 0.25,
    ) -> ScoreBreakdown:
        """
        Calculate final weighted score.

        Args:
            similarity_score: Brand similarity (0-100)
            engagement_score: Engagement quality (0-100)
            category_score: Category fit (0-100)
            similarity_weight: Weight for similarity (default 0.40)
            engagement_weight: Weight for engagement (default 0.35)
            category_weight: Weight for category (default 0.25)

        Returns:
            ScoreBreakdown with final score and grade
        """
        # Validate weights sum to 1.0
        total_weight = similarity_weight + engagement_weight + category_weight
        if abs(total_weight - 1.0) > 0.01:
            logger.warning("Weights don't sum to 1.0, normalizing", total=total_weight)
            similarity_weight /= total_weight
            engagement_weight /= total_weight
            category_weight /= total_weight

        # Calculate weighted final score
        final_score = (
            similarity_score * similarity_weight
            + engagement_score * engagement_weight
            + category_score * category_weight
        )

        # Determine grade
        grade = cls._get_grade(final_score)

        return ScoreBreakdown(
            similarity_score=round(similarity_score, 1),
            engagement_score=round(engagement_score, 1),
            category_score=round(category_score, 1),
            final_score=round(final_score, 1),
            grade=grade,
            similarity_weight=similarity_weight,
            engagement_weight=engagement_weight,
            category_weight=category_weight,
        )

    @classmethod
    def _get_grade(cls, score: float) -> str:
        """
        Determine grade from score.

        Returns:
            Grade: A, B, C, or D
        """
        for grade, (min_score, max_score, _) in cls.GRADES.items():
            if min_score <= score <= max_score:
                return grade
        return "D"  # Default for invalid scores

    @classmethod
    def get_grade_description(cls, grade: str) -> str:
        """Get grade description in Korean"""
        return cls.GRADES.get(grade, (0, 0, "Unknown"))[2]

    @classmethod
    def calculate_engagement_score(
        cls, engagement_rate: float, followers: int
    ) -> float:
        """
        Calculate engagement quality score (0-100).

        Based on engagement rate relative to follower tier benchmarks.

        Args:
            engagement_rate: Average engagement rate (%)
            followers: Total follower count

        Returns:
            Engagement quality score 0-100
        """
        # Use the engagement calculator for consistency
        return EngagementCalculator.calculate_quality_score(engagement_rate, followers)

    @classmethod
    def calculate_category_score(
        cls, brand_categories: List[str], influencer_categories: List[str]
    ) -> float:
        """
        Calculate category fit score (0-100).

        Based on Jaccard similarity of category assignments.

        Args:
            brand_categories: List of brand category slugs
            influencer_categories: List of influencer category slugs

        Returns:
            Category fit score 0-100
        """
        if not brand_categories or not influencer_categories:
            return 50.0  # Neutral if no category data

        brand_set = set(brand_categories)
        influencer_set = set(influencer_categories)

        # Calculate Jaccard similarity
        intersection = len(brand_set & influencer_set)
        union = len(brand_set | influencer_set)

        if union == 0:
            return 0.0

        similarity = intersection / union
        return round(similarity * 100, 1)

    @classmethod
    def rank_influencers(
        cls, scores: List[ScoreBreakdown], min_grade: Optional[str] = None
    ) -> List[ScoreBreakdown]:
        """
        Rank influencers by final score.

        Args:
            scores: List of ScoreBreakdown objects
            min_grade: Minimum grade to include (e.g., "B" includes A and B)

        Returns:
            Sorted list (highest score first)
        """
        # Filter by minimum grade if specified
        if min_grade:
            min_threshold = cls.GRADES.get(min_grade, (0, 100, ""))[0]
            scores = [s for s in scores if s.final_score >= min_threshold]

        # Sort by final score descending
        return sorted(scores, key=lambda x: x.final_score, reverse=True)

    @classmethod
    def get_recommendation(cls, score: ScoreBreakdown) -> Dict[str, str]:
        """
        Get human-readable recommendation based on score.

        Returns:
            Dict with recommendation details
        """
        grade_desc = cls.get_grade_description(score.grade)

        recommendations = {
            "A": {
                "summary": f"{grade_desc} - 이 인플루언서는 브랜드와 매우 잘 맞습니다",
                "action": "우선적으로 컨택하세요",
                "details": "높은 유사도와 우수한 참여율을 보유하고 있습니다.",
            },
            "B": {
                "summary": f"{grade_desc} - 좋은 매칭입니다",
                "action": "컨택을 고려하세요",
                "details": "전반적으로 브랜드와 잘 어울리며 긍정적인 결과를 기대할 수 있습니다.",
            },
            "C": {
                "summary": f"{grade_desc} - 보통 수준의 매칭입니다",
                "action": "추가 검토가 필요합니다",
                "details": "일부 측면에서 매칭이 되지만 개선의 여지가 있습니다.",
            },
            "D": {
                "summary": f"{grade_desc} - 적합하지 않은 매칭입니다",
                "action": "컨택을 권장하지 않습니다",
                "details": "브랜드와의 적합도가 낮거나 참여율이 부족합니다.",
            },
        }

        return recommendations.get(score.grade, recommendations["D"])
