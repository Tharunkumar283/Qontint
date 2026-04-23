"""
╔═══════════════════════════════════════════════════════════════╗
║  QONTINT — Semantic Authority Operating System               ║
║  AI-Powered Content Ranking Prediction Platform              ║
║                                                               ║
║  Architecture: Intelligence FIRST, Generation SECOND          ║
║  Stack: FastAPI + spaCy + NetworkX + XGBoost + Claude API     ║
╚═══════════════════════════════════════════════════════════════╝
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core import settings
from app.core.database import init_db, close_db
from app.api.router import api_router
from app.services.cache_manager import cache_manager
from app.services.ml_trainer import ensure_model_exists, get_model_metadata
from app.services.youtube_analyzer import youtube_analyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s | %(name)-30s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("qontint")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle: startup and shutdown."""
    logger.info("═" * 60)
    logger.info("  QONTINT — Semantic Authority OS — Starting Up")
    logger.info("═" * 60)

    # Initialize database
    await init_db()
    logger.info("✓ Database initialized")

    # Initialize Redis cache
    await cache_manager.initialize(settings.REDIS_URL or None)
    logger.info(f"✓ Cache initialized ({cache_manager.backend})")

    # Configure YouTube analyzer
    if settings.YOUTUBE_API_KEY:
        youtube_analyzer.configure(api_key=settings.YOUTUBE_API_KEY)
        logger.info("✓ YouTube API configured")
    else:
        logger.info("  YouTube API key not set — using mock data")

    # Train ML model if not exists
    model_trained = await ensure_model_exists()
    if model_trained:
        meta = get_model_metadata()
        acc = meta.get("accuracy_within_2_positions", "?")
        logger.info(f"✓ ML model ready (accuracy ±2 positions: {acc}%)")

    # Log active configuration
    logger.info(f"✓ Default vertical: {settings.DEFAULT_VERTICAL}")
    logger.info(f"✓ Novelty threshold: {settings.NOVELTY_THRESHOLD}")
    logger.info(f"✓ Claude API: {'configured' if not settings.ANTHROPIC_API_KEY.startswith('sk-ant-YOUR') else 'not set (using Ollama/template)'}")
    logger.info(f"✓ Ahrefs API: {'configured' if settings.AHREFS_API_KEY else 'not set (using DuckDuckGo)'}")
    logger.info(f"✓ Neo4j: {'configured' if settings.NEO4J_URI else 'not set (using NetworkX)'}")

    yield

    # Shutdown
    await close_db()
    logger.info("Qontint shutdown complete.")


# ─── FastAPI App ──────────────────────────────────────────────────────

app = FastAPI(
    title="Qontint — Semantic Authority OS",
    description=(
        "AI-powered platform that predicts whether content will rank on Google (and YouTube) "
        "before publishing. Uses NLP, Knowledge Graphs, Machine Learning, "
        "Novelty Scoring, Intent Mapping, and Ranking Prediction. "
        "Supports 6 verticals: SaaS, Mortgage, Healthcare, Finance, Legal, Insurance."
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS Middleware ──────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Register Routes ─────────────────────────────────────────────────

app.include_router(api_router)


# ─── Health Check ─────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    """Health check and system info."""
    from app.services.ml_trainer import get_model_metadata
    ml_meta = get_model_metadata()
    return {
        "name": "Qontint — Semantic Authority OS",
        "version": settings.APP_VERSION,
        "status": "operational",
        "modules": {
            "serp_collector": "active",
            "entity_extractor": "active",
            "graph_builder": "active",
            "novelty_scorer": "active",
            "ranking_predictor": "active",
            "intent_mapper": "active",
            "content_analyzer": "active",
            "recommendation_engine": "active",
            "content_generator": "active",
            "validation_loop": "active",
            "slm_manager": "active (6 verticals)",
            "workflow_engine": "active",
            "cache_manager": f"active ({cache_manager.backend})",
            "ml_trainer": "active",
            "youtube_analyzer": "active",
            "auth_service": "active",
        },
        "integrations": {
            "claude_api": "configured" if not settings.ANTHROPIC_API_KEY.startswith("sk-ant-YOUR") else "not_configured",
            "ahrefs_api": "configured" if settings.AHREFS_API_KEY else "not_configured",
            "youtube_api": "configured" if settings.YOUTUBE_API_KEY else "not_configured",
            "redis": "configured" if settings.REDIS_URL else "not_configured",
            "neo4j": "configured" if settings.NEO4J_URI else "not_configured",
        },
        "ml_model": ml_meta,
        "verticals": ["saas", "mortgage", "healthcare", "finance", "legal", "insurance"],
        "vertical": settings.DEFAULT_VERTICAL,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health():
    """Simple health check."""
    return {"status": "ok"}
