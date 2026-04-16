"""POST /api/v1/generate — AI content generation endpoint."""
from fastapi import APIRouter
from app.schemas import GenerateRequest, GenerateResponse, EntityResponse
from app.services.content_generator import content_generator
from app.services.graph_builder import graph_builder
from app.services.workflow_engine import workflow_engine

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
async def generate_content(request: GenerateRequest):
    """
    Generate SEO-optimized content using authority intelligence.
    Uses Ollama (free local LLM) or template-based generation.
    """
    # Get authority entities from graph
    authority_entities = []
    missing_entities = []
    graph_insights = None

    if request.use_authority_entities:
        top_entities = graph_builder.get_top_entities(request.keyword, n=15)
        authority_entities = top_entities
        graph_insights = graph_builder.get_graph_data(request.keyword)

    result = await content_generator.generate(
        keyword=request.keyword,
        vertical=request.vertical.value,
        intent=request.intent.value,
        authority_entities=authority_entities,
        missing_entities=missing_entities,
        guidelines=request.guidelines,
        graph_insights=graph_insights,
    )

    return GenerateResponse(
        content=result.get("content", ""),
        keyword=request.keyword,
        intent=request.intent.value,
        entities_used=result.get("entities_used", []),
        authority_entities=[
            EntityResponse(
                text=e.get("text", ""),
                type=e.get("type", "UNKNOWN"),
                authority_score=e.get("authority_score", 0),
                frequency=e.get("frequency", 1),
            )
            for e in result.get("authority_entities", [])
        ],
        estimated_novelty=result.get("estimated_novelty", 0),
        word_count=result.get("word_count", 0),
    )


@router.post("/workflow")
async def run_workflow(request: GenerateRequest):
    """
    Run the full workflow: SERP → Generate → Score → Predict → Publish.
    Uses iterative validation loop to ensure quality.
    """
    result = await workflow_engine.run(
        keyword=request.keyword,
        vertical=request.vertical.value,
        intent=request.intent.value,
        guidelines=request.guidelines,
    )
    return result
