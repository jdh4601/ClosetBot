"""Weighted Jaccard similarity algorithm for brand-influencer matching"""

from typing import List, Dict, Set, Tuple
from collections import Counter
import structlog

logger = structlog.get_logger()


class WeightedJaccardSimilarity:
    """
    Calculate weighted Jaccard similarity between brand and influencer.

    Weights:
    - Hashtags: 0.7 (higher weight - more specific)
    - Keywords: 0.3 (lower weight - more general)
    """

    HASHTAG_WEIGHT = 0.7
    KEYWORD_WEIGHT = 0.3

    @staticmethod
    def calculate(
        brand_hashtags: List[str],
        brand_keywords: List[str],
        influencer_hashtags: List[str],
        influencer_keywords: List[str],
        hashtag_weight: float = HASHTAG_WEIGHT,
        keyword_weight: float = KEYWORD_WEIGHT,
    ) -> Dict[str, any]:
        """
        Calculate weighted Jaccard similarity.

        Args:
            brand_hashtags: Brand's hashtags
            brand_keywords: Brand's keywords
            influencer_hashtags: Influencer's hashtags
            influencer_keywords: Influencer's keywords
            hashtag_weight: Weight for hashtag similarity (default 0.7)
            keyword_weight: Weight for keyword similarity (default 0.3)

        Returns:
            Dict with similarity score and details
        """
        # Normalize to sets
        brand_tags = set(h.lower() for h in brand_hashtags)
        brand_words = set(k.lower() for k in brand_keywords)
        inf_tags = set(h.lower() for h in influencer_hashtags)
        inf_words = set(k.lower() for k in influencer_keywords)

        # Calculate Jaccard for hashtags
        hashtag_similarity = WeightedJaccardSimilarity._jaccard(brand_tags, inf_tags)

        # Calculate Jaccard for keywords
        keyword_similarity = WeightedJaccardSimilarity._jaccard(brand_words, inf_words)

        # Calculate weighted average
        weighted_score = (
            hashtag_similarity * hashtag_weight + keyword_similarity * keyword_weight
        )

        # Find common elements
        common_hashtags = list(brand_tags & inf_tags)
        common_keywords = list(brand_words & inf_words)

        return {
            "similarity_score": round(weighted_score * 100, 1),  # Convert to 0-100
            "hashtag_similarity": round(hashtag_similarity * 100, 1),
            "keyword_similarity": round(keyword_similarity * 100, 1),
            "common_hashtags": common_hashtags,
            "common_keywords": common_keywords,
            "brand_hashtag_count": len(brand_tags),
            "influencer_hashtag_count": len(inf_tags),
            "overlap_hashtag_count": len(common_hashtags),
        }

    @staticmethod
    def _jaccard(set_a: Set[str], set_b: Set[str]) -> float:
        """
        Calculate Jaccard similarity coefficient.

        J(A, B) = |A ∩ B| / |A ∪ B|

        Returns:
            Similarity score between 0.0 and 1.0
        """
        if not set_a and not set_b:
            return 0.0

        intersection = len(set_a & set_b)
        union = len(set_a | set_b)

        if union == 0:
            return 0.0

        return intersection / union

    @staticmethod
    def calculate_weighted_with_tf_idf(
        brand_hashtags: List[str],
        influencer_hashtags: List[str],
        idf_scores: Dict[str, float],
    ) -> float:
        """
        Calculate TF-IDF weighted Jaccard similarity.

        Rare hashtags get higher weight in the calculation.

        Args:
            brand_hashtags: Brand's hashtags
            influencer_hashtags: Influencer's hashtags
            idf_scores: Inverse document frequency for each hashtag

        Returns:
            Weighted similarity score (0-100)
        """
        brand_counter = Counter(h.lower() for h in brand_hashtags)
        inf_counter = Counter(h.lower() for h in influencer_hashtags)

        # Get all unique hashtags
        all_tags = set(brand_counter.keys()) | set(inf_counter.keys())

        # Calculate weighted intersection and union
        weighted_intersection = 0.0
        weighted_union = 0.0

        for tag in all_tags:
            idf = idf_scores.get(tag, 1.0)  # Default IDF of 1.0
            brand_tf = brand_counter.get(tag, 0)
            inf_tf = inf_counter.get(tag, 0)

            # Weighted term frequency
            brand_weight = brand_tf * idf
            inf_weight = inf_tf * idf

            # Intersection: minimum weight
            weighted_intersection += min(brand_weight, inf_weight)

            # Union: maximum weight
            weighted_union += max(brand_weight, inf_weight)

        if weighted_union == 0:
            return 0.0

        similarity = weighted_intersection / weighted_union
        return round(similarity * 100, 1)

    @staticmethod
    def calculate_caption_tone_similarity(
        brand_captions: List[str], influencer_captions: List[str]
    ) -> float:
        """
        Calculate similarity in caption tone/style.

        Uses simple metrics like:
        - Average caption length
        - Emoji usage
        - Question frequency
        - Exclamation frequency

        Returns:
            Tone similarity score (0-100)
        """

        def analyze_tone(captions: List[str]) -> Dict:
            if not captions:
                return {"avg_length": 0, "emoji_ratio": 0, "question_ratio": 0}

            total_length = sum(len(c) for c in captions)
            emoji_count = sum(
                c.count("😀") + c.count("✨") + c.count("❤️") for c in captions
            )  # Simplified
            question_count = sum(c.count("?") + c.count("？") for c in captions)

            return {
                "avg_length": total_length / len(captions),
                "emoji_ratio": emoji_count / len(captions),
                "question_ratio": question_count / len(captions),
            }

        brand_tone = analyze_tone(brand_captions)
        inf_tone = analyze_tone(influencer_captions)

        # Calculate similarity for each metric
        if brand_tone["avg_length"] == 0 or inf_tone["avg_length"] == 0:
            return 50.0  # Neutral if no data

        # Normalize differences (0 = identical, 1 = completely different)
        length_diff = abs(brand_tone["avg_length"] - inf_tone["avg_length"]) / max(
            brand_tone["avg_length"], inf_tone["avg_length"]
        )
        emoji_diff = abs(brand_tone["emoji_ratio"] - inf_tone["emoji_ratio"])
        question_diff = abs(brand_tone["question_ratio"] - inf_tone["question_ratio"])

        # Average difference and convert to similarity
        avg_diff = (length_diff + emoji_diff + question_diff) / 3
        similarity = (1 - avg_diff) * 100

        return round(max(0, min(100, similarity)), 1)
