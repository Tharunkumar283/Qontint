"""GET /api/v1/graph/{keyword} — Knowledge graph data endpoint."""
from fastapi import APIRouter
from app.schemas import GraphResponse, GraphNode, GraphEdge, GraphStats, EntityResponse
from app.services.graph_builder import graph_builder

router = APIRouter()


@router.get("/graph/{keyword}", response_model=GraphResponse)
async def get_graph(keyword: str):
    """
    Get knowledge graph data for visualization.
    Returns nodes, edges, and graph statistics.
    """
    data = graph_builder.get_graph_data(keyword)

    return GraphResponse(
        keyword=keyword,
        nodes=[
            GraphNode(
                id=n["id"],
                label=n["label"],
                type=n["type"],
                authority=n["authority"],
                frequency=n["frequency"],
                size=n["size"],
            )
            for n in data.get("nodes", [])
        ],
        edges=[
            GraphEdge(
                source=e["source"],
                target=e["target"],
                relationship=e["relationship"],
                weight=e["weight"],
            )
            for e in data.get("edges", [])
        ],
        stats=GraphStats(
            total_nodes=data["stats"].get("total_nodes", 0),
            total_edges=data["stats"].get("total_edges", 0),
            avg_authority=data["stats"].get("avg_authority", 0),
            top_entities=[
                EntityResponse(
                    text=e.get("text", ""),
                    type=e.get("type", "UNKNOWN"),
                    authority_score=e.get("authority_score", 0),
                    frequency=e.get("frequency", 1),
                )
                for e in data["stats"].get("top_entities", [])
            ],
        ),
    )
