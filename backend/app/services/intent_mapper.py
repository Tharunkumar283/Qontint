"""
MODULE 6 — User Intent Mapping Engine
Classifies search intent and detects intent mismatches.
"""
import re
import logging
from typing import Dict, List, Tuple
from collections import Counter

logger = logging.getLogger(__name__)


# Intent classification patterns
INTENT_PATTERNS = {
    "transactional": {
        "keywords": [
            "buy", "purchase", "order", "subscribe", "sign up", "signup",
            "get started", "start free", "pricing", "price", "cost",
            "discount", "coupon", "deal", "offer", "checkout",
            "download", "install", "register", "trial",
            "plan", "upgrade", "premium",
        ],
        "weight": 1.0,
    },
    "commercial": {
        "keywords": [
            "best", "top", "review", "reviews", "comparison", "compare",
            "vs", "versus", "alternative", "alternatives", "recommended",
            "cheapest", "affordable", "enterprise", "professional",
            "features", "pros and cons", "which", "should i",
            "worth it", "roi", "benchmark",
        ],
        "weight": 0.9,
    },
    "informational": {
        "keywords": [
            "what is", "how to", "how do", "why", "when", "where",
            "guide", "tutorial", "learn", "understand", "explain",
            "definition", "meaning", "example", "examples",
            "tips", "strategies", "strategy", "best practices",
            "framework", "methodology", "approach",
            "benefits", "advantages", "challenges",
        ],
        "weight": 0.8,
    },
    "navigational": {
        "keywords": [
            "login", "log in", "signin", "sign in", "dashboard",
            "account", "profile", "settings", "support", "help",
            "contact", "docs", "documentation", "api",
            "github", "website", "official", "homepage",
        ],
        "weight": 0.7,
    },
}

# SaaS-specific intent signals
SAAS_INTENT_SIGNALS = {
    "transactional": [
        "free trial", "start free trial", "demo", "request demo",
        "book a demo", "get a quote", "contact sales",
    ],
    "commercial": [
        "saas pricing", "pricing model", "pricing strategy",
        "total cost of ownership", "TCO", "vendor comparison",
    ],
    "informational": [
        "saas metrics", "saas kpis", "growth strategy",
        "product-led growth", "customer success",
    ],
}


class IntentMapper:
    """
    Classifies search intent for queries and content.
    Detects intent mismatches between query intent and content intent.

    Intent Types:
        - Informational: User wants to learn/understand
        - Transactional: User wants to buy/act
        - Navigational: User wants to find a specific page
        - Commercial: User wants to compare/evaluate
    """

    def classify_query_intent(self, query: str) -> Dict:
        """
        Classify the search intent of a query.
        Returns intent type and confidence score.
        """
        query_lower = query.lower().strip()
        scores = {}

        for intent, config in INTENT_PATTERNS.items():
            score = 0
            matches = []

            for keyword in config["keywords"]:
                if keyword in query_lower:
                    score += config["weight"]
                    matches.append(keyword)

            # Check SaaS-specific signals
            for signal in SAAS_INTENT_SIGNALS.get(intent, []):
                if signal in query_lower:
                    score += 1.5  # Boost for domain-specific matches
                    matches.append(signal)

            scores[intent] = {"score": score, "matches": matches}

        # Determine primary intent
        if not any(s["score"] > 0 for s in scores.values()):
            # Default to informational if no clear signals
            return {
                "intent_type": "informational",
                "confidence": 0.5,
                "scores": {k: v["score"] for k, v in scores.items()},
                "signals": [],
            }

        best_intent = max(scores, key=lambda k: scores[k]["score"])
        max_score = scores[best_intent]["score"]
        total_score = sum(s["score"] for s in scores.values())

        confidence = max_score / total_score if total_score > 0 else 0.5

        return {
            "intent_type": best_intent,
            "confidence": round(min(confidence, 0.99), 4),
            "scores": {k: round(v["score"], 4) for k, v in scores.items()},
            "signals": scores[best_intent]["matches"],
        }

    def classify_content_intent(self, content: str) -> Dict:
        """
        Classify the intent that content is optimized for.
        Analyzes structure, CTAs, and language patterns.
        """
        content_lower = content.lower()
        scores = Counter()

        # Check for transactional signals (CTAs, pricing, action words)
        cta_patterns = [
            r"get started", r"sign up", r"start free", r"try free",
            r"book a demo", r"request", r"subscribe", r"buy now",
            r"\$\d+", r"per month", r"per year", r"/mo", r"/yr",
        ]
        for pattern in cta_patterns:
            if re.search(pattern, content_lower):
                scores["transactional"] += 1

        # Check for commercial signals
        commercial_patterns = [
            r"vs\.?", r"compared to", r"pros and cons", r"review",
            r"best .+ for", r"top \d+", r"alternative",
        ]
        for pattern in commercial_patterns:
            if re.search(pattern, content_lower):
                scores["commercial"] += 1

        # Check for informational signals
        info_patterns = [
            r"what is", r"how to", r"guide", r"learn",
            r"definition", r"explains", r"understanding",
            r"step \d+", r"in this article", r"let.s explore",
        ]
        for pattern in info_patterns:
            if re.search(pattern, content_lower):
                scores["informational"] += 1

        # Check structural signals
        lines = content.split("\n")
        heading_count = sum(1 for l in lines if l.strip().startswith("#"))
        list_count = sum(1 for l in lines if re.match(r'\s*[-*\d]+[.)]\s', l))

        if heading_count >= 3:
            scores["informational"] += 2
        if list_count >= 5:
            scores["informational"] += 1

        # Determine primary intent
        if not scores:
            return {
                "intent_type": "informational",
                "confidence": 0.5,
                "scores": dict(scores),
            }

        best_intent = scores.most_common(1)[0][0]
        total = sum(scores.values())
        confidence = scores[best_intent] / total if total > 0 else 0.5

        return {
            "intent_type": best_intent,
            "confidence": round(min(confidence, 0.99), 4),
            "scores": dict(scores),
        }

    def calculate_alignment(
        self,
        query_intent: Dict,
        content_intent: Dict,
    ) -> Dict:
        """
        Calculate intent alignment between query and content.
        Detects mismatches and provides recommendations.
        """
        query_type = query_intent["intent_type"]
        content_type = content_intent["intent_type"]

        # Exact match
        if query_type == content_type:
            alignment_score = 1.0
            mismatch = False
            recommendation = "Intent perfectly aligned."
        # Compatible intents
        elif (query_type, content_type) in [
            ("commercial", "informational"),
            ("informational", "commercial"),
            ("transactional", "commercial"),
        ]:
            alignment_score = 0.65
            mismatch = False
            recommendation = (
                f"Partial alignment: Query intent is '{query_type}' "
                f"but content leans '{content_type}'. "
                f"Consider adding more {query_type} elements."
            )
        # Mismatch
        else:
            alignment_score = 0.25
            mismatch = True
            recommendation = (
                f"⚠️ Intent mismatch detected! Query intent is '{query_type}' "
                f"but content is optimized for '{content_type}'. "
                f"This will likely hurt ranking potential. "
                f"Restructure content to match '{query_type}' intent."
            )

        return {
            "alignment_score": round(alignment_score, 4),
            "query_intent": query_type,
            "content_intent": content_type,
            "mismatch": mismatch,
            "recommendation": recommendation,
            "query_confidence": query_intent["confidence"],
            "content_confidence": content_intent["confidence"],
        }


# Singleton instance
intent_mapper = IntentMapper()
