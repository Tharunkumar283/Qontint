"""Export API endpoint — export analysis results as JSON or CSV."""
import csv
import io
import json
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
from app.services.content_analyzer import content_analyzer
from app.services.serp_collector import serp_collector
from app.services.graph_builder import graph_builder
from pydantic import BaseModel

router = APIRouter()


class ExportRequest(BaseModel):
    keyword: str
    vertical: Optional[str] = "saas"
    content: Optional[str] = ""


@router.post("/export/json")
async def export_json(request: ExportRequest):
    """Export full analysis as a JSON object."""
    analysis = await content_analyzer.analyze(
        content=request.content or f"Analysis export for: {request.keyword}",
        keyword=request.keyword,
        vertical=request.vertical or "saas",
    )
    graph_data = graph_builder.get_graph_data(request.keyword)

    export = {
        "meta": {
            "keyword": request.keyword,
            "vertical": request.vertical,
            "exported_at": analysis.get("analyzed_at", ""),
            "tool": "Qontint — Semantic Authority OS",
            "version": "1.0.0",
        },
        "scores": {
            "novelty_score": analysis.get("novelty_score", 0),
            "entity_novelty": analysis.get("entity_novelty", 0),
            "relationship_novelty": analysis.get("relationship_novelty", 0),
            "semantic_diversity": analysis.get("semantic_diversity", 0),
            "predicted_rank": analysis.get("predicted_rank", 20),
            "confidence_score": analysis.get("confidence_score", 0),
            "intent_alignment": analysis.get("intent_alignment", 0),
            "entity_coverage": analysis.get("entity_coverage", 0),
            "relationship_completeness": analysis.get("relationship_completeness", 0),
            "authority_score": analysis.get("authority_score", 0),
            "content_quality": analysis.get("content_quality", 0),
            "pass_fail": analysis.get("pass_fail", "PENDING"),
        },
        "entities": {
            "found": analysis.get("entities_found", []),
            "missing": analysis.get("missing_entities", []),
        },
        "knowledge_graph": {
            "nodes": graph_data.get("nodes", [])[:50],
            "edges": graph_data.get("edges", [])[:100],
            "stats": graph_data.get("stats", {}),
        },
        "recommendations": analysis.get("recommendations", []),
    }

    return JSONResponse(
        content=export,
        headers={
            "Content-Disposition": f'attachment; filename="qontint-{request.keyword.replace(" ", "-")}.json"'
        },
    )


@router.post("/export/csv")
async def export_csv(request: ExportRequest):
    """Export entity analysis as a CSV file."""
    analysis = await content_analyzer.analyze(
        content=request.content or f"Analysis export for: {request.keyword}",
        keyword=request.keyword,
        vertical=request.vertical or "saas",
    )

    output = io.StringIO()
    writer = csv.writer(output)

    # Summary section
    writer.writerow(["QONTINT ANALYSIS EXPORT"])
    writer.writerow(["Keyword", request.keyword])
    writer.writerow(["Vertical", request.vertical])
    writer.writerow(["Exported At", analysis.get("analyzed_at", "")])
    writer.writerow([])

    # Scores
    writer.writerow(["SCORES"])
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Novelty Score", f"{analysis.get('novelty_score', 0):.4f}"])
    writer.writerow(["Predicted Rank", analysis.get("predicted_rank", 20)])
    writer.writerow(["Confidence", f"{analysis.get('confidence_score', 0):.4f}"])
    writer.writerow(["Intent Alignment", f"{analysis.get('intent_alignment', 0):.4f}"])
    writer.writerow(["Entity Coverage", f"{analysis.get('entity_coverage', 0):.4f}"])
    writer.writerow(["Authority Score", f"{analysis.get('authority_score', 0):.4f}"])
    writer.writerow(["Content Quality", f"{analysis.get('content_quality', 0):.4f}"])
    writer.writerow(["Pass/Fail", analysis.get("pass_fail", "PENDING")])
    writer.writerow([])

    # Entities found
    writer.writerow(["ENTITIES FOUND"])
    writer.writerow(["#", "Entity", "Type", "Frequency", "Authority Score"])
    for i, e in enumerate(analysis.get("entities_found", []), 1):
        writer.writerow([i, e.get("text"), e.get("type"), e.get("frequency"), f"{e.get('authority_score', 0):.4f}"])
    writer.writerow([])

    # Missing entities (recommendations)
    writer.writerow(["MISSING ENTITIES (Recommendations)"])
    writer.writerow(["#", "Entity", "Type", "Authority Score"])
    for i, e in enumerate(analysis.get("missing_entities", []), 1):
        writer.writerow([i, e.get("text"), e.get("type"), f"{e.get('authority_score', 0):.4f}"])

    output.seek(0)
    filename = f"qontint-{request.keyword.replace(' ', '-')}.csv"

    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
