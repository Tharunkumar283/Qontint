"""
Qontint — Semantic Authority Operating System
Core Configuration
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App
    APP_NAME: str = "Qontint"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database — SQLite (default) or PostgreSQL
    DATABASE_URL: str = "sqlite+aiosqlite:///./qontint.db"

    # ── LLM Configuration ──────────────────────────────────────────────
    # Claude API (Anthropic) — PRIMARY. Set ANTHROPIC_API_KEY env var.
    ANTHROPIC_API_KEY: str = "sk-ant-YOUR_KEY_HERE"

    # Ollama (free, local) — SECONDARY fallback
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    # ── External APIs ──────────────────────────────────────────────────
    # Ahrefs API — PRIMARY SERP source ($99/mo plan)
    AHREFS_API_KEY: str = ""

    # YouTube Data API v3 — for YouTube ranking prediction
    YOUTUBE_API_KEY: str = ""

    # ── Caching ────────────────────────────────────────────────────────
    # Redis URL — falls back to in-memory if not set
    REDIS_URL: str = ""

    # ── Graph Database ─────────────────────────────────────────────────
    # Neo4j — falls back to in-memory NetworkX if not set
    NEO4J_URI: str = ""
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = ""

    # ── Authentication ─────────────────────────────────────────────────
    JWT_SECRET: str = "qontint_jwt_secret_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 7

    # ── NLP ────────────────────────────────────────────────────────────
    SPACY_MODEL: str = "en_core_web_sm"

    # ── Thresholds ─────────────────────────────────────────────────────
    NOVELTY_THRESHOLD: float = 0.35
    SIMILARITY_THRESHOLD: float = 0.40

    # ── Ranking Prediction ─────────────────────────────────────────────
    MAX_SERP_RESULTS: int = 20
    PREDICTION_CONFIDENCE_MIN: float = 0.70

    # ── Content Generation ─────────────────────────────────────────────
    MAX_VALIDATION_ITERATIONS: int = 5

    # ── Verticals ──────────────────────────────────────────────────────
    DEFAULT_VERTICAL: str = "saas"

    # ── CORS ───────────────────────────────────────────────────────────
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:3000",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
