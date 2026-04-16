"""
MODULE 2 — NLP Entity Extraction Engine
Uses spaCy for Named Entity Recognition with SaaS-vertical custom patterns.
"""
import re
import logging
from typing import List, Dict, Tuple, Set
from collections import Counter

logger = logging.getLogger(__name__)

# Domain-specific entity patterns for SaaS vertical
SAAS_ENTITIES = {
    "METRIC": [
        "MRR", "ARR", "CAC", "LTV", "NRR", "ARPU", "ARPA",
        "churn rate", "retention rate", "conversion rate", "burn rate",
        "runway", "gross margin", "net margin", "CAC payback",
        "magic number", "rule of 40", "LTV:CAC ratio",
        "monthly recurring revenue", "annual recurring revenue",
        "customer acquisition cost", "lifetime value",
        "net revenue retention", "average revenue per user",
    ],
    "CONCEPT": [
        "product-led growth", "PLG", "sales-led growth", "SLG",
        "freemium", "free trial", "usage-based pricing", "tiered pricing",
        "flat-rate pricing", "per-user pricing", "value-based pricing",
        "expansion revenue", "upsell", "cross-sell", "downsell",
        "feature gating", "paywall", "pricing page", "pricing tier",
        "onboarding", "customer success", "customer health score",
        "product-market fit", "go-to-market", "GTM",
        "total addressable market", "TAM", "serviceable addressable market", "SAM",
        "B2B SaaS", "B2C SaaS", "enterprise SaaS", "SMB",
        "vertical SaaS", "horizontal SaaS",
        "API", "SDK", "webhook", "integration",
        "SSO", "SAML", "RBAC", "SOC 2", "GDPR", "HIPAA",
        "microservices", "multi-tenant", "single-tenant",
        "CI/CD", "DevOps", "infrastructure",
    ],
    "STRATEGY": [
        "A/B testing", "pricing experiment", "cohort analysis",
        "customer segmentation", "persona", "ideal customer profile", "ICP",
        "land and expand", "bottoms-up adoption", "top-down sales",
        "content marketing", "SEO", "demand generation",
        "account-based marketing", "ABM", "inbound marketing",
        "outbound sales", "cold outreach", "warm intro",
    ],
}


