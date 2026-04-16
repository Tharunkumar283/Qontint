"""
Qontint — Semantic Authority Operating System
Core Configuration
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App
    APP_NAME: str = "Qontint"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./qontint.db"

    # Ollama LLM (free, local)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    # NLP
    SPACY_MODEL: str = "en_core_web_sm"

    # Novelty Thresholds
    NOVELTY_THRESHOLD: float = 0.35
    SIMILARITY_THRESHOLD: float = 0.40

    # Ranking Prediction
    MAX_SERP_RESULTS: int = 20
    PREDICTION_CONFIDENCE_MIN: float = 0.70

    # Content Generation
    MAX_VALIDATION_ITERATIONS: int = 5

    # MVP Vertical
    DEFAULT_VERTICAL: str = "saas"

    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
