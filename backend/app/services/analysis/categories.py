"""Category taxonomy for fashion influencers"""

from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
import structlog

logger = structlog.get_logger()


@dataclass
class Category:
    """Fashion category definition"""

    slug: str
    name: str
    keywords: Set[str]
    weight: float = 1.0
    parent_slug: str = None


# Fashion category taxonomy
FASHION_CATEGORIES = {
    "minimal": Category(
        slug="minimal",
        name="미니멀",
        keywords={
            "minimal",
            "minimalism",
            "minimalist",
            "simple",
            "clean",
            "basic",
            "essentials",
            "classic",
            "neutral",
            "simplicity",
            "understated",
            "미니멀",
            "미니멀룩",
            "심플",
            "클린",
            "베이직",
            "미니멀리스트",
            "미니멀패션",
            "심플룩",
            "모던",
            "깔끔한",
            "단정한",
            "미니멀스타일",
        },
        weight=1.0,
    ),
    "streetwear": Category(
        slug="streetwear",
        name="스트리트",
        keywords={
            "streetwear",
            "street",
            "urban",
            "hiphop",
            "sneakers",
            "kicks",
            "hypebeast",
            "supreme",
            "nike",
            "adidas",
            "jordan",
            "yeezy",
            "오버핏",
            "스트릿",
            "스트리트",
            "힙합",
            "스니커즈",
            "스트릿패션",
            "스트리트패션",
            "오버사이즈",
            "레이어드",
            "힙한",
            "힙스터",
        },
        weight=1.0,
    ),
    "luxury": Category(
        slug="luxury",
        name="럭셔리",
        keywords={
            "luxury",
            "lux",
            "designer",
            "highfashion",
            "highend",
            "premium",
            "chanel",
            "gucci",
            "prada",
            "lv",
            "louisvuitton",
            "hermes",
            "럭셔리",
            "명품",
            "하이엔드",
            "디자이너",
            "명품패션",
            "고급스러운",
            "프리미엄",
            "럭셔리패션",
            "명품스타일",
            "우아한",
            "품격있는",
        },
        weight=1.0,
    ),
    "casual": Category(
        slug="casual",
        name="캐주얼",
        keywords={
            "casual",
            "daily",
            "everyday",
            "comfy",
            "comfortable",
            "relaxed",
            "weekend",
            "laidback",
            "effortless",
            "easy",
            "캐주얼",
            "데일리",
            "일상",
            "편안한",
            "편한",
            "캐주얼룩",
            "데일리룩",
            "일상룩",
            "편한옷",
            "캐주얼패션",
            "일상패션",
            "휴일룩",
        },
        weight=1.0,
    ),
    "vintage": Category(
        slug="vintage",
        name="빈티지",
        keywords={
            "vintage",
            "retro",
            "old-school",
            "secondhand",
            "thrifted",
            "thrift",
            "antique",
            "classic",
            "heritage",
            "oldschool",
            "빈티지",
            "레트로",
            "올드스쿨",
            "중고",
            "빈티지룩",
            "빈티지패션",
            "레트로룩",
            "레트로패션",
            "고전적인",
            "클래식",
            "옛날",
        },
        weight=1.0,
    ),
    "feminine": Category(
        slug="feminine",
        name="페미닌",
        keywords={
            "feminine",
            "girly",
            "romantic",
            "elegant",
            "graceful",
            "lovely",
            "chic",
            "dress",
            "skirt",
            "floral",
            "lace",
            "pink",
            "페미닌",
            "여성스러운",
            "로맨틱",
            "우아한",
            "귀여운",
            "러블리",
            "페미닌룩",
            "페미닌패션",
            "원피스",
            "치마",
            "레이스",
            "플로럴",
        },
        weight=1.0,
    ),
    "menswear": Category(
        slug="menswear",
        name="남성복",
        keywords={
            "menswear",
            "mensfashion",
            "menstyle",
            "dapper",
            "gentleman",
            "suit",
            "tailored",
            "formal",
            "business",
            "남성복",
            "남성패션",
            "남자패션",
            "맨즈웨어",
            "정장",
            "수트",
            "신사",
            "젠틀맨",
            "맨즈룩",
            "남친룩",
            "비즈니스룩",
            "정장룩",
        },
        weight=1.0,
    ),
    "sportswear": Category(
        slug="sportswear",
        name="스포츠웨어",
        keywords={
            "sportswear",
            "athleisure",
            "athletic",
            "gym",
            "workout",
            "fitness",
            "activewear",
            "running",
            "training",
            "sports",
            "yoga",
            "스포츠웨어",
            "애슬레저",
            "운동복",
            "헬스복",
            "요가복",
            "피트니스",
            "운동",
            "헬스",
            "러닝",
            "트레이닝",
            "홈트",
            "애슬레저룩",
        },
        weight=1.0,
    ),
    "bohemian": Category(
        slug="bohemian",
        name="보헤미안",
        keywords={
            "bohemian",
            "boho",
            "hippie",
            "ethnic",
            "tribal",
            "festival",
            "freespirit",
            "flowy",
            "maxi",
            "natural",
            "earthy",
            "보헤미안",
            "보호",
            "힙피",
            "에스닉",
            "자유로운",
            "페스티벌",
            "보헤미안룩",
            "보헤미안패션",
            "맥시",
            "자연스러운",
            "내추럴",
        },
        weight=1.0,
    ),
    "preppy": Category(
        slug="preppy",
        name="프레피",
        keywords={
            "preppy",
            "ivy",
            "college",
            "academic",
            "classic",
            "polo",
            "sweater",
            "blazer",
            "oxford",
            "loafer",
            "plaid",
            "tartan",
            "프레피",
            "아이비",
            "대학생",
            "아카데믹",
            "클래식",
            "폴로",
            "스웨터",
            "블레이저",
            "플레드",
            "체크",
            "학생룩",
            "캠퍼스룩",
        },
        weight=1.0,
    ),
}