class EntityExtractor:
    """
    Extracts named entities, keywords, topics, concepts, and relationships
    from text content using spaCy NLP and domain-specific patterns.
    """

    def __init__(self):
        self._nlp = None
        self._initialized = False

    def _ensure_initialized(self):
        """Lazy-load spaCy model."""
        if not self._initialized:
            try:
                import spacy
                try:
                    self._nlp = spacy.load("en_core_web_sm")
                except OSError:
                    logger.warning("spaCy model not found. Using basic extraction.")
                    self._nlp = None
            except ImportError:
                logger.warning("spaCy not installed. Using basic extraction.")
                self._nlp = None
            self._initialized = True

    def extract_entities(self, text: str, vertical: str = "saas") -> List[Dict]:
        """
        Extract all entities from text.
        Returns list of {text, type, frequency, positions}.
        """
        self._ensure_initialized()

        entities = []
        entity_counter = Counter()

        # 1. spaCy NER extraction
        if self._nlp:
            doc = self._nlp(text)
            for ent in doc.ents:
                key = (ent.text.strip(), ent.label_)
                entity_counter[key] += 1

        # 2. Domain-specific entity extraction
        domain_entities = SAAS_ENTITIES if vertical == "saas" else {}
        text_lower = text.lower()
        for entity_type, patterns in domain_entities.items():
            for pattern in patterns:
                count = text_lower.count(pattern.lower())
                if count > 0:
                    key = (pattern, entity_type)
                    entity_counter[key] += count

        # 3. Keyword extraction (TF-based)
        keywords = self._extract_keywords(text)
        for kw, freq in keywords:
            key = (kw, "KEYWORD")
            if key not in entity_counter:
                entity_counter[key] += freq

        # Compile results
        for (text_val, etype), freq in entity_counter.most_common():
            if len(text_val) > 1 and not text_val.isdigit():
                entities.append({
                    "text": text_val,
                    "type": etype,
                    "frequency": freq,
                })

        return entities

    def extract_relationships(self, text: str) -> List[Dict]:
        """
        Extract entity relationships using dependency parsing.
        Returns list of {source, target, relationship, context}.
        """
        self._ensure_initialized()
        relationships = []

        if not self._nlp:
            return self._extract_relationships_basic(text)

        doc = self._nlp(text)

        # Extract subject-verb-object triples
        for sent in doc.sents:
            subjects = []
            objects = []
            verb = None

            for token in sent:
                if token.dep_ in ("nsubj", "nsubjpass") and token.text.strip():
                    subjects.append(token.text)
                elif token.dep_ in ("dobj", "pobj", "attr") and token.text.strip():
                    objects.append(token.text)
                elif token.pos_ == "VERB" and token.dep_ == "ROOT":
                    verb = token.lemma_

            if subjects and objects and verb:
                for subj in subjects:
                    for obj in objects:
                        relationships.append({
                            "source": subj,
                            "target": obj,
                            "relationship": verb,
                            "context": sent.text[:100],
                        })

        # Extract entity co-occurrences (entities appearing in same sentence)
        for sent in doc.sents:
            sent_ents = [ent.text for ent in sent.ents]
            for i in range(len(sent_ents)):
                for j in range(i + 1, len(sent_ents)):
                    relationships.append({
                        "source": sent_ents[i],
                        "target": sent_ents[j],
                        "relationship": "co_occurs_with",
                        "context": sent.text[:100],
                    })

        return relationships

    def _extract_relationships_basic(self, text: str) -> List[Dict]:
        """Basic relationship extraction without spaCy."""
        relationships = []
        sentences = text.split(".")

        for sent in sentences:
            words = sent.strip().split()
            # Look for patterns like "X is/are Y" or "X includes Y"
            for i, word in enumerate(words):
                if word.lower() in ("is", "are", "includes", "uses", "requires", "enables"):
                    if i > 0 and i < len(words) - 1:
                        relationships.append({
                            "source": words[i - 1],
                            "target": words[i + 1],
                            "relationship": word.lower(),
                            "context": sent.strip()[:100],
                        })
        return relationships

    def _extract_keywords(self, text: str, top_n: int = 20) -> List[Tuple[str, int]]:
        """Extract keywords using term frequency."""
        # Common stopwords
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "shall", "can", "need", "dare", "ought",
            "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
            "as", "into", "through", "during", "before", "after", "above", "below",
            "between", "out", "off", "over", "under", "again", "further", "then",
            "once", "here", "there", "when", "where", "why", "how", "all", "each",
            "every", "both", "few", "more", "most", "other", "some", "such", "no",
            "nor", "not", "only", "own", "same", "so", "than", "too", "very",
            "and", "but", "or", "yet", "it", "its", "this", "that", "these",
            "those", "i", "me", "my", "we", "our", "you", "your", "he", "him",
            "she", "her", "they", "them", "their", "what", "which", "who", "whom",
        }

        # Tokenize and filter
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        filtered = [w for w in words if w not in stopwords]

        counter = Counter(filtered)
        return counter.most_common(top_n)

    def calculate_entity_coverage(
        self,
        content_entities: List[Dict],
        serp_entities: List[Dict],
    ) -> float:
        """
        Calculate how well content covers SERP entities.
        Returns coverage score (0-1).
        """
        if not serp_entities:
            return 0.0

        content_set = {e["text"].lower() for e in content_entities}
        serp_set = {e["text"].lower() for e in serp_entities}

        if not serp_set:
            return 0.0

        overlap = content_set & serp_set
        return len(overlap) / len(serp_set)


# Singleton instance
entity_extractor = EntityExtractor()
