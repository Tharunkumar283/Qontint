"""
MODULE 1 — SERP Intelligence Collector
Priority: Ahrefs API → DuckDuckGo → Mock data
Scraping: Playwright (full JS) → httpx + BeautifulSoup → snippet-only
"""
import hashlib
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


# ─── SaaS Vertical Mock SERP Data ────────────────────────────────────

MOCK_SERP_DATA = {
    "saas pricing strategies": [
        {
            "title": "The Ultimate Guide to SaaS Pricing Models in 2025",
            "url": "https://example.com/saas-pricing-guide",
            "snippet": "Explore the most effective SaaS pricing strategies including value-based pricing, tiered pricing, freemium models, and usage-based pricing.",
            "content": """SaaS pricing is one of the most critical decisions for any software company. The right pricing strategy can accelerate growth, improve retention, and maximize revenue.

Key SaaS Pricing Models:

1. Flat-Rate Pricing: A single price for a single product with a fixed set of features. Simple but limits growth potential.

2. Usage-Based Pricing: Customers pay based on their usage. Common in API services and cloud infrastructure. Examples include AWS and Twilio.

3. Tiered Pricing: Multiple packages at different price points. Most popular among SaaS companies. Typically includes Basic, Professional, and Enterprise tiers.

4. Per-User Pricing: Price scales with the number of users. Used by Slack, Salesforce, and many B2B SaaS products.

5. Freemium Model: Free tier with limited features, paid upgrades. Effective for product-led growth. Dropbox and Spotify are prime examples.

6. Value-Based Pricing: Price based on the perceived value delivered to the customer. Requires deep understanding of customer ROI.

Key Metrics to Track:
- Monthly Recurring Revenue (MRR)
- Annual Recurring Revenue (ARR)
- Customer Acquisition Cost (CAC)
- Lifetime Value (LTV)
- Churn Rate
- Net Revenue Retention (NRR)

Best Practices:
- Align pricing with value delivered
- A/B test pricing pages
- Offer annual discounts (typically 15-20%)
- Include a clear call-to-action
- Show social proof and case studies
- Implement transparent pricing pages"""
        },
        {
            "title": "SaaS Pricing: How to Price Your SaaS Product",
            "url": "https://example.com/how-to-price-saas",
            "snippet": "Learn proven SaaS pricing strategies used by top companies to maximize MRR and reduce churn.",
            "content": """Pricing your SaaS product correctly is essential for sustainable growth. This guide covers the fundamentals of SaaS pricing strategy.

Understanding Value Metrics:
A value metric is what you charge for. It should align with customer success. For project management tools, it might be per-user. For email marketing, it might be per-subscriber.

The Pricing Process:
1. Research competitor pricing
2. Understand customer willingness to pay
3. Define your value metric
4. Create pricing tiers
5. Test and iterate

Common Mistakes:
- Underpricing your product
- Too many pricing tiers
- Ignoring customer segmentation
- Not updating pricing regularly
- Hiding pricing information

Growth Strategies:
- Product-led growth (PLG) with freemium
- Sales-led growth with enterprise pricing
- Hybrid approach combining both models

Revenue Optimization:
- Expansion revenue through upsells
- Cross-selling additional products
- Annual contract incentives
- Feature gating strategies"""
        },
        {
            "title": "B2B SaaS Pricing Benchmarks and Strategies",
            "url": "https://example.com/b2b-saas-pricing",
            "snippet": "Industry benchmarks and data-driven strategies for B2B SaaS pricing optimization.",
            "content": """B2B SaaS pricing requires a different approach than B2C. Enterprise buyers evaluate ROI, security, compliance, and integration capabilities.

B2B Pricing Benchmarks:
- Average contract value: $25,000-$100,000 for mid-market
- Enterprise deals: $100,000+
- SMB pricing: $50-$500/month
- Gross margins: 70-85%
- Net revenue retention: 110-130% for top performers

Enterprise Features:
- Single Sign-On (SSO)
- SAML authentication
- Role-based access control (RBAC)
- Audit logging
- Custom SLAs
- Dedicated support
- API access
- Data export capabilities

Pricing Psychology:
- Anchoring effect with enterprise tier
- Decoy pricing strategies
- Price localization
- Charm pricing ($99 vs $100)

Customer Success Integration:
- Onboarding programs
- Customer health scoring
- Proactive churn prevention
- Quarterly business reviews"""
        },
        {
            "title": "Usage-Based Pricing for SaaS: Complete Framework",
            "url": "https://example.com/usage-based-pricing",
            "snippet": "How to implement usage-based pricing in your SaaS product with real-world examples and frameworks.",
            "content": """Usage-based pricing (UBP) is the fastest-growing pricing model in SaaS. Companies like Snowflake, Datadog, and Stripe have demonstrated its effectiveness.

Benefits of Usage-Based Pricing:
- Lower barrier to entry
- Revenue scales with customer success
- Natural expansion revenue
- Better alignment with customer value

Implementation Framework:
1. Identify your value metric (API calls, data processed, emails sent)
2. Set pricing tiers with volume discounts
3. Implement metering infrastructure
4. Build billing integration
5. Create usage dashboards for customers

Hybrid Models:
Many companies combine a base subscription with usage-based components. This provides predictable revenue while capturing upside.

Metering Best Practices:
- Real-time usage tracking
- Grace periods for overages
- Predictive usage alerts
- Transparent billing dashboards"""
        },
        {
            "title": "SaaS Metrics: The Complete Guide to KPIs",
            "url": "https://example.com/saas-metrics-guide",
            "snippet": "Essential SaaS metrics and KPIs every founder needs to track for growth and investor readiness.",
            "content": """Understanding and tracking the right SaaS metrics is critical for making data-driven decisions.

Core SaaS Metrics:
1. MRR (Monthly Recurring Revenue): The predictable revenue from subscriptions
2. ARR (Annual Recurring Revenue): MRR × 12
3. CAC (Customer Acquisition Cost): Total sales and marketing spend / new customers
4. LTV (Lifetime Value): Average revenue per customer / churn rate
5. LTV:CAC Ratio: Should be at least 3:1
6. Churn Rate: Percentage of customers lost per period
7. Net Revenue Retention (NRR): Revenue from existing customers including expansion
8. Burn Rate: Monthly cash spend
9. Runway: Cash remaining / burn rate
10. Rule of 40: Growth rate + profit margin should exceed 40%

Growth Benchmarks:
- Seed stage: 15-20% MoM growth
- Series A: 10-15% MoM growth
- Series B+: 100%+ YoY growth
- Public companies: 20-40% YoY growth

Unit Economics:
- CAC Payback Period: Months to recover acquisition cost
- Gross Margin: Revenue minus cost of goods sold
- Magic Number: Net new ARR / sales and marketing spend"""
        },
    ],
    "default": [
        {
            "title": "Comprehensive Guide to {keyword}",
            "url": "https://example.com/guide-{slug}",
            "snippet": "Everything you need to know about {keyword}. Complete guide with best practices.",
            "content": """This is a comprehensive guide to {keyword}. Understanding this topic is essential for success in the modern digital landscape.

Key Concepts:
- Foundation principles of {keyword}
- Best practices and strategies
- Common challenges and solutions
- Tools and technologies
- Industry trends and future outlook

Implementation Strategies:
1. Start with research and analysis
2. Define clear objectives and KPIs
3. Build a structured plan
4. Execute with iterative improvement
5. Measure and optimize results

Advanced Topics:
- Automation and AI integration
- Scalability considerations
- Performance optimization
- Security and compliance
- Integration with existing systems

Best Practices:
- Data-driven decision making
- Continuous monitoring and improvement
- Cross-functional collaboration
- Customer-centric approach
- Regular auditing and updates"""
        },
    ]
}