class CategoryClassifier:
    """Classify content into fashion categories"""

    def __init__(self):
        self.categories = FASHION_CATEGORIES

    def classify(
        self, hashtags: List[str], keywords: List[str], min_score: float = 0.1
    ) -> List[Tuple[str, float]]:
        """
        Classify content into categories based on hashtags and keywords.

        Args:
            hashtags: List of hashtags
            keywords: List of keywords from captions
            min_score: Minimum score to include category

        Returns:
            List of (category_slug, score) tuples, sorted by score desc
        """
        # Combine hashtags and keywords for matching
        all_terms = set(h.lower() for h in hashtags) | set(k.lower() for k in keywords)

        scores = []
        for slug, category in self.categories.items():
            # Calculate score based on keyword overlap
            matching_keywords = all_terms & category.keywords

            if matching_keywords:
                # Score = (matching keywords / total category keywords) * weight
                score = (
                    len(matching_keywords) / len(category.keywords)
                ) * category.weight

                if score >= min_score:
                    scores.append((slug, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def get_primary_category(
        self, hashtags: List[str], keywords: List[str]
    ) -> Tuple[str, float]:
        """
        Get the primary (highest scoring) category.

        Returns:
            Tuple of (category_slug, score) or (None, 0) if no match
        """
        scores = self.classify(hashtags, keywords)
        if scores:
            return scores[0]
        return (None, 0.0)

    def get_category_match_score(
        self, brand_categories: List[str], influencer_categories: List[str]
    ) -> float:
        """
        Calculate match score between brand and influencer categories.

        Returns:
            Match score from 0.0 to 1.0
        """
        if not brand_categories or not influencer_categories:
            return 0.0

        brand_set = set(brand_categories)
        influencer_set = set(influencer_categories)

        # Calculate Jaccard similarity
        intersection = brand_set & influencer_set
        union = brand_set | influencer_set

        if not union:
            return 0.0

        return len(intersection) / len(union)

    def get_category_name(self, slug: str) -> str:
        """Get category display name"""
        category = self.categories.get(slug)
        return category.name if category else slug

    def get_all_categories(self) -> List[Dict]:
        """Get all category definitions"""
        return [
            {
                "slug": c.slug,
                "name": c.name,
                "weight": c.weight,
            }
            for c in self.categories.values()
        ]
