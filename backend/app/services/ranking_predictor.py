"""
MODULE 5 — Ranking Prediction Engine
Uses XGBoost Gradient Boosting for SERP position prediction.
Features: Entity Coverage (40%), Relationship Completeness (30%),
Authority Score (20%), Content Quality (10%).
"""
import logging
import math
import os
from typing import Dict, Optional, Tuple

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

logger = logging.getLogger(__name__)



class RankingPredictor:
    """
    Predicts Google ranking position (1-20) using gradient boosting.
    Uses an intelligent feature-weighted scoring system with XGBoost
    when trained model is available, otherwise uses weighted formula.

    Feature Weights:
        Entity Coverage     → 40%
        Relationship Comp.  → 30%
        Authority Score     → 20%
        Content Quality     → 10%
    """

    WEIGHTS = {
        "entity_coverage": 0.40,
        "relationship_completeness": 0.30,
        "authority_score": 0.20,
        "content_quality": 0.10,
    }

    def __init__(self):
        self._model = None
        self._model_loaded = False

    def _try_load_model(self):
        """Attempt to load a trained XGBoost model."""
        if self._model_loaded:
            return

        model_path = os.path.join(
            os.path.dirname(__file__), "..", "ml", "models", "ranking_model.json"
        )

        try:
            import xgboost as xgb
            if os.path.exists(model_path):
                self._model = xgb.XGBRegressor()
                self._model.load_model(model_path)
                logger.info("Loaded trained ranking model.")
            else:
                logger.info("No trained model found. Using weighted prediction.")
        except Exception as e:
            logger.info(f"XGBoost not available: {e}. Using weighted prediction.")

        self._model_loaded = True

    def predict(
        self,
        entity_coverage: float,
        relationship_completeness: float,
        authority_score: float,
        content_quality: float,
    ) -> Dict:
        """
        Predict SERP ranking position and confidence.

        Args:
            entity_coverage: How well content covers SERP entities (0-1)
            relationship_completeness: Coverage of relationship patterns (0-1)
            authority_score: Average authority of entities used (0-1)
            content_quality: Content quality score (0-1)

        Returns:
            Dict with predicted_position (1-20), confidence (0-1), features
        """
        self._try_load_model()

        # Ensure values are in [0, 1]
        features = {
            "entity_coverage": max(0, min(1, entity_coverage)),
            "relationship_completeness": max(0, min(1, relationship_completeness)),
            "authority_score": max(0, min(1, authority_score)),
            "content_quality": max(0, min(1, content_quality)),
        }

        if self._model and HAS_NUMPY:
            return self._predict_xgboost(features)
        else:
            return self._predict_weighted(features)

    def _predict_xgboost(self, features: Dict) -> Dict:
        """Predict using trained XGBoost model."""
        try:
            feature_array = np.array([[
                features["entity_coverage"],
                features["relationship_completeness"],
                features["authority_score"],
                features["content_quality"],
            ]])

            predicted = self._model.predict(feature_array)[0]
            position = max(1, min(20, round(predicted)))

            # Confidence based on feature strength
            confidence = self._calculate_confidence(features)

            return self._build_result(position, confidence, features)

        except Exception as e:
            logger.error(f"XGBoost prediction failed: {e}")
            return self._predict_weighted(features)

    def _predict_weighted(self, features: Dict) -> Dict:
        """
        Predict using weighted feature formula.
        This is the fallback when no trained model is available.
        The formula maps weighted features to a ranking position.
        """
        # Calculate weighted score (0-1, higher is better)
        weighted_score = sum(
            features[key] * weight
            for key, weight in self.WEIGHTS.items()
        )

        # Map score to position (1-20)
        # Score 1.0 → position 1, Score 0.0 → position 20
        # Using a non-linear mapping (positions near top are harder to achieve)
        if weighted_score >= 0.90:
            position = 1
        elif weighted_score >= 0.85:
            position = 2
        elif weighted_score >= 0.80:
            position = 3
        elif weighted_score >= 0.70:
            position = max(4, int(4 + (0.80 - weighted_score) * 30))
        elif weighted_score >= 0.50:
            position = max(7, int(7 + (0.70 - weighted_score) * 30))
        elif weighted_score >= 0.30:
            position = max(13, int(13 + (0.50 - weighted_score) * 20))
        else:
            position = max(17, int(17 + (0.30 - weighted_score) * 10))

        position = max(1, min(20, position))
        confidence = self._calculate_confidence(features)

        return self._build_result(position, confidence, features)

    def _calculate_confidence(self, features: Dict) -> float:
        """
        Calculate prediction confidence based on feature quality.
        Higher and more balanced features = higher confidence.
        """
        values = list(features.values())
        avg = sum(values) / len(values)
        std = (sum((v - avg) ** 2 for v in values) / len(values)) ** 0.5

        # High average = high confidence
        # Low standard deviation = consistent features = higher confidence
        consistency_bonus = max(0, 0.15 - std)  # Bonus for consistent features

        confidence = avg * 0.75 + consistency_bonus * 0.25 + 0.20
        return round(min(max(confidence, 0.10), 0.99), 4)

    def _build_result(self, position: int, confidence: float, features: Dict) -> Dict:
        """Build prediction result dictionary."""
        return {
            "predicted_position": position,
            "confidence": confidence,
            "features": {
                **features,
                "weights": self.WEIGHTS.copy(),
            },
        }

    def calculate_content_quality(self, content: str) -> float:
        """
        Calculate content quality score based on structural and linguistic features.
        Returns score (0-1).
        """
        if not content:
            return 0.0

        scores = []

        # 1. Length score (500-3000 words is ideal for SEO)
        words = content.split()
        word_count = len(words)
        if word_count < 300:
            length_score = word_count / 300 * 0.5
        elif word_count < 500:
            length_score = 0.6
        elif word_count <= 2000:
            length_score = 0.9
        elif word_count <= 3000:
            length_score = 1.0
        else:
            length_score = max(0.7, 1.0 - (word_count - 3000) / 5000)
        scores.append(length_score)

        # 2. Structure score (headings, paragraphs, lists)
        has_headings = any(line.startswith("#") or line.startswith("##") for line in content.split("\n"))
        has_lists = any(line.strip().startswith(("-", "*", "1.", "2.")) for line in content.split("\n"))
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

        structure_score = 0.3
        if has_headings:
            structure_score += 0.3
        if has_lists:
            structure_score += 0.2
        if len(paragraphs) >= 3:
            structure_score += 0.2
        scores.append(min(structure_score, 1.0))

        # 3. Readability score (avg sentence length)
        sentences = content.replace("!", ".").replace("?", ".").split(".")
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        if sentences:
            avg_sentence_len = sum(len(s.split()) for s in sentences) / len(sentences)
            if 10 <= avg_sentence_len <= 20:
                readability = 1.0
            elif avg_sentence_len < 10:
                readability = avg_sentence_len / 10
            else:
                readability = max(0.3, 1.0 - (avg_sentence_len - 20) / 30)
        else:
            readability = 0.3
        scores.append(readability)

        # 4. Vocabulary diversity
        unique_words = set(w.lower() for w in words if len(w) > 2)
        diversity = len(unique_words) / max(word_count, 1)
        vocab_score = min(diversity * 3, 1.0)
        scores.append(vocab_score)

        return round(sum(scores) / len(scores), 4)


# Singleton instance
ranking_predictor = RankingPredictor()
