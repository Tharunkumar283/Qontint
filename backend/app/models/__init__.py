"""
SQLAlchemy ORM Models for SERP data, Content, Predictions, and Entities.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, JSON, Boolean
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class SerpResult(Base):
    """Stores scraped SERP results from search engines."""
    __tablename__ = "serp_results"

    id = Column(String, primary_key=True, default=generate_uuid)
    keyword = Column(String(500), nullable=False, index=True)
    vertical = Column(String(100), nullable=False, default="saas")
    position = Column(Integer, nullable=False)
    url = Column(Text, nullable=False)
    title = Column(Text)
    snippet = Column(Text)
    content = Column(Text)
    content_hash = Column(String(64))
    metadata_ = Column("metadata", JSON)
    collected_at = Column(DateTime, default=datetime.utcnow)


class ContentDocument(Base):
    """User-generated content documents for analysis."""
    __tablename__ = "content_documents"

    id = Column(String, primary_key=True, default=generate_uuid)
    keyword = Column(String(500), nullable=False, index=True)
    vertical = Column(String(100), nullable=False, default="saas")
    title = Column(Text)
    content = Column(Text, nullable=False)
    intent_type = Column(String(50))
    status = Column(String(50), default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AnalysisResult(Base):
    """Stores analysis results for content documents."""
    __tablename__ = "analysis_results"

    id = Column(String, primary_key=True, default=generate_uuid)
    content_id = Column(String, nullable=True)
    keyword = Column(String(500), nullable=False)
    novelty_score = Column(Float, default=0.0)
    entity_novelty = Column(Float, default=0.0)
    relationship_novelty = Column(Float, default=0.0)
    semantic_diversity = Column(Float, default=0.0)
    predicted_rank = Column(Integer)
    confidence_score = Column(Float, default=0.0)
    intent_alignment = Column(Float, default=0.0)
    intent_type = Column(String(50))
    entity_coverage = Column(Float, default=0.0)
    relationship_completeness = Column(Float, default=0.0)
    authority_score = Column(Float, default=0.0)
    content_quality = Column(Float, default=0.0)
    pass_fail = Column(String(10), default="PENDING")
    recommendations = Column(JSON)
    entities_found = Column(JSON)
    missing_entities = Column(JSON)
    analyzed_at = Column(DateTime, default=datetime.utcnow)


class EntityRecord(Base):
    """Extracted entities with authority scores."""
    __tablename__ = "entities"

    id = Column(String, primary_key=True, default=generate_uuid)
    keyword = Column(String(500), nullable=False, index=True)
    entity_text = Column(String(500), nullable=False)
    entity_type = Column(String(100))
    authority_score = Column(Float, default=0.0)
    frequency = Column(Integer, default=1)
    source = Column(String(50), default="serp")
    vertical = Column(String(100), default="saas")
    metadata_ = Column("metadata", JSON)


class PredictionRecord(Base):
    """Historical ranking predictions for model evaluation."""
    __tablename__ = "predictions"

    id = Column(String, primary_key=True, default=generate_uuid)
    keyword = Column(String(500), nullable=False)
    content_hash = Column(String(64))
    predicted_position = Column(Integer)
    confidence = Column(Float)
    entity_coverage = Column(Float)
    relationship_completeness = Column(Float)
    authority_score = Column(Float)
    content_quality = Column(Float)
    features = Column(JSON)
    predicted_at = Column(DateTime, default=datetime.utcnow)
