"""
╔═══════════════════════════════════════════════════════════════╗
║  QONTINT — Semantic Authority Operating System               ║
║  AI-Powered Content Ranking Prediction Platform              ║
║                                                               ║
║  Architecture: Intelligence FIRST, Generation SECOND          ║
║  Stack: FastAPI + spaCy + NetworkX + XGBoost                  ║
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
    logger.info("✓ Database initialized (SQLite)")

    # Log configuration
    logger.info(f"✓ Vertical: {settings.DEFAULT_VERTICAL}")
    logger.info(f"✓ Novelty threshold: {settings.NOVELTY_THRESHOLD}")
    logger.info(f"✓ CORS origins: {settings.CORS_ORIGINS}")

    yield

    # Shutdown
    await close_db()
    logger.info("Qontint shutdown complete.")


# ─── FastAPI App ──────────────────────────────────────────────────────

app = FastAPI(
    title="Qontint — Semantic Authority OS",
    description=(
        "AI-powered platform that predicts whether content will rank on Google "
        "before publishing. Uses NLP, Knowledge Graphs, Machine Learning, "
        "Novelty Scoring, Intent Mapping, and Ranking Prediction."
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
            "slm_manager": "active",
            "workflow_engine": "active",
        },
        "vertical": settings.DEFAULT_VERTICAL,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health():
    """Simple health check."""
    return {"status": "ok"}