class SerpCollector:
    """
    Collects SERP data with priority:
    1. Ahrefs API (set AHREFS_API_KEY)  — production grade, top 20 results
    2. DuckDuckGo (free)                — good fallback, no API key needed
    3. Mock data                        — demo / offline mode

    Scraping priority:
    1. Playwright (headless, full JS)   — set USE_PLAYWRIGHT=true
    2. httpx + BeautifulSoup            — lightweight HTTP scraping
    3. Snippet only                     — minimal, always available
    """

    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._playwright_available: Optional[bool] = None

    async def collect(
        self,
        keyword: str,
        vertical: str = "saas",
        max_results: int = 20,
        use_live: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Collect SERP results for a keyword.
        Priority: Ahrefs API → DuckDuckGo → mock data.
        """
        cache_key = f"{keyword}:{vertical}"
        if cache_key in self._cache:
            logger.info(f"SERP cache hit for '{keyword}'")
            return self._cache[cache_key]

        results = []

        if use_live:
            # 1. Try Ahrefs API first
            try:
                from app.core import settings
                if settings.AHREFS_API_KEY:
                    results = await self._collect_ahrefs(keyword, max_results, settings.AHREFS_API_KEY)
                    logger.info(f"Ahrefs: {len(results)} results for '{keyword}'")
            except Exception as e:
                logger.warning(f"Ahrefs collection failed: {e}")

            # 2. Fall back to DuckDuckGo
            if not results:
                try:
                    results = await self._collect_live(keyword, max_results)
                    logger.info(f"DuckDuckGo: {len(results)} results for '{keyword}'")
                except Exception as e:
                    logger.warning(f"DuckDuckGo collection failed: {e}. Using mock data.")

        # 3. Final fallback: mock data
        if not results:
            results = self._get_mock_data(keyword, vertical)
            logger.info(f"Mock: {len(results)} results for '{keyword}'")

        # Generate content hashes and deduplicate
        seen_hashes = set()
        unique_results = []
        for i, result in enumerate(results):
            content = result.get("content", result.get("snippet", ""))
            content_hash = hashlib.sha256(content.encode()).hexdigest()

            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                result["content_hash"] = content_hash
                result["position"] = i + 1
                result["collected_at"] = datetime.utcnow().isoformat()
                unique_results.append(result)

        self._cache[cache_key] = unique_results[:max_results]
        return unique_results[:max_results]

    async def _collect_ahrefs(
        self, keyword: str, max_results: int, api_key: str
    ) -> List[Dict[str, Any]]:
        """
        Collect SERP data using the Ahrefs API.
        Endpoint: https://api.ahrefs.com/v3/serp-overview
        Requires: $99/mo API plan.
        """
        url = "https://api.ahrefs.com/v3/serp-overview"
        params = {
            "select": "url,title,description,traffic,backlinks,referring_domains",
            "where": f"keyword={keyword}",
            "limit": max_results,
            "country": "us",
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(url, params=params, headers=headers)
            if resp.status_code != 200:
                raise Exception(f"Ahrefs API {resp.status_code}: {resp.text[:200]}")
            data = resp.json()

        results = []
        for i, item in enumerate(data.get("serp", [])[:max_results]):
            page_url = item.get("url", "")
            content = await self._scrape_content_playwright(page_url)
            if not content:
                content = await self._scrape_content(page_url)
            results.append({
                "title": item.get("title", ""),
                "url": page_url,
                "snippet": item.get("description", ""),
                "content": content or item.get("description", ""),
                "position": i + 1,
                "backlinks": item.get("backlinks", 0),
                "referring_domains": item.get("referring_domains", 0),
                "source": "ahrefs",
            })
        return results

    async def _collect_live(self, keyword: str, max_results: int) -> List[Dict[str, Any]]:
        """Collect live results from DuckDuckGo — free fallback."""
        try:
            from duckduckgo_search import DDGS

            results = []
            with DDGS() as ddgs:
                search_results = list(ddgs.text(keyword, max_results=max_results))

                for i, r in enumerate(search_results):
                    url = r.get("href", "")
                    # Try Playwright first, then httpx
                    content = await self._scrape_content_playwright(url)
                    if not content:
                        content = await self._scrape_content(url)
                    results.append({
                        "title": r.get("title", ""),
                        "url": url,
                        "snippet": r.get("body", ""),
                        "content": content or r.get("body", ""),
                        "position": i + 1,
                        "source": "duckduckgo",
                    })

            return results
        except ImportError:
            logger.warning("duckduckgo-search not installed. Using mock data.")
            return []

    async def _scrape_content_playwright(self, url: str) -> Optional[str]:
        """
        Scrape full page content using Playwright headless browser.
        Handles JavaScript-rendered pages that httpx cannot access.
        Falls back silently if Playwright is not installed.
        """
        if not url or not url.startswith("http"):
            return None

        # Check/cache Playwright availability
        if self._playwright_available is False:
            return None

        try:
            from playwright.async_api import async_playwright
        except ImportError:
            if self._playwright_available is None:
                logger.info("Playwright not installed — using httpx scraper. Install with: pip install playwright && playwright install chromium")
                self._playwright_available = False
            return None

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.set_extra_http_headers({
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                })
                await page.goto(url, wait_until="domcontentloaded", timeout=12000)
                # Remove navigation/footer noise
                await page.evaluate("""
                    ['nav','header','footer','aside','script','style'].forEach(tag => {
                        document.querySelectorAll(tag).forEach(el => el.remove());
                    });
                """)
                text = await page.inner_text("body")
                await browser.close()
                self._playwright_available = True
                return text[:6000] if text else None
        except Exception as e:
            logger.debug(f"Playwright scrape failed for {url}: {e}")
            return None

    async def _scrape_content(self, url: str) -> Optional[str]:
        """Scrape page content using httpx + BeautifulSoup — fast, lightweight."""
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                response = await client.get(url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                })
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Remove scripts, styles, and nav elements
                    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
                        tag.decompose()

                    text = soup.get_text(separator="\n", strip=True)
                    # Limit content length
                    return text[:5000] if text else None
        except Exception as e:
            logger.debug(f"Failed to scrape {url}: {e}")
        return None

    def _get_mock_data(self, keyword: str, vertical: str) -> List[Dict[str, Any]]:
        """Return mock SERP data for development."""
        keyword_lower = keyword.lower().strip()

        # Check for exact or partial matches in mock data
        for mock_key, data in MOCK_SERP_DATA.items():
            if mock_key == "default":
                continue
            if mock_key in keyword_lower or keyword_lower in mock_key:
                return data

        # Use default mock data with keyword substitution
        default_data = MOCK_SERP_DATA["default"]
        results = []
        for item in default_data:
            slug = keyword_lower.replace(" ", "-")
            results.append({
                "title": item["title"].replace("{keyword}", keyword),
                "url": item["url"].replace("{slug}", slug),
                "snippet": item["snippet"].replace("{keyword}", keyword),
                "content": item["content"].replace("{keyword}", keyword),
            })
        return results


# Singleton instance
serp_collector = SerpCollector()
