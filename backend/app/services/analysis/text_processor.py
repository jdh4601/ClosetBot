"""Text processing and hashtag extraction from captions"""

import re
from typing import List, Dict, Set, Tuple
from collections import Counter
import structlog

logger = structlog.get_logger()


# Korean stopwords and spam hashtags to filter
STOPWORDS = {
    # English
    "the",
    "be",
    "to",
    "of",
    "and",
    "a",
    "in",
    "that",
    "have",
    "i",
    "it",
    "for",
    "not",
    "on",
    "with",
    "he",
    "as",
    "you",
    "do",
    "at",
    "this",
    "but",
    "his",
    "by",
    "from",
    "they",
    "we",
    "say",
    "her",
    "she",
    "or",
    "an",
    "will",
    "my",
    "one",
    "all",
    "would",
    "there",
    "their",
    "what",
    "so",
    "up",
    "out",
    "if",
    "about",
    "who",
    "get",
    "which",
    "go",
    "me",
    "when",
    "make",
    "can",
    "like",
    "time",
    "no",
    "just",
    "him",
    "know",
    "take",
    "people",
    "into",
    "year",
    "your",
    "good",
    "some",
    "could",
    "them",
    "see",
    "other",
    "than",
    "then",
    "now",
    "look",
    "only",
    "come",
    "its",
    "over",
    "think",
    "also",
    "back",
    "after",
    "use",
    "two",
    "how",
    "our",
    "work",
    "first",
    "well",
    "way",
    "even",
    "new",
    "want",
    "because",
    "any",
    "these",
    "give",
    "day",
    "most",
    "us",
    "is",
    "was",
    "are",
    "were",
    "been",
    "has",
    "had",
    "did",
    "does",
    "doing",
    "done",
    "am",
    "being",
    "having",
    # Korean
    "은",
    "는",
    "이",
    "가",
    "을",
    "를",
    "의",
    "에",
    "에서",
    "로",
    "으로",
    "와",
    "과",
    "도",
    "만",
    "이나",
    "나",
    "부터",
    "까지",
    "에게",
    "한테",
    "께",
    "와",
    "과",
    "하고",
    "이랑",
    "랑",
    "으로서",
    "으로써",
    "같이",
    "처럼",
    "만큼",
    "보다",
    "더",
    "덜",
    "많이",
    "조금",
    "아주",
    "너무",
    "정말",
    "진짜",
    "그냥",
    "무척",
    "몹시",
    "매우",
    "상당히",
    "약간",
    "다",
    "좀",
    "한",
    "또",
    "그리고",
    "하지만",
    "그래서",
    "그러나",
    "그런데",
    "또는",
    "혹은",
    "아니면",
    "그러면",
    "그렇지만",
    "그러니까",
    "오늘",
    "내일",
    "어제",
    "지금",
    "방금",
    "곧",
    "나중에",
    "먼저",
    "항상",
    "자주",
    "가끔",
    "때때로",
    "전혀",
    "결코",
    "절대",
}

# Spam/low-quality hashtags to filter
SPAM_HASHTAGS = {
    "fff",
    "f4f",
    "follow4follow",
    "followforfollow",
    "l4l",
    "like4like",
    "likeforlike",
    "tagsforlikes",
    "tflers",
    "followme",
    "followback",
    "pleasefollow",
    "follow4followback",
    "teamfollowback",
    "followall",
    "instafollow",
    "followher",
    "followhim",
    "followforlike",
    "likeback",
    "likes4likes",
    "likesforlikes",
    "spam",
    "spam4spam",
    "recent4recent",
    "r4r",
    "likebackteam",
    "followbackteam",
    " gaintrain",
    "gainpost",
    "sdv",
    "seguidores",
    "followtrick",
    "chuvadelikes",
    "chuvadeseguidores",
    "followmenow",
    "followstagram",
    "followplease",
    "follow4like",
    "instalike",
    "likealways",
    "liketeam",
    "likeall",
    "likebackalways",
    "likeplease",
    "liking",
    "liker",
    "liked",
    "likes",
    "likeme",
}


