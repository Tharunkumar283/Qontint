"""POST /api/v1/predict — Ranking prediction endpoint."""
from fastapi import APIRouter
from app.schemas import PredictRequest, PredictResponse, FeatureBreakdown
from app.services.entity_extractor import entity_extractor
from app.services.graph_builder import graph_builder
from app.services.ranking_predictor import ranking_predictor

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
async def predict_ranking(request: PredictRequest):
    """
    Predict SERP ranking position for content.
    Returns predicted position (1-20) and confidence score.
    """
    # Extract content entities
    content_entities = entity_extractor.extract_entities(
        request.content, request.vertical.value
    )
    content_relationships = entity_extractor.extract_relationships(request.content)

    # Get SERP entities from graph
    graph_data = graph_builder.get_graph_data(request.keyword)
    serp_entities = [
        {"text": n["label"], "type": n["type"], "frequency": n["frequency"]}
        for n in graph_data.get("nodes", [])
    ]

    # Calculate features
    entity_coverage = entity_extractor.calculate_entity_coverage(
        content_entities, serp_entities
    )
    relationship_completeness = graph_builder.get_relationship_completeness(
        request.keyword, content_relationships
    )

    # Calculate authority score
    top_entities = graph_builder.get_top_entities(request.keyword, n=50)
    content_entity_texts = {e["text"].lower() for e in content_entities}
    authority_scores = [
        e["authority_score"]
        for e in top_entities
        if e["text"].lower() in content_entity_texts
    ]
    avg_authority = sum(authority_scores) / len(authority_scores) if authority_scores else 0.3

    # Content quality
    content_quality = ranking_predictor.calculate_content_quality(request.content)

    # Predict
    prediction = ranking_predictor.predict(
        entity_coverage=entity_coverage,
        relationship_completeness=relationship_completeness,
        authority_score=avg_authority,
        content_quality=content_quality,
    )

    # Determine pass/fail
    pass_fail = "PASS" if prediction["predicted_position"] <= 10 else "FAIL"

    return PredictResponse(
        predicted_position=prediction["predicted_position"],
        confidence=prediction["confidence"],
        features=FeatureBreakdown(
            entity_coverage=round(entity_coverage, 4),
            relationship_completeness=round(relationship_completeness, 4),
            authority_score=round(avg_authority, 4),
            content_quality=round(content_quality, 4),
        ),
        pass_fail=pass_fail,
    )
