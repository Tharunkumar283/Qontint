"""
MODULE 10 — Iterative Validation Loop
Generate → Score → Improve → Regenerate until Novelty >= 0.35
"""
import logging
import time
from typing import Dict, Optional, List

from app.services.content_generator import content_generator
from app.services.content_analyzer import content_analyzer

logger = logging.getLogger(__name__)


class ValidationLoop:
    """
    Implements Generate → Score → Improve → Regenerate workflow.
    Repeats until content meets novelty threshold or max iterations reached.

    Quality Gate: Novelty ≥ 0.35
    Max Iterations: 5
    """

    def __init__(self, max_iterations: int = 5, novelty_threshold: float = 0.35):
        self.max_iterations = max_iterations
        self.novelty_threshold = novelty_threshold

    async def run(
        self,
        keyword: str,
        vertical: str = "saas",
        intent: str = "informational",
        initial_content: Optional[str] = None,
        guidelines: Optional[str] = None,
    ) -> Dict:
        """
        Run the iterative validation loop.
        Returns the best content that passes quality gates.
        """
        start_time = time.time()
        iterations = []
        best_content = initial_content
        best_score = 0.0

        for i in range(self.max_iterations):
            iteration_start = time.time()
            logger.info(f"Validation Loop — Iteration {i + 1}/{self.max_iterations}")

            # Generate content (or use provided content on first iteration)
            if best_content and i == 0:
                content = best_content
            else:
                # Build improvement context from previous analysis
                improvement_guidelines = guidelines or ""
                if iterations:
                    last = iterations[-1]
                    missing = last.get("analysis", {}).get("missing_entities", [])
                    recs = last.get("analysis", {}).get("recommendations", [])

                    if missing:
                        missing_text = ", ".join(e["text"] for e in missing[:5])
                        improvement_guidelines += (
                            f"\nIncorporate these missing entities: {missing_text}"
                        )
                    if recs:
                        rec_text = " ".join(r.get("suggestion", "") for r in recs[:3])
                        improvement_guidelines += f"\n{rec_text}"

                generation = await content_generator.generate(
                    keyword=keyword,
                    vertical=vertical,
                    intent=intent,
                    authority_entities=last.get("analysis", {}).get("entities_found", []) if iterations else None,
                    missing_entities=last.get("analysis", {}).get("missing_entities", []) if iterations else None,
                    guidelines=improvement_guidelines,
                )
                content = generation.get("content", "")

            # Analyze content
            analysis = await content_analyzer.analyze(
                content=content,
                keyword=keyword,
                vertical=vertical,
            )

            novelty = analysis.get("novelty_score", 0.0)
            predicted_rank = analysis.get("predicted_rank", 20)

            iteration_data = {
                "iteration": i + 1,
                "novelty_score": novelty,
                "predicted_rank": predicted_rank,
                "pass_fail": analysis.get("pass_fail", "FAIL"),
                "content_length": len(content),
                "word_count": len(content.split()),
                "time_seconds": round(time.time() - iteration_start, 2),
                "analysis": analysis,
            }
            iterations.append(iteration_data)

            # Track best content
            if novelty > best_score:
                best_score = novelty
                best_content = content

            # Check if content passes quality gate
            if novelty >= self.novelty_threshold:
                logger.info(
                    f"✓ Content passed validation at iteration {i + 1} "
                    f"(Novelty: {novelty:.4f} >= {self.novelty_threshold})"
                )
                break
            else:
                logger.info(
                    f"✗ Iteration {i + 1} failed "
                    f"(Novelty: {novelty:.4f} < {self.novelty_threshold}). "
                    f"{'Retrying...' if i < self.max_iterations - 1 else 'Max iterations reached.'}"
                )

        total_time = time.time() - start_time

        return {
            "keyword": keyword,
            "vertical": vertical,
            "intent": intent,
            "final_content": best_content,
            "final_novelty": best_score,
            "passed": best_score >= self.novelty_threshold,
            "iterations_count": len(iterations),
            "max_iterations": self.max_iterations,
            "iterations": iterations,
            "total_time_seconds": round(total_time, 2),
        }


# Singleton instance
validation_loop = ValidationLoop()
