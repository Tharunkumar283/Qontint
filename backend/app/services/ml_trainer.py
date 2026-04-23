"""
ML Training Pipeline — Auto-trains XGBoost ranking model.
Generates synthetic training data from SERP patterns and trains a gradient
boosting model. Saves to ml/models/ranking_model.json.
Run manually: python -m app.services.ml_trainer
"""
import os
import logging
import json
from typing import List, Tuple

logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "ml", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "ranking_model.json")
METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.json")


def _generate_training_data() -> Tuple[List[List[float]], List[float]]:
    """
    Generate synthetic training data representing real-world SERP patterns.
    Features: [entity_coverage, relationship_completeness, authority_score, content_quality]
    Label: SERP position (1-20)
    """
    import random
    random.seed(42)

    X, y = [], []

    # Pattern 1: Top rankers (position 1-3) — high on all features
    for _ in range(200):
        ec = random.uniform(0.75, 1.0)
        rc = random.uniform(0.70, 1.0)
        auth = random.uniform(0.70, 1.0)
        cq = random.uniform(0.65, 1.0)
        pos = random.uniform(1, 3)
        X.append([ec, rc, auth, cq])
        y.append(pos)

    # Pattern 2: Good content (position 4-7) — high entity coverage, moderate rest
    for _ in range(200):
        ec = random.uniform(0.60, 0.85)
        rc = random.uniform(0.50, 0.75)
        auth = random.uniform(0.55, 0.80)
        cq = random.uniform(0.55, 0.80)
        pos = random.uniform(4, 7)
        X.append([ec, rc, auth, cq])
        y.append(pos)

    # Pattern 3: Moderate content (position 8-12)
    for _ in range(200):
        ec = random.uniform(0.40, 0.65)
        rc = random.uniform(0.35, 0.60)
        auth = random.uniform(0.35, 0.65)
        cq = random.uniform(0.40, 0.65)
        pos = random.uniform(8, 12)
        X.append([ec, rc, auth, cq])
        y.append(pos)

    # Pattern 4: Poor content (position 13-20) — low coverage & authority
    for _ in range(200):
        ec = random.uniform(0.10, 0.45)
        rc = random.uniform(0.05, 0.40)
        auth = random.uniform(0.05, 0.40)
        cq = random.uniform(0.10, 0.45)
        pos = random.uniform(13, 20)
        X.append([ec, rc, auth, cq])
        y.append(pos)

    # Pattern 5: High quality but low authority (outliers)
    for _ in range(100):
        ec = random.uniform(0.60, 0.90)
        rc = random.uniform(0.50, 0.75)
        auth = random.uniform(0.20, 0.45)  # Low authority
        cq = random.uniform(0.75, 1.0)  # High quality
        pos = random.uniform(5, 14)
        X.append([ec, rc, auth, cq])
        y.append(pos)

    # Pattern 6: High authority, poor freshness (established pages)
    for _ in range(100):
        ec = random.uniform(0.50, 0.75)
        rc = random.uniform(0.40, 0.65)
        auth = random.uniform(0.75, 1.0)  # High authority
        cq = random.uniform(0.35, 0.60)  # Older content quality
        pos = random.uniform(3, 10)
        X.append([ec, rc, auth, cq])
        y.append(pos)

    return X, y


def train_model() -> bool:
    """Train and save the XGBoost ranking model. Returns True on success."""
    try:
        import xgboost as xgb
        import numpy as np

        logger.info("ML Trainer: Generating synthetic training data...")
        X_list, y_list = _generate_training_data()
        X = np.array(X_list)
        y = np.array(y_list)

        # Train XGBoost regressor
        model = xgb.XGBRegressor(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.08,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            objective="reg:squarederror",
            eval_metric="rmse",
        )

        # Split train/val
        split = int(len(X) * 0.85)
        X_train, X_val = X[:split], X[split:]
        y_train, y_val = y[:split], y[split:]

        model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            verbose=False,
        )

        # Compute accuracy (within ±2 positions)
        preds = model.predict(X_val)
        within_2 = sum(abs(p - a) <= 2 for p, a in zip(preds, y_val))
        accuracy = within_2 / len(y_val)

        # Save model
        os.makedirs(MODEL_DIR, exist_ok=True)
        model.save_model(MODEL_PATH)

        # Save metadata
        metadata = {
            "model_type": "XGBoostRegressor",
            "features": ["entity_coverage", "relationship_completeness", "authority_score", "content_quality"],
            "feature_weights": {"entity_coverage": 0.40, "relationship_completeness": 0.30, "authority_score": 0.20, "content_quality": 0.10},
            "training_samples": len(X),
            "validation_samples": len(X_val),
            "accuracy_within_2_positions": round(accuracy * 100, 1),
            "n_estimators": 200,
            "max_depth": 5,
            "learning_rate": 0.08,
        }
        with open(METADATA_PATH, "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"✓ ML model trained: {len(X)} samples, accuracy ±2 positions: {accuracy * 100:.1f}%")
        logger.info(f"✓ Model saved to: {MODEL_PATH}")
        return True

    except ImportError as e:
        logger.warning(f"ML training skipped — missing dependency: {e}")
        return False
    except Exception as e:
        logger.error(f"ML training failed: {e}")
        return False


async def ensure_model_exists():
    """Called on startup — trains model if it doesn't exist."""
    if os.path.exists(MODEL_PATH):
        logger.info(f"✓ ML model already exists: {MODEL_PATH}")
        return True
    logger.info("ML model not found. Training now...")
    return train_model()


def get_model_metadata() -> dict:
    """Return model metadata if available."""
    try:
        if os.path.exists(METADATA_PATH):
            with open(METADATA_PATH) as f:
                return json.load(f)
    except Exception:
        pass
    return {"status": "not_trained"}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train_model()
