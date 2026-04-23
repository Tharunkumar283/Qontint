"""
YouTube Ranking Prediction — Analyzes YouTube videos for a query,
extracts transcript entities, scores content patterns, and predicts
video performance before publishing.
"""
import logging
import hashlib
from typing import List, Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Mock top-performing video data for demo/fallback
MOCK_YOUTUBE_DATA = {
    "best mortgage rates": [
        {
            "video_id": "demo_001",
            "title": "Best Mortgage Rates 2025 — How to Get the Lowest Rate",
            "channel": "Mortgage Expert",
            "views": 485000,
            "likes": 12300,
            "duration_seconds": 845,
            "transcript_excerpt": "Today we're covering the best mortgage rates available in 2025. The Federal Reserve's recent decisions have significantly impacted 30-year fixed rates. Understanding APR versus interest rate is critical when shopping lenders. Your credit score, LTV ratio, and debt-to-income ratio all determine your final rate.",
            "tags": ["mortgage rates", "30-year fixed", "refinance", "interest rates", "home buying"],
            "engagement_rate": 0.87,
        },
        {
            "video_id": "demo_002",
            "title": "FHA vs Conventional Mortgage — Which is Better in 2025?",
            "channel": "Home Finance Academy",
            "views": 312000,
            "likes": 8900,
            "duration_seconds": 720,
            "transcript_excerpt": "FHA loans require a minimum 3.5% down payment with a 580 credit score. Conventional loans offer better rates with 20% down and eliminate PMI. Understanding mortgage insurance, closing costs, and rate locks will save you thousands. The debt-to-income ratio is your most important qualification metric.",
            "tags": ["FHA loan", "conventional mortgage", "down payment", "PMI", "mortgage comparison"],
            "engagement_rate": 0.83,
        },
    ],
    "default": [
        {
            "video_id": "demo_default_001",
            "title": "Complete Guide to {keyword} — Everything You Need to Know in 2025",
            "channel": "Expert Channel",
            "views": 250000,
            "likes": 7500,
            "duration_seconds": 660,
            "transcript_excerpt": "In this comprehensive video, we cover the essential aspects of {keyword}. We'll walk through the key concepts, strategies, and practical tips that top performers use. Understanding these fundamentals will give you a significant advantage.",
            "tags": ["{keyword}", "guide", "tutorial", "2025", "explained"],
            "engagement_rate": 0.78,
        },
    ],
}


