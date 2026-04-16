"""POST /api/v1/analyze — Full content analysis endpoint."""
from fastapi import APIRouter
from app.schemas import AnalyzeRequest, AnalyzeResponse, EntityResponse
from app.services.content_analyzer import content_analyzer
from app.services.serp_collector import serp_collector
from app.services.entity_extractor import entity_extractor
from app.services.graph_builder import graph_builder

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_content(request: AnalyzeRequest):
    """
    Run full analysis pipeline on content.
    Extracts entities, scores novelty, predicts ranking, and generates recommendations.
    """
    # Ensure SERP data and graph exist for this keyword
    graph_data = graph_builder.get_graph_data(request.keyword)
    if not graph_data["nodes"]:
        # Auto-collect SERP data if not available
        results = await serp_collector.collect(
            keyword=request.keyword,
            vertical=request.vertical.value,
        )
        all_entities = []
        all_relationships = []
        for result in results:
            content = result.get("content", result.get("snippet", ""))
            if content:
                entities = entity_extractor.extract_entities(content, request.vertical.value)
                relationships = entity_extractor.extract_relationships(content)
                all_entities.extend(entities)
                all_relationships.extend(relationships)

        graph_builder.build_graph(
            keyword=request.keyword,
            entities=all_entities,
            relationships=all_relationships,
        )

    # Run analysis
    result = await content_analyzer.analyze(
        content=request.content,
        keyword=request.keyword,
        vertical=request.vertical.value,
    )

    return AnalyzeResponse(
        keyword=result.get("keyword", request.keyword),
        novelty_score=result.get("novelty_score", 0),
        entity_novelty=result.get("entity_novelty", 0),
        relationship_novelty=result.get("relationship_novelty", 0),
        semantic_diversity=result.get("semantic_diversity", 0),
        predicted_rank=result.get("predicted_rank", 20),
        confidence_score=result.get("confidence_score", 0),
        intent_alignment=result.get("intent_alignment", 0),
        intent_type=result.get("intent_type", "informational"),
        entity_coverage=result.get("entity_coverage", 0),
        relationship_completeness=result.get("relationship_completeness", 0),
        authority_score=result.get("authority_score", 0),
        content_quality=result.get("content_quality", 0),
        pass_fail=result.get("pass_fail", "PENDING"),
        entities_found=[
            EntityResponse(
                text=e.get("text", ""),
                type=e.get("type", "UNKNOWN"),
                authority_score=e.get("authority_score", 0),
                frequency=e.get("frequency", 1),
            )
            for e in result.get("entities_found", [])[:20]
        ],
        missing_entities=[
            EntityResponse(
                text=e.get("text", ""),
                type=e.get("type", "UNKNOWN"),
                authority_score=e.get("authority_score", 0),
                frequency=e.get("frequency", 1),
            )
            for e in result.get("missing_entities", [])[:10]
        ],
        recommendations=result.get("recommendations", []),
        analyzed_at=result.get("analyzed_at", ""),
    )