class TextProcessor:
    """Process captions and extract hashtags/keywords"""

    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """
        Extract hashtags from text.

        Returns:
            List of hashtags (without # symbol, lowercase)
        """
        if not text:
            return []

        # Find all hashtags
        hashtags = re.findall(r"#(\w+)", text)

        # Normalize: lowercase and filter empty
        hashtags = [tag.lower().strip() for tag in hashtags if tag.strip()]

        logger.debug("Extracted hashtags", count=len(hashtags))
        return hashtags

    @staticmethod
    def extract_mentions(text: str) -> List[str]:
        """
        Extract @mentions from text.

        Returns:
            List of usernames (without @ symbol, lowercase)
        """
        if not text:
            return []

        mentions = re.findall(r"@(\w+)", text)
        return [m.lower().strip() for m in mentions if m.strip()]

    @staticmethod
    def extract_keywords(text: str, min_length: int = 2) -> List[str]:
        """
        Extract keywords from text (excluding hashtags and mentions).

        Args:
            text: Input text
            min_length: Minimum keyword length

        Returns:
            List of keywords
        """
        if not text:
            return []

        # Remove hashtags and mentions
        text = re.sub(r"#\w+", "", text)
        text = re.sub(r"@\w+", "", text)

        # Remove URLs
        text = re.sub(r"http[s]?://\S+", "", text)

        # Extract words
        words = re.findall(r"\b[a-zA-Z가-힣]+\b", text)

        # Filter: lowercase, min length, not stopword
        keywords = [
            word.lower()
            for word in words
            if len(word) >= min_length and word.lower() not in STOPWORDS
        ]

        return keywords

    @staticmethod
    def filter_hashtags(
        hashtags: List[str], min_length: int = 2, remove_spam: bool = True
    ) -> List[str]:
        """
        Filter hashtags to remove spam and low-quality tags.

        Args:
            hashtags: List of hashtags (without #)
            min_length: Minimum hashtag length
            remove_spam: Whether to remove known spam tags

        Returns:
            Filtered list of hashtags
        """
        filtered = []

        for tag in hashtags:
            # Skip short tags
            if len(tag) < min_length:
                continue

            # Skip spam tags
            if remove_spam and tag in SPAM_HASHTAGS:
                continue

            # Skip pure numeric tags
            if tag.isdigit():
                continue

            filtered.append(tag)

        return filtered

    @staticmethod
    def analyze_hashtag_frequency(
        hashtags: List[str], top_n: int = 20
    ) -> List[Tuple[str, int]]:
        """
        Analyze hashtag frequency.

        Returns:
            List of (hashtag, count) tuples, sorted by count desc
        """
        counter = Counter(hashtags)
        return counter.most_common(top_n)

    @staticmethod
    def detect_collaboration_signals(text: str) -> Dict[str, any]:
        """
        Detect collaboration indicators in text.

        Returns:
            Dict with collaboration signals
        """
        text_lower = text.lower()

        # Collaboration hashtags
        collab_tags = [
            "ad",
            "sponsored",
            "partner",
            "partnership",
            "collab",
            "협찬",
            "광고",
            "제품제공",
            "파트너십",
            "협업",
            "유료광고",
            "gifted",
            "pr",
            "review",
            "리뷰",
            "내돈내산",
        ]

        found_tags = []
        for tag in collab_tags:
            if f"#{tag}" in text_lower:
                found_tags.append(tag)

        # Check for mention patterns
        mentions = TextProcessor.extract_mentions(text)

        # Determine collaboration type
        collab_type = None
        if any(
            t
            in [
                "ad",
                "sponsored",
                "partner",
                "partnership",
                "광고",
                "유료광고",
                "파트너십",
            ]
            for t in found_tags
        ):
            collab_type = "paid"
        elif any(
            t in ["gifted", "pr", "제품제공", "review", "리뷰"] for t in found_tags
        ):
            collab_type = "gifted"
        elif any(t in ["collab", "협찬", "협업"] for t in found_tags):
            collab_type = "collab"

        return {
            "is_collaboration": len(found_tags) > 0 or len(mentions) > 0,
            "collaboration_type": collab_type,
            "collab_hashtags": found_tags,
            "mentions": mentions,
        }
