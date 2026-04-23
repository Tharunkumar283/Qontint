"""
MODULE 9 — AI Content Generation Engine
Priority: Claude API (Anthropic) → Ollama (local) → Template
Generates SEO-optimized content using authority intelligence.
"""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ContentGenerator:
    """
    Generates intelligent, SEO-optimized content using:
    - Claude API (Anthropic) — primary [set ANTHROPIC_API_KEY]
    - Ollama (free local LLM) — secondary fallback
    - Template-based generation — final fallback

    Priority order: Claude → Ollama → Template
    """

    def __init__(self):
        self._ollama_available = None
        self._claude_available = None

    async def _check_claude(self) -> bool:
        """Check if Anthropic Claude API is available."""
        if self._claude_available is not None:
            return self._claude_available

        try:
            import anthropic
            import os
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")
            if not api_key or api_key.startswith("sk-ant-YOUR"):
                self._claude_available = False
                return False
            self._claude_available = True
            logger.info("Claude API is available for content generation.")
        except ImportError:
            self._claude_available = False
            logger.info("anthropic package not installed.")
        return self._claude_available

    async def _check_ollama(self) -> bool:
        """Check if Ollama is available."""
        if self._ollama_available is not None:
            return self._ollama_available
        try:
            import ollama
            ollama.list()
            self._ollama_available = True
            logger.info("Ollama is available for content generation.")
        except Exception:
            self._ollama_available = False
            logger.info("Ollama not available. Will use template generation.")
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
        Priority: Claude API → Ollama → Template
        """
        # Try Claude first
        if await self._check_claude():
            try:
                return await self._generate_claude(
                    keyword, vertical, intent,
                    authority_entities, missing_entities, guidelines, graph_insights,
                )
            except Exception as e:
                logger.warning(f"Claude generation failed: {e}. Trying Ollama.")

        # Try Ollama
        if await self._check_ollama():
            try:
                return await self._generate_ollama(
                    keyword, vertical, intent,
                    authority_entities, missing_entities, guidelines, graph_insights,
                )
            except Exception as e:
                logger.warning(f"Ollama generation failed: {e}. Using template.")

        # Fallback: template
        return self._generate_template(
            keyword, vertical, intent,
            authority_entities, missing_entities, guidelines,
        )

    async def _generate_claude(
        self,
        keyword: str,
        vertical: str,
        intent: str,
        authority_entities: Optional[List[Dict]],
        missing_entities: Optional[List[Dict]],
        guidelines: Optional[str],
        graph_insights: Optional[Dict],
    ) -> Dict:
        """Generate content using Anthropic Claude API."""
        import anthropic
        import os

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        client = anthropic.Anthropic(api_key=api_key)

        prompt = self._build_prompt(
            keyword, vertical, intent,
            authority_entities, missing_entities, guidelines, graph_insights,
        )

        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=2048,
            system=(
                f"You are an expert SEO content writer specializing in the {vertical} industry. "
                "Write comprehensive, authoritative content that naturally incorporates the specified "
                "entities and concepts. Use markdown formatting with H2 and H3 headers, bullet lists, "
                "and structured sections. Be informative and avoid generic filler text."
            ),
            messages=[{"role": "user", "content": prompt}],
        )

        content = message.content[0].text if message.content else ""

        entities_used = []
        if authority_entities:
            content_lower = content.lower()
            entities_used = [e["text"] for e in authority_entities if e["text"].lower() in content_lower]

        return {
            "content": content,
            "keyword": keyword,
            "intent": intent,
            "entities_used": entities_used,
            "authority_entities": authority_entities or [],
            "estimated_novelty": 0.65,
            "word_count": len(content.split()),
            "generation_method": "claude",
            "model": "claude-3-5-haiku-20241022",
        }

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

        prompt = self._build_prompt(
            keyword, vertical, intent,
            authority_entities, missing_entities, guidelines, graph_insights,
        )

        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are an expert SEO content writer specializing in the "
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
            entities_used = [e["text"] for e in authority_entities if e["text"].lower() in content_lower]

        return {
            "content": content,
            "keyword": keyword,
            "intent": intent,
            "entities_used": entities_used,
            "authority_entities": authority_entities or [],
            "estimated_novelty": 0.5,
            "word_count": len(content.split()),
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
                f"\nIMPORTANT — Naturally incorporate these high-authority entities: {entity_list}"
            )

        if missing_entities:
            missing_list = ", ".join(e["text"] for e in missing_entities[:5])
            prompt_parts.append(f"\nAlso include: {missing_list}")

        if graph_insights:
            top = graph_insights.get("stats", {}).get("top_entities", [])
            if top:
                insights = ", ".join(e["text"] for e in top[:5])
                prompt_parts.append(f"\nTop authority entities in this space: {insights}")

        intent_instructions = {
            "informational": "Focus on educating with definitions, examples, and step-by-step guides.",
            "transactional": "Include clear calls-to-action, pricing information, and conversion-focused content.",
            "commercial": "Provide comparisons, pros/cons, and evaluation criteria.",
            "navigational": "Focus on product features, getting-started guides, and direct links.",
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
        """Template-based content generation fallback."""
        all_entities = []
        if authority_entities:
            all_entities.extend(authority_entities)
        if missing_entities:
            all_entities.extend(missing_entities)

        entity_groups = {}
        for e in all_entities:
            etype = e.get("type", "CONCEPT")
            if etype not in entity_groups:
                entity_groups[etype] = []
            entity_groups[etype].append(e["text"])

        sections = []

        sections.append(f"# The Complete Guide to {keyword.title()}\n")
        sections.append(
            f"In today's competitive {vertical} landscape, understanding "
            f"{keyword} is essential for success. This comprehensive guide "
            f"covers everything you need to know, from fundamental concepts "
            f"to advanced strategies.\n"
        )

        concepts = entity_groups.get("CONCEPT", [])[:10]
        if concepts:
            sections.append("## Key Concepts\n")
            for concept in concepts:
                sections.append(f"- **{concept}**: A critical element in the {vertical} ecosystem.")
            sections.append("")

        metrics = entity_groups.get("METRIC", [])[:8]
        if metrics:
            sections.append("## Essential Metrics and KPIs\n")
            for metric in metrics:
                sections.append(f"- **{metric}**: A key performance indicator for {keyword}.")
            sections.append("")

        strategies = entity_groups.get("STRATEGY", [])[:6]
        if strategies:
            sections.append("## Proven Strategies\n")
            for i, strategy in enumerate(strategies, 1):
                sections.append(
                    f"### {i}. {strategy}\n\n"
                    f"Implementing {strategy} as part of your {keyword} approach "
                    f"drives measurable results when applied consistently.\n"
                )

        sections.append(f"## Best Practices for {keyword.title()}\n")
        sections.append(
            f"To maximize the impact of your {keyword} strategy, follow these best practices:\n"
        )
        sections.append("1. **Start with data-driven research** — Analyze your market and competitors")
        sections.append("2. **Define clear objectives** — Set measurable goals aligned with your KPIs")
        sections.append("3. **Iterate and improve** — Continuously refine based on results")
        sections.append("4. **Leverage automation** — Use tools to scale efficiently")
        sections.append("5. **Focus on quality** — Prioritize depth and accuracy over volume\n")

        sections.append("## Conclusion\n")
        sections.append(
            f"Mastering {keyword} requires strategic thinking, data-driven decision-making, and "
            f"continuous improvement. By focusing on the key concepts, metrics, and strategies "
            f"outlined in this guide, you can build a strong foundation for success in the {vertical} industry."
        )

        content = "\n".join(sections)

        entities_used = [e["text"] for e in all_entities if e["text"].lower() in content.lower()]

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
