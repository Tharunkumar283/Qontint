"""POST /api/v1/serp/collect — SERP Intelligence Collection endpoint."""
from fastapi import APIRouter
from app.schemas import SerpCollectRequest, SerpCollectResponse, SerpResultResponse
from app.services.serp_collector import serp_collector
from app.services.entity_extractor import entity_extractor
from app.services.graph_builder import graph_builder

router = APIRouter()


@router.post("/serp/collect", response_model=SerpCollectResponse)
async def collect_serp(request: SerpCollectRequest):
    """
    Collect SERP data for a keyword and build the knowledge graph.
    This is typically the first step in the analysis pipeline.
    """
    # Collect SERP results
    results = await serp_collector.collect(
        keyword=request.keyword,
        vertical=request.vertical.value,
    )

    # Extract entities and relationships from all SERP content
    all_entities = []
    all_relationships = []

    for result in results:
        content = result.get("content", result.get("snippet", ""))
        if content:
            entities = entity_extractor.extract_entities(content, request.vertical.value)
            relationships = entity_extractor.extract_relationships(content)
            all_entities.extend(entities)
            all_relationships.extend(relationships)

    # Build/update knowledge graph
    graph_builder.build_graph(
        keyword=request.keyword,
        entities=all_entities,
        relationships=all_relationships,
    )

    return SerpCollectResponse(
        keyword=request.keyword,
        vertical=request.vertical.value,
        total_results=len(results),
        results=[
            SerpResultResponse(
                position=r.get("position", 0),
                url=r.get("url", ""),
                title=r.get("title"),
                snippet=r.get("snippet"),
                content_length=len(r.get("content", "")),
            )
            for r in results
        ],
        collected_at=results[0].get("collected_at", "") if results else "",
    )
