"""
MODULE 4 — Content Novelty Scoring Engine
Calculates entity novelty, relationship novelty, and semantic diversity.
Uses Jaccard similarity and graph comparison.
"""
import logging
from typing import List, Dict, Set
from collections import Counter

logger = logging.getLogger(__name__)


class NoveltyScorer:
    """
    Scores content novelty by comparing against SERP entity landscape.
    Prevents derivative content by enforcing minimum novelty thresholds.

    Decision Rule:
        PASS if Novelty >= 0.35 AND Similarity < 0.40
        Else: FAIL
    """

    def __init__(
        self,
        novelty_threshold: float = 0.35,
        similarity_threshold: float = 0.40,
    ):
        self.novelty_threshold = novelty_threshold
        self.similarity_threshold = similarity_threshold

    def score(
        self,
        content_entities: List[Dict],
        serp_entities: List[Dict],
        content_relationships: List[Dict],
        serp_relationships: List[Dict],
    ) -> Dict:
        """
        Calculate comprehensive novelty score.
        Returns dict with individual scores and overall pass/fail.
        """
        entity_novelty = self._entity_novelty(content_entities, serp_entities)
        relationship_novelty = self._relationship_novelty(
            content_relationships, serp_relationships
        )
        semantic_diversity = self._semantic_diversity(content_entities, serp_entities)

        # Weighted combination
        novelty_score = (
            entity_novelty * 0.40
            + relationship_novelty * 0.35
            + semantic_diversity * 0.25
        )

        # Calculate similarity (inverse perspective)
        similarity = 1.0 - novelty_score

        # Apply decision rule
        pass_fail = "PASS" if (
            novelty_score >= self.novelty_threshold
            and similarity < self.similarity_threshold
        ) else "FAIL"

        result = {
            "novelty_score": round(novelty_score, 4),
            "entity_novelty": round(entity_novelty, 4),
            "relationship_novelty": round(relationship_novelty, 4),
            "semantic_diversity": round(semantic_diversity, 4),
            "similarity": round(similarity, 4),
            "pass_fail": pass_fail,
            "threshold": {
                "novelty_min": self.novelty_threshold,
                "similarity_max": self.similarity_threshold,
            },
        }

        logger.info(
            f"Novelty Score: {novelty_score:.4f} | "
            f"Similarity: {similarity:.4f} | "
            f"Result: {pass_fail}"
        )
        return result

    def _entity_novelty(
        self,
        content_entities: List[Dict],
        serp_entities: List[Dict],
    ) -> float:
        """
        Calculate entity novelty using Jaccard distance.
        Measures how many unique entities the content introduces.
        """
        content_set = self._entity_set(content_entities)
        serp_set = self._entity_set(serp_entities)

        if not content_set and not serp_set:
            return 0.5  # Neutral score if no entities

        # Jaccard distance = 1 - Jaccard similarity
        union = content_set | serp_set
        intersection = content_set & serp_set

        if not union:
            return 0.5

        jaccard_similarity = len(intersection) / len(union)
        jaccard_distance = 1.0 - jaccard_similarity

        # Novel entities ratio (entities in content but not in SERP)
        novel_entities = content_set - serp_set
        novel_ratio = len(novel_entities) / len(content_set) if content_set else 0

        # Combine: some overlap is good (coverage), too much is derivative
        # Sweet spot: moderate overlap with unique additions
        score = (jaccard_distance * 0.6) + (novel_ratio * 0.4)

        return min(max(score, 0.0), 1.0)

    def _relationship_novelty(
        self,
        content_relationships: List[Dict],
        serp_relationships: List[Dict],
    ) -> float:
        """
        Calculate relationship novelty via graph comparison.
        Measures how many unique relationship patterns the content introduces.
        """
        content_pairs = self._relationship_set(content_relationships)
        serp_pairs = self._relationship_set(serp_relationships)

        if not content_pairs and not serp_pairs:
            return 0.5

        union = content_pairs | serp_pairs
        intersection = content_pairs & serp_pairs

        if not union:
            return 0.5

        jaccard_distance = 1.0 - (len(intersection) / len(union))

        # Novel relationships
        novel_pairs = content_pairs - serp_pairs
        novel_ratio = len(novel_pairs) / len(content_pairs) if content_pairs else 0

        score = (jaccard_distance * 0.5) + (novel_ratio * 0.5)
        return min(max(score, 0.0), 1.0)

    def _semantic_diversity(
        self,
        content_entities: List[Dict],
        serp_entities: List[Dict],
    ) -> float:
        """
        Calculate semantic diversity based on entity type distribution.
        Content with diverse entity types scores higher.
        """
        content_types = Counter(e.get("type", "UNKNOWN") for e in content_entities)
        serp_types = Counter(e.get("type", "UNKNOWN") for e in serp_entities)

        if not content_types:
            return 0.0

        # Type diversity (number of unique types / total entities)
        content_diversity = len(content_types) / max(sum(content_types.values()), 1)
        serp_diversity = len(serp_types) / max(sum(serp_types.values()), 1) if serp_types else 0

        # Unique type coverage
        all_types = set(content_types.keys()) | set(serp_types.keys())
        content_type_coverage = len(set(content_types.keys())) / len(all_types) if all_types else 0

        # Novel types (types in content but not in SERP)
        novel_types = set(content_types.keys()) - set(serp_types.keys())
        novel_type_ratio = len(novel_types) / len(set(content_types.keys())) if content_types else 0

        score = (
            content_diversity * 0.3
            + content_type_coverage * 0.4
            + novel_type_ratio * 0.3
        )

        return min(max(score, 0.0), 1.0)

    def _entity_set(self, entities: List[Dict]) -> Set[str]:
        """Convert entity list to normalized text set."""
        return {e["text"].lower().strip() for e in entities if e.get("text")}

    def _relationship_set(self, relationships: List[Dict]) -> Set[tuple]:
        """Convert relationship list to normalized pair set."""
        pairs = set()
        for rel in relationships:
            source = rel.get("source", "").lower().strip()
            target = rel.get("target", "").lower().strip()
            if source and target:
                # Normalize order for bidirectional comparison
                pair = tuple(sorted([source, target]))
                pairs.add(pair)
        return pairs


# Singleton instance
novelty_scorer = NoveltyScorer()
