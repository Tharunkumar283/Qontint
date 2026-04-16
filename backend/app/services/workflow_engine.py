"""
MODULE 12 — Full Workflow Engine
Orchestrates: User Input → SERP Analysis → Generate → Score → Predict → Publish
With loop-back when Novelty < Threshold.
"""
import logging
import time
from typing import Dict, Optional

from app.services.serp_collector import serp_collector
from app.services.entity_extractor import entity_extractor
from app.services.graph_builder import graph_builder
from app.services.content_analyzer import content_analyzer
from app.services.content_generator import content_generator
from app.services.validation_loop import validation_loop

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """
    Full end-to-end workflow engine.

    Pipeline:
        1. Collect SERP data for keyword
        2. Extract entities from SERP content
        3. Build knowledge graph
        4. Generate content with authority intelligence
        5. Analyze and score content
        6. If Novelty < Threshold: Loop back to step 4
        7. Return final content with analysis

    Purpose: Continuous improvement cycle for publishing-ready content.
    """

    async def run(
        self,
        keyword: str,
        vertical: str = "saas",
        intent: str = "informational",
        guidelines: Optional[str] = None,
        existing_content: Optional[str] = None,
    ) -> Dict:
        """
        Execute the full workflow pipeline.
        Returns complete workflow result with content and analysis.
        """
        start_time = time.time()
        steps = []

        try:
            # ─── Step 1: SERP Collection ──────────────────────────────
            step_start = time.time()
            logger.info(f"[Workflow] Step 1: Collecting SERP data for '{keyword}'")

            serp_results = await serp_collector.collect(
                keyword=keyword,
                vertical=vertical,
            )

            steps.append({
                "step": "SERP Collection",
                "status": "completed",
                "data": {
                    "results_count": len(serp_results),
                    "time_seconds": round(time.time() - step_start, 2),
                },
            })

            # ─── Step 2: Entity Extraction ────────────────────────────
            step_start = time.time()
            logger.info("[Workflow] Step 2: Extracting entities from SERP content")

            all_entities = []
            all_relationships = []

            for result in serp_results:
                content = result.get("content", result.get("snippet", ""))
                if content:
                    entities = entity_extractor.extract_entities(content, vertical)
                    relationships = entity_extractor.extract_relationships(content)
                    all_entities.extend(entities)
                    all_relationships.extend(relationships)

            steps.append({
                "step": "Entity Extraction",
                "status": "completed",
                "data": {
                    "entities_extracted": len(all_entities),
                    "relationships_found": len(all_relationships),
                    "time_seconds": round(time.time() - step_start, 2),
                },
            })

            # ─── Step 3: Knowledge Graph Construction ─────────────────
            step_start = time.time()
            logger.info("[Workflow] Step 3: Building knowledge graph")

            graph = graph_builder.build_graph(
                keyword=keyword,
                entities=all_entities,
                relationships=all_relationships,
            )

            graph_data = graph_builder.get_graph_data(keyword)
            top_entities = graph_builder.get_top_entities(keyword, n=15)

            steps.append({
                "step": "Knowledge Graph Construction",
                "status": "completed",
                "data": {
                    "nodes": graph_data["stats"]["total_nodes"],
                    "edges": graph_data["stats"]["total_edges"],
                    "avg_authority": graph_data["stats"]["avg_authority"],
                    "time_seconds": round(time.time() - step_start, 2),
                },
            })

            # ─── Step 4: Content Generation + Validation Loop ─────────
            step_start = time.time()
            logger.info("[Workflow] Step 4: Generating and validating content")

            if existing_content:
                # Analyze existing content
                analysis = await content_analyzer.analyze(
                    content=existing_content,
                    keyword=keyword,
                    vertical=vertical,
                )
                final_content = existing_content
                iterations = 1
            else:
                # Run validation loop for new content
                loop_result = await validation_loop.run(
                    keyword=keyword,
                    vertical=vertical,
                    intent=intent,
                    guidelines=guidelines,
                )
                final_content = loop_result["final_content"]
                iterations = loop_result["iterations_count"]

                # Final analysis
                analysis = await content_analyzer.analyze(
                    content=final_content,
                    keyword=keyword,
                    vertical=vertical,
                )

            steps.append({
                "step": "Content Generation & Validation",
                "status": "completed",
                "data": {
                    "iterations": iterations,
                    "novelty_score": analysis.get("novelty_score", 0),
                    "predicted_rank": analysis.get("predicted_rank", 20),
                    "pass_fail": analysis.get("pass_fail", "PENDING"),
                    "time_seconds": round(time.time() - step_start, 2),
                },
            })

            # ─── Step 5: Final Scoring ────────────────────────────────
            step_start = time.time()
            logger.info("[Workflow] Step 5: Final scoring and ranking prediction")

            steps.append({
                "step": "Final Scoring",
                "status": "completed",
                "data": {
                    "novelty_score": analysis.get("novelty_score", 0),
                    "predicted_rank": analysis.get("predicted_rank", 20),
                    "confidence_score": analysis.get("confidence_score", 0),
                    "intent_alignment": analysis.get("intent_alignment", 0),
                    "entity_coverage": analysis.get("entity_coverage", 0),
                    "time_seconds": round(time.time() - step_start, 2),
                },
            })

            total_time = time.time() - start_time

            return {
                "keyword": keyword,
                "vertical": vertical,
                "intent": intent,
                "steps_completed": steps,
                "final_content": final_content,
                "final_analysis": analysis,
                "iterations": iterations,
                "total_time_seconds": round(total_time, 2),
                "status": "completed",
            }

        except Exception as e:
            logger.error(f"Workflow error: {e}", exc_info=True)
            steps.append({
                "step": "Error",
                "status": "failed",
                "data": {"error": str(e)},
            })

            return {
                "keyword": keyword,
                "steps_completed": steps,
                "final_content": existing_content or "",
                "final_analysis": {},
                "iterations": 0,
                "total_time_seconds": round(time.time() - start_time, 2),
                "status": "failed",
                "error": str(e),
            }


# Singleton instance
workflow_engine = WorkflowEngine()