class YouTubeAnalyzer:
    """
    Analyzes YouTube video performance and predicts ranking potential.
    Uses YouTube Data API v3 when available; falls back to mock data.
    Extracts transcript entities and patterns from top-performing videos.
    """

    def __init__(self):
        self._api_key: Optional[str] = None
        self._cache: Dict[str, Any] = {}

    def configure(self, api_key: Optional[str] = None):
        """Set YouTube Data API key."""
        self._api_key = api_key

    async def analyze_query(
        self,
        query: str,
        vertical: str = "saas",
        max_videos: int = 10,
    ) -> Dict:
        """
        Analyze top YouTube videos for a query.
        Returns video data, common topics, entity patterns, and content gaps.
        """
        cache_key = f"yt:{query}:{vertical}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Try live YouTube API
        videos = []
        if self._api_key:
            try:
                videos = await self._fetch_live_videos(query, max_videos)
            except Exception as e:
                logger.warning(f"YouTube API failed: {e}. Using mock data.")

        if not videos:
            videos = self._get_mock_videos(query)

        # Analyze the videos
        analysis = self._analyze_videos(query, videos)
        self._cache[cache_key] = analysis
        return analysis

    async def _fetch_live_videos(self, query: str, max_results: int) -> List[Dict]:
        """Fetch top videos from YouTube Data API v3."""
        import httpx
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "order": "relevance",
            "maxResults": max_results,
            "key": self._api_key,
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code != 200:
                raise Exception(f"YouTube API error: {resp.status_code}")
            data = resp.json()

        videos = []
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            video_id = item.get("id", {}).get("videoId", "")
            videos.append({
                "video_id": video_id,
                "title": snippet.get("title", ""),
                "channel": snippet.get("channelTitle", ""),
                "description": snippet.get("description", ""),
                "views": 0,  # Requires second API call for stats
                "likes": 0,
                "tags": [],
                "transcript_excerpt": snippet.get("description", ""),
                "engagement_rate": 0.75,
            })
        return videos

    def _get_mock_videos(self, query: str) -> List[Dict]:
        """Return mock video data."""
        query_lower = query.lower()
        for key, videos in MOCK_YOUTUBE_DATA.items():
            if key == "default":
                continue
            if any(word in query_lower for word in key.split()):
                return videos

        # Use default with substitution
        defaults = []
        for v in MOCK_YOUTUBE_DATA["default"]:
            defaults.append({
                **v,
                "title": v["title"].replace("{keyword}", query),
                "transcript_excerpt": v["transcript_excerpt"].replace("{keyword}", query),
                "tags": [t.replace("{keyword}", query) for t in v["tags"]],
            })
        return defaults

    def _analyze_videos(self, query: str, videos: List[Dict]) -> Dict:
        """Extract patterns, entities, and insights from top videos."""
        # Common tags across top videos
        all_tags: Dict[str, int] = {}
        for v in videos:
            for tag in v.get("tags", []):
                all_tags[tag] = all_tags.get(tag, 0) + 1

        top_tags = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)[:15]

        # Extract entities from transcripts
        all_words: Dict[str, int] = {}
        for v in videos:
            transcript = v.get("transcript_excerpt", "")
            words = transcript.lower().split()
            for word in words:
                if len(word) > 4 and word.isalpha():
                    all_words[word] = all_words.get(word, 0) + 1

        common_topics = sorted(all_words.items(), key=lambda x: x[1], reverse=True)[:20]

        # Calculate average engagement
        avg_engagement = sum(v.get("engagement_rate", 0.7) for v in videos) / max(len(videos), 1)
        avg_views = int(sum(v.get("views", 0) for v in videos) / max(len(videos), 1))
        avg_duration = int(sum(v.get("duration_seconds", 600) for v in videos) / max(len(videos), 1))

        # Content patterns
        avg_title_length = sum(len(v.get("title", "").split()) for v in videos) / max(len(videos), 1)

        return {
            "query": query,
            "videos_analyzed": len(videos),
            "top_videos": videos[:5],
            "common_topics": [{"term": t, "frequency": f} for t, f in common_topics[:10]],
            "top_tags": [{"tag": t, "count": c} for t, c in top_tags],
            "benchmarks": {
                "avg_engagement_rate": round(avg_engagement, 3),
                "avg_views": avg_views,
                "avg_duration_seconds": avg_duration,
                "avg_title_word_count": round(avg_title_length, 1),
                "optimal_duration_range": "8-15 minutes",
                "optimal_title_length": "8-12 words",
            },
            "analyzed_at": datetime.utcnow().isoformat(),
        }

    async def predict_video_performance(
        self,
        title: str,
        description: str,
        tags: List[str],
        transcript_outline: str,
        query: str,
        vertical: str = "saas",
    ) -> Dict:
        """
        Predict how a planned video will perform on YouTube before publishing.
        Returns performance score, gap analysis, and recommendations.
        """
        # Get reference data for the query
        reference = await self.analyze_query(query, vertical)

        # Score different dimensions
        scores = {}

        # 1. Title optimization (0-1)
        title_words = title.lower().split()
        query_words = set(query.lower().split())
        title_keyword_coverage = len(set(title_words) & query_words) / max(len(query_words), 1)
        title_length_score = 1.0 if 8 <= len(title_words) <= 12 else max(0.3, 1 - abs(len(title_words) - 10) * 0.08)
        scores["title_optimization"] = round((title_keyword_coverage * 0.6 + title_length_score * 0.4), 3)

        # 2. Tag coverage (0-1)
        top_tags_set = {t["tag"].lower() for t in reference.get("top_tags", [])}
        user_tags_set = {t.lower() for t in tags}
        tag_overlap = len(user_tags_set & top_tags_set) / max(len(top_tags_set), 1)
        scores["tag_coverage"] = round(min(tag_overlap * 2, 1.0), 3)  # Normalize

        # 3. Content depth (based on transcript outline)
        common_topics = {t["term"] for t in reference.get("common_topics", [])}
        outline_words = set(transcript_outline.lower().split())
        topic_coverage = len(outline_words & common_topics) / max(len(common_topics), 1)
        depth_score = min(len(transcript_outline.split()) / 500, 1.0)  # More outline = more depth
        scores["content_depth"] = round((topic_coverage * 0.6 + depth_score * 0.4), 3)

        # 4. Description quality (0-1)
        desc_length_score = min(len(description.split()) / 200, 1.0)
        desc_keyword_coverage = len(set(description.lower().split()) & query_words) / max(len(query_words), 1)
        scores["description_quality"] = round((desc_length_score * 0.4 + desc_keyword_coverage * 0.6), 3)

        # Overall performance score (weighted)
        overall = (
            scores["title_optimization"] * 0.35 +
            scores["tag_coverage"] * 0.20 +
            scores["content_depth"] * 0.30 +
            scores["description_quality"] * 0.15
        )
        scores["overall"] = round(overall, 3)

        # Predicted ranking tier
        if overall >= 0.80:
            predicted_tier = "Top 5"
            predicted_percentile = 95
        elif overall >= 0.65:
            predicted_tier = "Top 20"
            predicted_percentile = 80
        elif overall >= 0.50:
            predicted_tier = "Top 50"
            predicted_percentile = 65
        elif overall >= 0.35:
            predicted_tier = "Top 100"
            predicted_percentile = 45
        else:
            predicted_tier = "Below Top 100"
            predicted_percentile = 25

        # Generate recommendations
        recommendations = []
        missing_tags = list(top_tags_set - user_tags_set)[:5]
        if missing_tags:
            recommendations.append({
                "type": "tags",
                "priority": "HIGH",
                "suggestion": f"Add these high-performing tags: {', '.join(missing_tags)}",
                "impact": "+0.12 score",
            })

        missing_topics = list(common_topics - outline_words)[:3]
        if missing_topics:
            recommendations.append({
                "type": "content",
                "priority": "HIGH",
                "suggestion": f"Cover these topics found in top videos: {', '.join(missing_topics)}",
                "impact": "+0.15 score",
            })

        if scores["title_optimization"] < 0.6:
            recommendations.append({
                "type": "title",
                "priority": "MEDIUM",
                "suggestion": f"Include query keywords in title. Target 8-12 words. Current query: '{query}'",
                "impact": "+0.10 score",
            })

        if scores["description_quality"] < 0.5:
            recommendations.append({
                "type": "description",
                "priority": "MEDIUM",
                "suggestion": "Write a 150-200 word description with keywords in the first 2 sentences.",
                "impact": "+0.08 score",
            })

        return {
            "query": query,
            "scores": scores,
            "predicted_tier": predicted_tier,
            "predicted_percentile": predicted_percentile,
            "pass_threshold": overall >= 0.55,
            "benchmarks": reference.get("benchmarks", {}),
            "recommendations": recommendations,
            "top_competing_videos": reference.get("top_videos", [])[:3],
            "analyzed_at": datetime.utcnow().isoformat(),
        }


# Singleton instance
youtube_analyzer = YouTubeAnalyzer()
