"""YouTube ranking prediction API endpoints."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services.youtube_analyzer import youtube_analyzer

router = APIRouter()


class YouTubeAnalyzeRequest(BaseModel):
    query: str
    vertical: Optional[str] = "saas"
    max_videos: Optional[int] = 10


class YouTubePredictRequest(BaseModel):
    title: str
    description: str
    tags: List[str] = []
    transcript_outline: str
    query: str
    vertical: Optional[str] = "saas"


@router.post("/youtube/analyze")
async def analyze_youtube(request: YouTubeAnalyzeRequest):
    """
    Analyze top YouTube videos for a query.
    Returns common topics, tags, benchmarks, and top videos.
    """
    result = await youtube_analyzer.analyze_query(
        query=request.query,
        vertical=request.vertical or "saas",
        max_videos=request.max_videos or 10,
    )
    return result


@router.post("/youtube/predict")
async def predict_youtube_performance(request: YouTubePredictRequest):
    """
    Predict how a planned video will perform on YouTube before publishing.
    Returns performance score, tier prediction, and recommendations.
    """
    result = await youtube_analyzer.predict_video_performance(
        title=request.title,
        description=request.description,
        tags=request.tags,
        transcript_outline=request.transcript_outline,
        query=request.query,
        vertical=request.vertical or "saas",
    )
    return result
