"""
MODULE 3 — Knowledge Graph Builder
Uses NetworkX (free, pure Python) to build entity relationship graphs.
Implements PageRank for authority scoring.
"""
import logging
from typing import List, Dict, Optional, Tuple
from collections import defaultdict

import networkx as nx

logger = logging.getLogger(__name__)


class GraphBuilder:
    """
    Builds and manages entity knowledge graphs using NetworkX.
    Supports PageRank authority scoring, co-occurrence analysis,
    and graph querying for recommendation engine.
    """

    def __init__(self):
        self._graphs: Dict[str, nx.DiGraph] = {}

    def get_or_create_graph(self, keyword: str) -> nx.DiGraph:
        """Get existing graph or create new one for a keyword."""
        if keyword not in self._graphs:
            self._graphs[keyword] = nx.DiGraph()
        return self._graphs[keyword]

    def build_graph(
        self,
        keyword: str,
        entities: List[Dict],
        relationships: List[Dict],
    ) -> nx.DiGraph:
        """
        Build a knowledge graph from extracted entities and relationships.
        Creates nodes for entities and edges for relationships.
        """
        graph = self.get_or_create_graph(keyword)

        # Add entity nodes
        for entity in entities:
            node_id = entity["text"].lower().strip()
            if not node_id:
                continue

            if graph.has_node(node_id):
                # Update existing node
                graph.nodes[node_id]["frequency"] = (
                    graph.nodes[node_id].get("frequency", 0) + entity.get("frequency", 1)
                )
            else:
                graph.add_node(
                    node_id,
                    label=entity["text"],
                    type=entity.get("type", "UNKNOWN"),
                    frequency=entity.get("frequency", 1),
                    authority=0.0,
                )

        # Add relationship edges
        for rel in relationships:
            source = rel["source"].lower().strip()
            target = rel["target"].lower().strip()

            if not source or not target or source == target:
                continue

            # Ensure nodes exist
            if not graph.has_node(source):
                graph.add_node(source, label=rel["source"], type="ENTITY", frequency=1, authority=0.0)
            if not graph.has_node(target):
                graph.add_node(target, label=rel["target"], type="ENTITY", frequency=1, authority=0.0)

            if graph.has_edge(source, target):
                graph[source][target]["weight"] += 1
                graph[source][target]["source_count"] += 1
            else:
                graph.add_edge(
                    source,
                    target,
                    relationship=rel.get("relationship", "related_to"),
                    weight=1.0,
                    context=rel.get("context", ""),
                    source_count=1,
                )

        # Compute authority scores
        self._compute_authority(keyword)

        logger.info(
            f"Graph for '{keyword}': {graph.number_of_nodes()} nodes, "
            f"{graph.number_of_edges()} edges"
        )
        return graph

    def _compute_authority(self, keyword: str):
        """
        Compute PageRank authority scores for all entities.
        Normalizes scores to 0-1 range.
        """
        graph = self._graphs.get(keyword)
        if not graph or graph.number_of_nodes() == 0:
            return

        try:
            # Compute PageRank
            pagerank_scores = nx.pagerank(
                graph,
                alpha=0.85,  # Damping factor
                max_iter=100,
                tol=1e-06,
                weight="weight",
            )

            # Normalize to 0-1 range
            max_score = max(pagerank_scores.values()) if pagerank_scores else 1.0
            min_score = min(pagerank_scores.values()) if pagerank_scores else 0.0
            score_range = max_score - min_score if max_score != min_score else 1.0

            for node, score in pagerank_scores.items():
                normalized = (score - min_score) / score_range
                graph.nodes[node]["authority"] = round(normalized, 4)

        except Exception as e:
            logger.error(f"PageRank computation failed: {e}")
            # Fallback: use degree centrality
            for node in graph.nodes:
                degree = graph.degree(node)
                max_degree = max(dict(graph.degree()).values()) or 1
                graph.nodes[node]["authority"] = round(degree / max_degree, 4)

    def get_top_entities(self, keyword: str, n: int = 10) -> List[Dict]:
        """Get top N entities by authority score."""
        graph = self._graphs.get(keyword)
        if not graph:
            return []

        entities = []
        for node, data in graph.nodes(data=True):
            entities.append({
                "text": data.get("label", node),
                "type": data.get("type", "UNKNOWN"),
                "authority_score": data.get("authority", 0.0),
                "frequency": data.get("frequency", 1),
            })

        return sorted(entities, key=lambda x: x["authority_score"], reverse=True)[:n]

    def get_missing_entities(
        self,
        keyword: str,
        content_entities: List[Dict],
    ) -> List[Dict]:
        """
        Find high-authority entities from the graph that are missing in the content.
        Used by the Recommendation Engine (Module 8).
        """
        graph = self._graphs.get(keyword)
        if not graph:
            return []

        content_set = {e["text"].lower() for e in content_entities}

        missing = []
        for node, data in graph.nodes(data=True):
            if node not in content_set and data.get("authority", 0) > 0.1:
                missing.append({
                    "text": data.get("label", node),
                    "type": data.get("type", "UNKNOWN"),
                    "authority_score": data.get("authority", 0.0),
                    "frequency": data.get("frequency", 1),
                })

        return sorted(missing, key=lambda x: x["authority_score"], reverse=True)

    def get_relationship_completeness(
        self,
        keyword: str,
        content_relationships: List[Dict],
    ) -> float:
        """
        Calculate how completely content covers SERP relationship patterns.
        Returns completeness score (0-1).
        """
        graph = self._graphs.get(keyword)
        if not graph or graph.number_of_edges() == 0:
            return 0.0

        content_pairs = set()
        for rel in content_relationships:
            pair = (rel["source"].lower(), rel["target"].lower())
            content_pairs.add(pair)
            content_pairs.add((pair[1], pair[0]))  # Bidirectional

        graph_pairs = set()
        for u, v in graph.edges():
            graph_pairs.add((u, v))

        if not graph_pairs:
            return 0.0

        overlap = content_pairs & graph_pairs
        return len(overlap) / len(graph_pairs)

    def get_graph_data(self, keyword: str) -> Dict:
        """
        Export graph data for frontend visualization.
        Returns nodes and edges in a format suitable for react-force-graph.
        """
        graph = self._graphs.get(keyword)
        if not graph:
            return {"nodes": [], "edges": [], "stats": {}}

        nodes = []
        for node, data in graph.nodes(data=True):
            authority = data.get("authority", 0.0)
            nodes.append({
                "id": node,
                "label": data.get("label", node),
                "type": data.get("type", "UNKNOWN"),
                "authority": authority,
                "frequency": data.get("frequency", 1),
                "size": 5 + (authority * 30),  # Scale node size by authority
            })

        edges = []
        for u, v, data in graph.edges(data=True):
            edges.append({
                "source": u,
                "target": v,
                "relationship": data.get("relationship", "related_to"),
                "weight": data.get("weight", 1.0),
            })

        # Compute stats
        authorities = [n["authority"] for n in nodes]
        avg_authority = sum(authorities) / len(authorities) if authorities else 0.0

        top_entities = sorted(nodes, key=lambda x: x["authority"], reverse=True)[:5]

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "avg_authority": round(avg_authority, 4),
                "top_entities": [
                    {
                        "text": e["label"],
                        "type": e["type"],
                        "authority_score": e["authority"],
                        "frequency": e["frequency"],
                    }
                    for e in top_entities
                ],
            },
        }

    def get_entity_neighbors(self, keyword: str, entity: str) -> List[Dict]:
        """Get all entities connected to a specific entity."""
        graph = self._graphs.get(keyword)
        if not graph or not graph.has_node(entity.lower()):
            return []

        neighbors = []
        for neighbor in graph.neighbors(entity.lower()):
            data = graph.nodes[neighbor]
            edge_data = graph[entity.lower()][neighbor]
            neighbors.append({
                "text": data.get("label", neighbor),
                "type": data.get("type", "UNKNOWN"),
                "authority_score": data.get("authority", 0.0),
                "relationship": edge_data.get("relationship", "related_to"),
                "weight": edge_data.get("weight", 1.0),
            })

        return sorted(neighbors, key=lambda x: x["authority_score"], reverse=True)


# Singleton instance
graph_builder = GraphBuilder()
