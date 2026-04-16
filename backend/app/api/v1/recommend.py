"""POST /api/v1/recommend — Entity recommendation endpoint."""
from fastapi import APIRouter
from app.schemas import RecommendRequest, RecommendResponse, RecommendationItem
from app.services.entity_extractor import entity_extractor
from app.services.recommendation_engine import recommendation_engine
from app.services.novelty_scorer import novelty_scorer
from app.services.graph_builder import graph_builder

router = APIRouter()


@router.post("/recommend", response_model=RecommendResponse)
async def get_recommendations(request: RecommendRequest):
    """
    Get entity recommendations for improving content.
    Returns top 3-5 missing high-authority entities with context.
    """
    # Extract content entities
    content_entities = entity_extractor.extract_entities(
        request.content, request.vertical.value
    )
    content_relationships = entity_extractor.extract_relationships(request.content)

    # Get SERP entities
    graph_data = graph_builder.get_graph_data(request.keyword)
    serp_entities = [
        {"text": n["label"], "type": n["type"], "frequency": n["frequency"]}
        for n in graph_data.get("nodes", [])
    ]
    serp_relationships = [
        {"source": e["source"], "target": e["target"], "relationship": e["relationship"]}
        for e in graph_data.get("edges", [])
    ]

    # Calculate current novelty
    novelty_result = novelty_scorer.score(
        content_entities, serp_entities,
        content_relationships, serp_relationships,
    )

    current_novelty = novelty_result["novelty_score"]

    # Get recommendations
    recs = recommendation_engine.recommend(
        keyword=request.keyword,
        content_entities=content_entities,
        novelty_score=current_novelty,
    )

    # Estimate potential novelty gain
    potential_gain = sum(r.get("potential_novelty_gain", 0) for r in recs[:5])

    return RecommendResponse(
        keyword=request.keyword,
        current_novelty=current_novelty,
        recommendations=[
            RecommendationItem(
                entity=r["entity"],
                entity_type=r["entity_type"],
                authority_score=r["authority_score"],
                relevance_score=r.get("relevance_score", 0),
                suggestion=r["suggestion"],
                context=r["context"],
            )
            for r in recs
        ],
        potential_novelty_gain=round(potential_gain, 4),
    )
