"""
MODULE 7 — Real-Time Content Analyzer
Orchestrates the full analysis pipeline: Extract → Graph → Novelty → Predict → Suggest
Target execution: <10 seconds with in-memory caching.
"""
import logging
import time
from typing import Dict, Optional
from cachetools import TTLCache

from app.services.entity_extractor import entity_extractor
from app.services.graph_builder import graph_builder
from app.services.novelty_scorer import novelty_scorer
from app.services.ranking_predictor import ranking_predictor
from app.services.intent_mapper import intent_mapper
from app.services.recommendation_engine import recommendation_engine

logger = logging.getLogger(__name__)

# In-memory cache with 10-minute TTL
_analysis_cache = TTLCache(maxsize=100, ttl=600)


class ContentAnalyzer:
    """
    Real-time content analysis pipeline.
    Orchestrates all intelligence modules for comprehensive content scoring.

    Pipeline:
        1. Extract Entities from content
        2. Query Knowledge Graph for SERP intelligence
        3. Calculate Novelty Score
        4. Predict Ranking Position
        5. Generate Recommendations
    """

    async def analyze(
        self,
        content: str,
        keyword: str,
        vertical: str = "saas",
        serp_entities: Optional[list] = None,
        serp_relationships: Optional[list] = None,
    ) -> Dict:
        """
        Run full analysis pipeline on content.
        Returns comprehensive analysis result.
        """
        start_time = time.time()

        # Check cache
        cache_key = f"{hash(content[:200])}:{keyword}"
        if cache_key in _analysis_cache:
            logger.info(f"Analysis cache hit for '{keyword}'")
            return _analysis_cache[cache_key]

        try:
            # Step 1: Extract entities from user content
            content_entities = entity_extractor.extract_entities(content, vertical)
            content_relationships = entity_extractor.extract_relationships(content)

            # Step 2: Get SERP intelligence from knowledge graph
            if serp_entities is None:
                graph_data = graph_builder.get_graph_data(keyword)
                serp_entities = [
                    {"text": n["label"], "type": n["type"], "frequency": n["frequency"]}
                    for n in graph_data.get("nodes", [])
                ]

            if serp_relationships is None:
                graph_data = graph_builder.get_graph_data(keyword)
                serp_relationships = [
                    {"source": e["source"], "target": e["target"], "relationship": e["relationship"]}
                    for e in graph_data.get("edges", [])
                ]

            # Step 3: Calculate novelty
            novelty_result = novelty_scorer.score(
                content_entities,
                serp_entities,
                content_relationships,
                serp_relationships,
            )

            # Step 4: Calculate entity coverage and authority
            entity_coverage = entity_extractor.calculate_entity_coverage(
                content_entities, serp_entities
            )

            relationship_completeness = graph_builder.get_relationship_completeness(
                keyword, content_relationships
            )

            # Average authority of entities found in content
            top_entities = graph_builder.get_top_entities(keyword, n=50)
            content_entity_texts = {e["text"].lower() for e in content_entities}
            authority_scores = [
                e["authority_score"]
                for e in top_entities
                if e["text"].lower() in content_entity_texts
            ]
            avg_authority = sum(authority_scores) / len(authority_scores) if authority_scores else 0.3

            # Content quality
            content_quality = ranking_predictor.calculate_content_quality(content)

            # Step 5: Predict ranking
            prediction = ranking_predictor.predict(
                entity_coverage=entity_coverage,
                relationship_completeness=relationship_completeness,
                authority_score=avg_authority,
                content_quality=content_quality,
            )

            # Step 6: Intent analysis
            query_intent = intent_mapper.classify_query_intent(keyword)
            content_intent = intent_mapper.classify_content_intent(content)
            intent_alignment = intent_mapper.calculate_alignment(query_intent, content_intent)

            # Step 7: Get recommendations
            recommendations = recommendation_engine.recommend(
                keyword=keyword,
                content_entities=content_entities,
                novelty_score=novelty_result["novelty_score"],
            )

            # Missing entities
            missing = graph_builder.get_missing_entities(keyword, content_entities)

            elapsed = time.time() - start_time

            result = {
                "keyword": keyword,
                "novelty_score": novelty_result["novelty_score"],
                "entity_novelty": novelty_result["entity_novelty"],
                "relationship_novelty": novelty_result["relationship_novelty"],
                "semantic_diversity": novelty_result["semantic_diversity"],
                "predicted_rank": prediction["predicted_position"],
                "confidence_score": prediction["confidence"],
                "intent_alignment": intent_alignment["alignment_score"],
                "intent_type": query_intent["intent_type"],
                "entity_coverage": round(entity_coverage, 4),
                "relationship_completeness": round(relationship_completeness, 4),
                "authority_score": round(avg_authority, 4),
                "content_quality": round(content_quality, 4),
                "pass_fail": novelty_result["pass_fail"],
                "entities_found": content_entities[:30],
                "missing_entities": missing[:10],
                "recommendations": recommendations,
                "intent_details": intent_alignment,
                "prediction_features": prediction["features"],
                "analysis_time_seconds": round(elapsed, 2),
                "analyzed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

            # Cache the result
            _analysis_cache[cache_key] = result

            logger.info(
                f"Analysis complete for '{keyword}' in {elapsed:.2f}s | "
                f"Novelty={novelty_result['novelty_score']:.3f} | "
                f"Rank={prediction['predicted_position']} | "
                f"Pass={novelty_result['pass_fail']}"
            )

            return result

        except Exception as e:
            logger.error(f"Analysis pipeline error: {e}", exc_info=True)
            return {
                "keyword": keyword,
                "error": str(e),
                "novelty_score": 0.0,
                "predicted_rank": 20,
                "confidence_score": 0.0,
                "pass_fail": "FAIL",
                "analysis_time_seconds": round(time.time() - start_time, 2),
            }


# Singleton instance
content_analyzer = ContentAnalyzer()
