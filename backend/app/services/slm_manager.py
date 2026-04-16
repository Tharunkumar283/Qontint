"""
MODULE 11 — Vertical Small Language Models (SLMs) Manager
Manages domain-specific entity recognition and relationship patterns.
MVP: SaaS vertical model.
"""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


# ─── SaaS Vertical Model Definition ──────────────────────────────────

SAAS_MODEL = {
    "name": "SaaS Vertical Model",
    "version": "1.0.0",
    "vertical": "saas",
    "description": "Domain-specific model for SaaS industry entity recognition and ranking prediction",

    # Custom entity patterns beyond standard NER
    "entity_patterns": {
        "SAAS_METRIC": {
            "patterns": [
                "MRR", "ARR", "NRR", "CAC", "LTV", "ARPU", "ARPA",
                "churn rate", "retention rate", "burn rate", "runway",
                "gross margin", "net margin", "EBITDA",
                "CAC payback period", "magic number", "rule of 40",
                "LTV:CAC ratio", "quick ratio", "NDR",
                "net dollar retention", "gross revenue retention",
                "expansion revenue", "contraction revenue",
            ],
            "weight": 1.5,
        },
        "SAAS_CONCEPT": {
            "patterns": [
                "product-led growth", "PLG", "sales-led growth", "SLG",
                "community-led growth", "CLG", "partner-led growth",
                "freemium", "free trial", "reverse trial",
                "usage-based pricing", "seat-based pricing", "tiered pricing",
                "value metric", "pricing page", "pricing strategy",
                "product-market fit", "PMF", "go-to-market", "GTM",
                "ideal customer profile", "ICP", "buyer persona",
                "total addressable market", "TAM", "SAM", "SOM",
                "customer success", "customer health score",
                "net promoter score", "NPS", "CSAT", "CES",
                "onboarding", "activation", "time to value",
                "feature adoption", "feature flag", "feature gating",
                "multi-tenant architecture", "single-tenant",
                "microservices", "monolith", "serverless",
                "API-first", "developer experience", "DX",
                "CI/CD pipeline", "DevOps", "SRE",
                "SOC 2", "ISO 27001", "GDPR", "HIPAA", "FedRAMP",
            ],
            "weight": 1.3,
        },
        "SAAS_STRATEGY": {
            "patterns": [
                "A/B testing", "cohort analysis", "funnel analysis",
                "customer segmentation", "persona development",
                "land and expand", "bottoms-up", "top-down",
                "content marketing", "SEO strategy", "demand generation",
                "account-based marketing", "ABM", "inbound marketing",
                "outbound sales", "SDR", "BDR", "AE",
                "customer advisory board", "beta program",
                "product hunt launch", "viral loop",
                "referral program", "partner program",
                "self-serve model", "enterprise sales motion",
            ],
            "weight": 1.2,
        },
        "SAAS_STAGE": {
            "patterns": [
                "pre-seed", "seed", "Series A", "Series B", "Series C",
                "growth stage", "scale-up", "IPO", "acquisition",
                "bootstrap", "bootstrapped", "venture-backed",
                "unicorn", "decacorn", "centaur",
            ],
            "weight": 1.0,
        },
    },

    # Relationship patterns specific to SaaS
    "relationship_patterns": {
        "drives": ["PLG drives adoption", "content drives leads", "NPS drives retention"],
        "measures": ["MRR measures revenue", "CAC measures efficiency", "NRR measures expansion"],
        "enables": ["automation enables scale", "API enables integration", "SSO enables enterprise"],
        "requires": ["enterprise requires SOC 2", "growth requires PMF", "scaling requires automation"],
        "impacts": ["churn impacts ARR", "pricing impacts CAC", "onboarding impacts activation"],
    },

    # Authority weight adjustments for SaaS context
    "authority_weights": {
        "SAAS_METRIC": 1.5,
        "SAAS_CONCEPT": 1.3,
        "SAAS_STRATEGY": 1.2,
        "SAAS_STAGE": 1.0,
        "ORG": 0.8,
        "PERSON": 0.6,
        "KEYWORD": 0.4,
    },
}


class SLMManager:
    """
    Manages Vertical Small Language Models (SLMs).
    Currently supports SaaS vertical with plans for extensibility.

    Responsibilities:
    - Load vertical-specific entity patterns
    - Adjust authority scoring weights
    - Provide domain-aware entity recognition
    - Support training data generation
    """

    def __init__(self):
        self._models: Dict[str, Dict] = {
            "saas": SAAS_MODEL,
        }
        self._active_model: Optional[str] = "saas"

    def get_model(self, vertical: str) -> Optional[Dict]:
        """Get the SLM configuration for a vertical."""
        return self._models.get(vertical)

    def get_entity_patterns(self, vertical: str) -> Dict:
        """Get domain-specific entity patterns for a vertical."""
        model = self._models.get(vertical)
        if model:
            return model.get("entity_patterns", {})
        return {}

    def get_authority_weights(self, vertical: str) -> Dict[str, float]:
        """Get authority weight adjustments for entity types."""
        model = self._models.get(vertical)
        if model:
            return model.get("authority_weights", {})
        return {}

    def adjust_authority_score(
        self,
        entity_type: str,
        base_score: float,
        vertical: str = "saas",
    ) -> float:
        """Adjust entity authority score based on vertical-specific weights."""
        weights = self.get_authority_weights(vertical)
        weight = weights.get(entity_type, 1.0)
        adjusted = base_score * weight
        return min(adjusted, 1.0)

    def get_available_verticals(self) -> List[Dict]:
        """List all available vertical models."""
        return [
            {
                "vertical": key,
                "name": model["name"],
                "version": model["version"],
                "description": model["description"],
                "entity_types": list(model.get("entity_patterns", {}).keys()),
            }
            for key, model in self._models.items()
        ]

    def is_domain_entity(self, text: str, vertical: str = "saas") -> Optional[Dict]:
        """Check if text matches a domain-specific entity pattern."""
        patterns = self.get_entity_patterns(vertical)
        text_lower = text.lower()

        for entity_type, config in patterns.items():
            for pattern in config["patterns"]:
                if pattern.lower() == text_lower or pattern.lower() in text_lower:
                    return {
                        "text": text,
                        "type": entity_type,
                        "weight": config.get("weight", 1.0),
                        "vertical": vertical,
                    }
        return None

    def enrich_entities(
        self,
        entities: List[Dict],
        vertical: str = "saas",
    ) -> List[Dict]:
        """Enrich entities with vertical-specific information."""
        enriched = []
        for entity in entities:
            domain_match = self.is_domain_entity(entity["text"], vertical)
            if domain_match:
                entity["type"] = domain_match["type"]
                entity["domain_weight"] = domain_match["weight"]
                entity["vertical"] = vertical
            enriched.append(entity)
        return enriched


# Singleton instance
slm_manager = SLMManager()
