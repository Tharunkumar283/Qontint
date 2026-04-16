"""
MODULE 9 — AI Content Generation Engine
Uses Ollama (free, local LLM) with intelligent mock fallback.
Generates SEO-optimized content using authority intelligence.
"""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ContentGenerator:
    """
    Generates intelligent, SEO-optimized content using:
    - Authority entities from knowledge graph
    - Intent alignment
    - Relationship patterns
    - Domain-specific knowledge (SaaS vertical)

    Supports:
    - Ollama (free local LLM) — primary
    - Template-based generation — fallback
    """

    def __init__(self):
        self._ollama_available = None

    async def _check_ollama(self) -> bool:
        """Check if Ollama is available."""
        if self._ollama_available is not None:
            return self._ollama_available

        try:
            import ollama
            models = ollama.list()
            self._ollama_available = True
            logger.info("Ollama is available for content generation.")
        except Exception:
            self._ollama_available = False
            logger.info("Ollama not available. Using template-based generation.")

        return self._ollama_available

    async def generate(
        self,
        keyword: str,
        vertical: str = "saas",
        intent: str = "informational",
        authority_entities: Optional[List[Dict]] = None,
        missing_entities: Optional[List[Dict]] = None,
        guidelines: Optional[str] = None,
        graph_insights: Optional[Dict] = None,
    ) -> Dict:
        """
        Generate optimized SEO content.
        Tries Ollama LLM first, falls back to template-based generation.
        """
        if await self._check_ollama():
            try:
                return await self._generate_ollama(
                    keyword, vertical, intent,
                    authority_entities, missing_entities,
                    guidelines, graph_insights,
                )
            except Exception as e:
                logger.warning(f"Ollama generation failed: {e}. Using template.")

        return self._generate_template(
            keyword, vertical, intent,
            authority_entities, missing_entities,
            guidelines,
        )

    async def _generate_ollama(
        self,
        keyword: str,
        vertical: str,
        intent: str,
        authority_entities: Optional[List[Dict]],
        missing_entities: Optional[List[Dict]],
        guidelines: Optional[str],
        graph_insights: Optional[Dict],
    ) -> Dict:
        """Generate content using Ollama LLM."""
        import ollama
        from app.core import settings

        # Build intelligence-informed prompt
        prompt = self._build_prompt(
            keyword, vertical, intent,
            authority_entities, missing_entities,
            guidelines, graph_insights,
        )

        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert SEO content writer specializing in the "
                        f"{vertical} industry. Write comprehensive, authoritative content "
                        "that naturally incorporates the specified entities and concepts. "
                        "Use markdown formatting with headers, lists, and structured sections."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )

        content = response.get("message", {}).get("content", "")

        entities_used = []
        if authority_entities:
            content_lower = content.lower()
            entities_used = [
                e["text"] for e in authority_entities
                if e["text"].lower() in content_lower
            ]

        word_count = len(content.split())

        return {
            "content": content,
            "keyword": keyword,
            "intent": intent,
            "entities_used": entities_used,
            "authority_entities": authority_entities or [],
            "estimated_novelty": 0.5,
            "word_count": word_count,
            "generation_method": "ollama",
        }

    def _build_prompt(
        self,
        keyword: str,
        vertical: str,
        intent: str,
        authority_entities: Optional[List[Dict]],
        missing_entities: Optional[List[Dict]],
        guidelines: Optional[str],
        graph_insights: Optional[Dict],
    ) -> str:
        """Build an intelligence-informed prompt for the LLM."""
        prompt_parts = [
            f"Write a comprehensive, SEO-optimized article about: {keyword}",
            f"\nTarget Intent: {intent}",
            f"Industry Vertical: {vertical}",
        ]

        if authority_entities:
            entity_list = ", ".join(e["text"] for e in authority_entities[:15])
            prompt_parts.append(
                f"\nIMPORTANT - You MUST naturally incorporate these high-authority "
                f"entities throughout the article: {entity_list}"
            )

        if missing_entities:
            missing_list = ", ".join(e["text"] for e in missing_entities[:5])
            prompt_parts.append(
                f"\nAlso include these recommended entities for better ranking: {missing_list}"
            )

        if graph_insights:
            top = graph_insights.get("stats", {}).get("top_entities", [])
            if top:
                insights = ", ".join(e["text"] for e in top[:5])
                prompt_parts.append(
                    f"\nTop authority entities in this topic space: {insights}"
                )

        intent_instructions = {
            "informational": "Focus on educating the reader with definitions, examples, and step-by-step guides.",
            "transactional": "Include clear calls-to-action, pricing information, and conversion-focused content.",
            "commercial": "Provide comparisons, pros/cons, and evaluation criteria to help readers make decisions.",
            "navigational": "Focus on product features, getting started guides, and direct links.",
        }
        prompt_parts.append(f"\nContent Style: {intent_instructions.get(intent, '')}")

        if guidelines:
            prompt_parts.append(f"\nAdditional Guidelines: {guidelines}")

        prompt_parts.append(
            "\nRequirements:"
            "\n- Use markdown with H2 and H3 headers"
            "\n- Include at least 5 sections"
            "\n- Write 1000-2000 words"
            "\n- Include practical examples"
            "\n- Add a conclusion section"
            "\n- Be authoritative, not generic"
        )

        return "\n".join(prompt_parts)

    def _generate_template(
        self,
        keyword: str,
        vertical: str,
        intent: str,
        authority_entities: Optional[List[Dict]],
        missing_entities: Optional[List[Dict]],
        guidelines: Optional[str],
    ) -> Dict:
        """
        Template-based content generation fallback.
        Uses authority intelligence to generate structured content.
        """
        all_entities = []
        if authority_entities:
            all_entities.extend(authority_entities)
        if missing_entities:
            all_entities.extend(missing_entities)

        # Group entities by type
        entity_groups = {}
        for e in all_entities:
            etype = e.get("type", "CONCEPT")
            if etype not in entity_groups:
                entity_groups[etype] = []
            entity_groups[etype].append(e["text"])

        # Build sections based on entity groups
        sections = []

        # Introduction
        sections.append(f"# The Complete Guide to {keyword.title()}\n")
        sections.append(
            f"In today's competitive {vertical} landscape, understanding "
            f"{keyword} is essential for success. This comprehensive guide "
            f"covers everything you need to know, from fundamental concepts "
            f"to advanced strategies.\n"
        )

        # Key Concepts section
        concepts = entity_groups.get("CONCEPT", [])[:10]
        if concepts:
            sections.append("## Key Concepts\n")
            sections.append(
                f"When it comes to {keyword}, several core concepts form the foundation "
                f"of a successful strategy:\n"
            )
            for concept in concepts:
                sections.append(
                    f"- **{concept}**: A critical element in the {vertical} ecosystem "
                    f"that directly impacts your approach to {keyword}."
                )
            sections.append("")

        # Metrics section
        metrics = entity_groups.get("METRIC", [])[:8]
        if metrics:
            sections.append("## Essential Metrics and KPIs\n")
            sections.append(
                f"Tracking the right metrics is crucial when implementing {keyword} strategies:\n"
            )
            for metric in metrics:
                sections.append(
                    f"- **{metric}**: A key performance indicator that measures the "
                    f"effectiveness of your {keyword} implementation."
                )
            sections.append("")

        # Strategy section
        strategies = entity_groups.get("STRATEGY", [])[:6]
        if strategies:
            sections.append("## Proven Strategies\n")
            sections.append(
                f"The most successful approaches to {keyword} involve a combination "
                f"of tested strategies:\n"
            )
            for i, strategy in enumerate(strategies, 1):
                sections.append(
                    f"### {i}. {strategy}\n\n"
                    f"Implementing {strategy} as part of your {keyword} approach "
                    f"can significantly improve outcomes. Leading {vertical} companies "
                    f"have demonstrated that {strategy} drives measurable results "
                    f"when applied consistently.\n"
                )

        # Organizations section
        orgs = entity_groups.get("ORG", [])[:5]
        if orgs:
            sections.append("## Industry Leaders\n")
            sections.append(
                f"Several organizations have set the standard for {keyword}:\n"
            )
            for org in orgs:
                sections.append(f"- **{org}**: A recognized leader in the space.")
            sections.append("")

        # Best Practices
        sections.append(f"## Best Practices for {keyword.title()}\n")
        sections.append(
            f"To maximize the impact of your {keyword} strategy, follow these "
            f"best practices:\n"
        )
        sections.append(f"1. **Start with data-driven research** — Analyze your market and competitors")
        sections.append(f"2. **Define clear objectives** — Set measurable goals aligned with your KPIs")
        sections.append(f"3. **Iterate and improve** — Continuously refine your approach based on results")
        sections.append(f"4. **Leverage automation** — Use tools and technology to scale efficiently")
        sections.append(f"5. **Focus on quality** — Prioritize depth and accuracy over volume\n")

        # Conclusion
        sections.append(f"## Conclusion\n")
        sections.append(
            f"Mastering {keyword} is a journey that requires a combination of "
            f"strategic thinking, data-driven decision-making, and continuous improvement. "
            f"By focusing on the key concepts, metrics, and strategies outlined in this guide, "
            f"you can build a strong foundation for success in the {vertical} industry.\n"
        )
        sections.append(
            f"Remember that the most successful {vertical} organizations treat {keyword} "
            f"as an ongoing process rather than a one-time initiative. Start implementing "
            f"these strategies today and measure your progress against the KPIs discussed above."
        )

        content = "\n".join(sections)

        entities_used = [
            e["text"] for e in all_entities
            if e["text"].lower() in content.lower()
        ]

        return {
            "content": content,
            "keyword": keyword,
            "intent": intent,
            "entities_used": entities_used,
            "authority_entities": authority_entities or [],
            "estimated_novelty": 0.45,
            "word_count": len(content.split()),
            "generation_method": "template",
        }


# Singleton instance
content_generator = ContentGenerator()
