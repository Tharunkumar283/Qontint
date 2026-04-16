"""
MODULE 8 — Intelligent Recommendation Engine
Recommends missing high-authority entities when novelty is below threshold.
"""
import logging
from typing import List, Dict

from app.services.graph_builder import graph_builder

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Generates intelligent entity recommendations by:
    1. Querying the knowledge graph for missing high-authority entities
    2. Ranking by Authority × Relevance × Uniqueness
    3. Generating contextual suggestion text

    Trigger: When novelty < threshold
    Output: Top 3-5 recommended entities
    """

    def recommend(
        self,
        keyword: str,
        content_entities: List[Dict],
        novelty_score: float = 0.0,
        threshold: float = 0.35,
        max_recommendations: int = 5,
    ) -> List[Dict]:
        """
        Generate entity recommendations for improving content.
        Returns list of recommendations with context.
        """
        missing = graph_builder.get_missing_entities(keyword, content_entities)

        if not missing:
            return self._generate_generic_recommendations(keyword, content_entities)

        recommendations = []
        content_entity_texts = {e["text"].lower() for e in content_entities}

        for entity in missing[:max_recommendations * 2]:
            # Calculate relevance score based on graph neighbors
            neighbors = graph_builder.get_entity_neighbors(keyword, entity["text"])
            relevant_neighbors = [
                n for n in neighbors
                if n["text"].lower() in content_entity_texts
            ]
            relevance = len(relevant_neighbors) / max(len(neighbors), 1)

            # Calculate uniqueness (how rare this entity is across SERP)
            uniqueness = 1.0 - min(entity.get("frequency", 1) / 10, 1.0)

            # Combined score
            combined_score = (
                entity["authority_score"] * 0.50
                + relevance * 0.30
                + uniqueness * 0.20
            )

            # Generate contextual suggestion
            context_entities = [n["text"] for n in relevant_neighbors[:3]]
            if context_entities:
                context = f"in the context of {', '.join(context_entities)}"
            else:
                context = f"related to {keyword}"

            suggestion = (
                f"Consider discussing '{entity['text']}' {context}. "
                f"This entity has high authority ({entity['authority_score']:.2f}) "
                f"and could improve your content's ranking potential."
            )

            recommendations.append({
                "entity": entity["text"],
                "entity_type": entity["type"],
                "authority_score": round(entity["authority_score"], 4),
                "relevance_score": round(relevance, 4),
                "uniqueness_score": round(uniqueness, 4),
                "combined_score": round(combined_score, 4),
                "suggestion": suggestion,
                "context": context,
                "related_entities": [n["text"] for n in relevant_neighbors[:5]],
            })

        # Sort by combined score and return top N
        recommendations.sort(key=lambda x: x["combined_score"], reverse=True)

        potential_gain = self._estimate_novelty_gain(
            recommendations[:max_recommendations], novelty_score
        )

        final = recommendations[:max_recommendations]
        for rec in final:
            rec["potential_novelty_gain"] = round(potential_gain, 4)

        return final

    def _generate_generic_recommendations(
        self,
        keyword: str,
        content_entities: List[Dict],
    ) -> List[Dict]:
        """Generate generic recommendations when no graph data available."""
        recommendations = []

        # Suggest diversifying entity types
        type_counts = {}
        for e in content_entities:
            etype = e.get("type", "UNKNOWN")
            type_counts[etype] = type_counts.get(etype, 0) + 1

        missing_types = [
            t for t in ["METRIC", "CONCEPT", "STRATEGY", "ORG", "PRODUCT"]
            if t not in type_counts
        ]

        for i, missing_type in enumerate(missing_types[:3]):
            recommendations.append({
                "entity": f"Add {missing_type.lower()} entities",
                "entity_type": missing_type,
                "authority_score": 0.5,
                "relevance_score": 0.5,
                "uniqueness_score": 0.5,
                "combined_score": 0.5,
                "suggestion": (
                    f"Your content lacks {missing_type.lower()} entities. "
                    f"Adding relevant {missing_type.lower()} references "
                    f"related to '{keyword}' could improve authority coverage."
                ),
                "context": f"for {keyword}",
                "related_entities": [],
                "potential_novelty_gain": 0.05,
            })

        return recommendations

    def _estimate_novelty_gain(
        self,
        recommendations: List[Dict],
        current_novelty: float,
    ) -> float:
        """Estimate potential novelty improvement from recommendations."""
        if not recommendations:
            return 0.0

        avg_authority = sum(
            r["authority_score"] for r in recommendations
        ) / len(recommendations)

        # Estimated novelty gain per recommended entity
        gain_per_entity = avg_authority * 0.03
        total_gain = gain_per_entity * len(recommendations)

        return min(total_gain, 1.0 - current_novelty)


# Singleton instance
recommendation_engine = RecommendationEngine()
