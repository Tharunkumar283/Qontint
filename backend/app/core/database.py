"""
Database setup — supports SQLite (default) and PostgreSQL.
Also defines all ORM models: User, SerpResult, AnalysisResult.
"""
import os
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, JSON
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from app.core import settings


# ─── Engine ────────────────────────────────────────────────────────────────
# Supports both SQLite (zero-config) and PostgreSQL (production)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ─── Base ──────────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


# ─── Models ────────────────────────────────────────────────────────────────

class UserModel(Base):
    """User accounts for multi-tenant access."""
    __tablename__ = "users"

    email = Column(String(255), primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    password_hash = Column(String(64), nullable=False)
    plan = Column(String(50), default="starter")
    analyses_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    verticals = Column(JSON, default=lambda: ["saas"])
    is_active = Column(Boolean, default=True)


class SerpResultModel(Base):
    """Persisted SERP results for caching and re-analysis."""
    __tablename__ = "serp_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(500), index=True, nullable=False)
    vertical = Column(String(100), default="saas")
    position = Column(Integer)
    url = Column(Text)
    title = Column(Text)
    snippet = Column(Text)
    content = Column(Text)
    content_hash = Column(String(64), index=True)
    collected_at = Column(DateTime, default=datetime.utcnow)


class AnalysisResultModel(Base):
    """Persisted analysis results for history and comparison."""
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(500), index=True, nullable=False)
    vertical = Column(String(100), default="saas")
    user_email = Column(String(255), nullable=True)
    novelty_score = Column(Float, default=0.0)
    predicted_rank = Column(Integer, default=20)
    confidence_score = Column(Float, default=0.0)
    intent_alignment = Column(Float, default=0.0)
    entity_coverage = Column(Float, default=0.0)
    authority_score = Column(Float, default=0.0)
    content_quality = Column(Float, default=0.0)
    pass_fail = Column(String(10), default="PENDING")
    entities_found = Column(JSON, default=list)
    recommendations = Column(JSON, default=list)
    analyzed_at = Column(DateTime, default=datetime.utcnow)


class KnowledgeGraphModel(Base):
    """Persisted graph snapshots for Neo4j-less deployments."""
    __tablename__ = "knowledge_graphs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(500), index=True, unique=True)
    vertical = Column(String(100), default="saas")
    nodes_json = Column(JSON, default=list)
    edges_json = Column(JSON, default=list)
    node_count = Column(Integer, default=0)
    edge_count = Column(Integer, default=0)
    avg_authority = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ─── Session dependency ────────────────────────────────────────────────────

async def get_db() -> AsyncSession:
    """Dependency: yields an async database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ─── Init / close ──────────────────────────────────────────────────────────

async def init_db():
    """Create all database tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Dispose of the database engine on shutdown."""
    await engine.dispose()
