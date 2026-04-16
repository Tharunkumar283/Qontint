"""
Pydantic Schemas for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ─── Enums ────────────────────────────────────────────────────────────

class IntentType(str, Enum):
    INFORMATIONAL = "informational"
    TRANSACTIONAL = "transactional"
    NAVIGATIONAL = "navigational"
    COMMERCIAL = "commercial"


class Vertical(str, Enum):
    SAAS = "saas"
    MORTGAGE = "mortgage"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    LEGAL = "legal"


class PassFail(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    PENDING = "PENDING"


# ─── SERP Schemas ─────────────────────────────────────────────────────

class SerpCollectRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=500, description="Target keyword")
    vertical: Vertical = Field(default=Vertical.SAAS, description="Industry vertical")


class SerpResultResponse(BaseModel):
    position: int
    url: str
    title: Optional[str] = None
    snippet: Optional[str] = None
    content_length: Optional[int] = None


class SerpCollectResponse(BaseModel):
    keyword: str
    vertical: str
    total_results: int
    results: List[SerpResultResponse]
    collected_at: str


# ─── Entity Schemas ───────────────────────────────────────────────────

class EntityResponse(BaseModel):
    text: str
    type: str
    authority_score: float = 0.0
    frequency: int = 1


class RelationshipResponse(BaseModel):
    source: str
    target: str
    relationship: str
    weight: float = 0.0


# ─── Analysis Schemas ─────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    content: str = Field(..., min_length=10, description="Content to analyze")
    keyword: str = Field(..., min_length=1, max_length=500, description="Target keyword")
    vertical: Vertical = Field(default=Vertical.SAAS)


class AnalyzeResponse(BaseModel):
    keyword: str
    novelty_score: float
    entity_novelty: float
    relationship_novelty: float
    semantic_diversity: float
    predicted_rank: int
    confidence_score: float
    intent_alignment: float
    intent_type: str
    entity_coverage: float
    relationship_completeness: float
    authority_score: float
    content_quality: float
    pass_fail: str
    entities_found: List[EntityResponse]
    missing_entities: List[EntityResponse]
    recommendations: List[Dict[str, Any]]
    analyzed_at: str


# ─── Prediction Schemas ──────────────────────────────────────────────

class PredictRequest(BaseModel):
    content: str = Field(..., min_length=10)
    keyword: str = Field(..., min_length=1, max_length=500)
    vertical: Vertical = Field(default=Vertical.SAAS)


class FeatureBreakdown(BaseModel):
    entity_coverage: float
    relationship_completeness: float
    authority_score: float
    content_quality: float
    weights: Dict[str, float] = {
        "entity_coverage": 0.40,
        "relationship_completeness": 0.30,
        "authority_score": 0.20,
        "content_quality": 0.10,
    }


class PredictResponse(BaseModel):
    predicted_position: int
    confidence: float
    features: FeatureBreakdown
    pass_fail: str


# ─── Generation Schemas ──────────────────────────────────────────────

class GenerateRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=500)
    vertical: Vertical = Field(default=Vertical.SAAS)
    intent: IntentType = Field(default=IntentType.INFORMATIONAL)
    guidelines: Optional[str] = None
    use_authority_entities: bool = True


class GenerateResponse(BaseModel):
    content: str
    keyword: str
    intent: str
    entities_used: List[str]
    authority_entities: List[EntityResponse]
    estimated_novelty: float
    word_count: int


# ─── Recommendation Schemas ──────────────────────────────────────────

class RecommendRequest(BaseModel):
    content: str = Field(..., min_length=10)
    keyword: str = Field(..., min_length=1, max_length=500)
    vertical: Vertical = Field(default=Vertical.SAAS)


class RecommendationItem(BaseModel):
    entity: str
    entity_type: str
    authority_score: float
    relevance_score: float
    suggestion: str
    context: str


class RecommendResponse(BaseModel):
    keyword: str
    current_novelty: float
    recommendations: List[RecommendationItem]
    potential_novelty_gain: float


# ─── Graph Schemas ────────────────────────────────────────────────────

class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    authority: float = 0.0
    frequency: int = 1
    size: float = 10.0


class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: str
    weight: float = 1.0


class GraphStats(BaseModel):
    total_nodes: int
    total_edges: int
    avg_authority: float
    top_entities: List[EntityResponse]


class GraphResponse(BaseModel):
    keyword: str
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    stats: GraphStats


# ─── Workflow Schemas ─────────────────────────────────────────────────

class WorkflowRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=500)
    vertical: Vertical = Field(default=Vertical.SAAS)
    intent: IntentType = Field(default=IntentType.INFORMATIONAL)
    guidelines: Optional[str] = None


class WorkflowStep(BaseModel):
    step: str
    status: str
    data: Optional[Dict[str, Any]] = None


class WorkflowResponse(BaseModel):
    keyword: str
    steps_completed: List[WorkflowStep]
    final_content: str
    final_analysis: AnalyzeResponse
    iterations: int
    total_time_seconds: float
