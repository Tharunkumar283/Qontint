"""
MODULE 3 — Knowledge Graph Builder
Primary: Neo4j (set NEO4J_URI + NEO4J_USER + NEO4J_PASSWORD) — persistent, scalable to 100K+ nodes
Fallback: in-memory NetworkX — zero-config, no external server required
Implements PageRank for entity authority scoring in both backends.
"""
import logging
from typing import List, Dict, Optional, Tuple, Any
from collections import defaultdict

import networkx as nx

logger = logging.getLogger(__name__)


class GraphBuilder:
    """
    Builds entity knowledge graphs with dual-backend support:
    • Neo4j (set NEO4J_URI env var) — persistent, ACID, scalable to 100K+ nodes,
      supports Cypher queries and graph algorithms natively.
    • NetworkX (fallback) — in-memory, zero config, works out of the box.

    Automatically detects and uses Neo4j when configured.
    All methods have identical API regardless of backend.
    """

    def __init__(self):
        self._graphs: Dict[str, nx.DiGraph] = {}  # NetworkX graphs (fallback)
        self._neo4j_driver = None
        self._neo4j_available: Optional[bool] = None
        self._init_neo4j()

    def _init_neo4j(self):
        """Attempt to connect to Neo4j. Silently falls back to NetworkX."""
        try:
            from app.core import settings
            if not settings.NEO4J_URI:
                self._neo4j_available = False
                return
            from neo4j import GraphDatabase
            self._neo4j_driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
            )
            self._neo4j_driver.verify_connectivity()
            self._neo4j_available = True
            logger.info(f"✓ Neo4j connected: {settings.NEO4J_URI}")
        except ImportError:
            logger.info("neo4j driver not installed. Using NetworkX.")
            self._neo4j_available = False
        except Exception as e:
            logger.warning(f"Neo4j unavailable ({e}). Using NetworkX.")
            self._neo4j_available = False

    @property
    def using_neo4j(self) -> bool:
        return bool(self._neo4j_available and self._neo4j_driver)

    def _neo4j_upsert_entity(self, keyword: str, entity: Dict[str, Any]):
        """Upsert a single entity node in Neo4j."""
        with self._neo4j_driver.session() as session:
            session.run(
                """
                MERGE (e:Entity {id: $id, keyword: $keyword})
                ON CREATE SET e.label = $label, e.type = $type,
                              e.authority = $authority, e.frequency = $frequency,
                              e.created_at = timestamp()
                ON MATCH SET  e.authority = $authority, e.frequency = $frequency,
                              e.updated_at = timestamp()
                """,
                id=entity["text"].lower().strip(),
                keyword=keyword,
                label=entity["text"],
                type=entity.get("type", "UNKNOWN"),
                authority=entity.get("authority_score", 0.0),
                frequency=entity.get("frequency", 1),
            )

    def _neo4j_upsert_relationship(self, keyword: str, rel: Dict[str, Any]):
        """Upsert a relationship edge in Neo4j."""
        with self._neo4j_driver.session() as session:
            session.run(
                """
                MATCH (a:Entity {id: $source, keyword: $keyword})
                MATCH (b:Entity {id: $target, keyword: $keyword})
                MERGE (a)-[r:RELATES_TO {type: $rel_type}]->(b)
                ON CREATE SET r.weight = $weight, r.created_at = timestamp()
                ON MATCH SET  r.weight = $weight, r.updated_at = timestamp()
                """,
                source=rel["source"].lower().strip(),
                target=rel["target"].lower().strip(),
                keyword=keyword,
                rel_type=rel.get("relationship", "related_to"),
                weight=rel.get("weight", 1.0),
            )

    def _neo4j_get_graph_data(self, keyword: str) -> Dict:
        """Fetch graph data from Neo4j for a keyword."""
        with self._neo4j_driver.session() as session:
            # Nodes
            node_result = session.run(
                "MATCH (e:Entity {keyword: $keyword}) RETURN e",
                keyword=keyword,
            )
            nodes = []
            for record in node_result:
                e = record["e"]
                authority = e.get("authority", 0.0)
                nodes.append({
                    "id": e["id"],
                    "label": e.get("label", e["id"]),
                    "type": e.get("type", "UNKNOWN"),
                    "authority": authority,
                    "frequency": e.get("frequency", 1),
                    "size": 5 + (authority * 30),
                })

            # Edges
            edge_result = session.run(
                "MATCH (a:Entity {keyword: $keyword})-[r:RELATES_TO]->(b:Entity {keyword: $keyword}) RETURN a.id, b.id, r",
                keyword=keyword,
            )
            edges = []
            for record in edge_result:
                r = record["r"]
                edges.append({
                    "source": record["a.id"],
                    "target": record["b.id"],
                    "relationship": r.get("type", "related_to"),
                    "weight": r.get("weight", 1.0),
                })

        authorities = [n["authority"] for n in nodes]
        avg_auth = sum(authorities) / len(authorities) if authorities else 0.0
        top = sorted(nodes, key=lambda x: x["authority"], reverse=True)[:5]
        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "avg_authority": round(avg_auth, 4),
                "top_entities": [
                    {"text": e["label"], "type": e["type"], "authority_score": e["authority"], "frequency": e["frequency"]}
                    for e in top
                ],
                "backend": "neo4j",
            },
        }

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

        # Compute authority scores (NetworkX PageRank fallback)
        self._compute_authority(keyword)

        # Also persist to Neo4j if available
        if self.using_neo4j:
            try:
                for entity in entities:
                    if entity.get("text"):
                        entity_with_auth = dict(entity)
                        node_id = entity["text"].lower().strip()
                        if graph.has_node(node_id):
                            entity_with_auth["authority_score"] = graph.nodes[node_id].get("authority", 0.0)
                        self._neo4j_upsert_entity(keyword, entity_with_auth)
                for rel in relationships:
                    if rel.get("source") and rel.get("target"):
                        self._neo4j_upsert_relationship(keyword, rel)
                logger.info(f"Neo4j: persisted graph for '{keyword}'")
            except Exception as e:
                logger.warning(f"Neo4j persistence failed: {e}. Graph stored in NetworkX.")

        logger.info(
            f"Graph for '{keyword}': {graph.number_of_nodes()} nodes, "
            f"{graph.number_of_edges()} edges (backend: {'neo4j' if self.using_neo4j else 'networkx'})"
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
        Reads from Neo4j when configured, falls back to in-memory NetworkX.
        """
        # Route to Neo4j when available
        if self.using_neo4j:
            try:
                data = self._neo4j_get_graph_data(keyword)
                if data["nodes"]:
                    return data
            except Exception as e:
                logger.warning(f"Neo4j read failed ({e}). Falling back to NetworkX.")

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
