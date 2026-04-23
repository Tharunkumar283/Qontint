"""
MODULE 11 — Vertical Small Language Models (SLMs) Manager
Manages domain-specific entity recognition and relationship patterns.
Supports: SaaS, Mortgage, Healthcare, Finance, Legal, Insurance
"""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


# ─── SaaS Vertical Model ─────────────────────────────────────────────
SAAS_MODEL = {
    "name": "SaaS Vertical Model",
    "version": "1.0.0",
    "vertical": "saas",
    "description": "Domain-specific model for SaaS industry entity recognition and ranking prediction",
    "entity_patterns": {
        "SAAS_METRIC": {
            "patterns": [
                "MRR", "ARR", "NRR", "CAC", "LTV", "ARPU", "ARPA",
                "churn rate", "retention rate", "burn rate", "runway",
                "gross margin", "net margin", "EBITDA",
                "CAC payback period", "magic number", "rule of 40",
                "LTV:CAC ratio", "quick ratio", "NDR",
                "net dollar retention", "gross revenue retention",
                "expansion revenue", "contraction revenue",
            ],
            "weight": 1.5,
        },
        "SAAS_CONCEPT": {
            "patterns": [
                "product-led growth", "PLG", "sales-led growth", "SLG",
                "community-led growth", "CLG", "partner-led growth",
                "freemium", "free trial", "reverse trial",
                "usage-based pricing", "seat-based pricing", "tiered pricing",
                "value metric", "pricing page", "pricing strategy",
                "product-market fit", "PMF", "go-to-market", "GTM",
                "ideal customer profile", "ICP", "buyer persona",
                "total addressable market", "TAM", "SAM", "SOM",
                "customer success", "customer health score",
                "net promoter score", "NPS", "CSAT", "CES",
                "onboarding", "activation", "time to value",
                "feature adoption", "feature flag", "feature gating",
                "multi-tenant architecture", "single-tenant",
                "microservices", "monolith", "serverless",
                "API-first", "developer experience", "DX",
                "CI/CD pipeline", "DevOps", "SRE",
                "SOC 2", "ISO 27001", "GDPR", "HIPAA", "FedRAMP",
            ],
            "weight": 1.3,
        },
        "SAAS_STRATEGY": {
            "patterns": [
                "A/B testing", "cohort analysis", "funnel analysis",
                "customer segmentation", "persona development",
                "land and expand", "bottoms-up", "top-down",
                "content marketing", "SEO strategy", "demand generation",
                "account-based marketing", "ABM", "inbound marketing",
                "outbound sales", "SDR", "BDR", "AE",
                "customer advisory board", "beta program",
                "product hunt launch", "viral loop",
                "referral program", "partner program",
                "self-serve model", "enterprise sales motion",
            ],
            "weight": 1.2,
        },
        "SAAS_STAGE": {
            "patterns": [
                "pre-seed", "seed", "Series A", "Series B", "Series C",
                "growth stage", "scale-up", "IPO", "acquisition",
                "bootstrap", "bootstrapped", "venture-backed",
                "unicorn", "decacorn", "centaur",
            ],
            "weight": 1.0,
        },
    },
    "relationship_patterns": {
        "drives": ["PLG drives adoption", "content drives leads", "NPS drives retention"],
        "measures": ["MRR measures revenue", "CAC measures efficiency", "NRR measures expansion"],
        "enables": ["automation enables scale", "API enables integration", "SSO enables enterprise"],
        "requires": ["enterprise requires SOC 2", "growth requires PMF", "scaling requires automation"],
        "impacts": ["churn impacts ARR", "pricing impacts CAC", "onboarding impacts activation"],
    },
    "authority_weights": {
        "SAAS_METRIC": 1.5, "SAAS_CONCEPT": 1.3, "SAAS_STRATEGY": 1.2,
        "SAAS_STAGE": 1.0, "ORG": 0.8, "PERSON": 0.6, "KEYWORD": 0.4,
    },
}


# ─── Mortgage Vertical Model ──────────────────────────────────────────
MORTGAGE_MODEL = {
    "name": "Mortgage Banking Vertical Model",
    "version": "1.0.0",
    "vertical": "mortgage",
    "description": "Domain-specific SLM for US Mortgage Banking — rates, lending, refinancing, compliance",
    "entity_patterns": {
        "MORTGAGE_PRODUCT": {
            "patterns": [
                "30-year fixed", "15-year fixed", "adjustable-rate mortgage", "ARM",
                "FHA loan", "VA loan", "USDA loan", "jumbo loan", "conforming loan",
                "conventional mortgage", "reverse mortgage", "HELOC",
                "home equity loan", "cash-out refinance", "rate-and-term refinance",
                "streamline refinance", "construction loan", "bridge loan",
                "interest-only mortgage", "balloon mortgage", "portfolio loan",
                "non-QM loan", "bank statement loan", "DSCR loan",
            ],
            "weight": 1.5,
        },
        "MORTGAGE_METRIC": {
            "patterns": [
                "APR", "interest rate", "mortgage rate", "basis points", "bps",
                "loan-to-value", "LTV", "combined LTV", "CLTV",
                "debt-to-income ratio", "DTI", "front-end ratio", "back-end ratio",
                "credit score", "FICO score", "origination fee", "discount points",
                "closing costs", "escrow", "PMI", "MIP", "mortgage insurance",
                "amortization", "principal", "equity", "underwater",
                "prepayment penalty", "yield spread premium", "par rate",
            ],
            "weight": 1.5,
        },
        "MORTGAGE_PROCESS": {
            "patterns": [
                "pre-approval", "pre-qualification", "underwriting", "appraisal",
                "title search", "title insurance", "closing disclosure", "loan estimate",
                "good faith estimate", "HUD-1", "right of rescission",
                "mortgage commitment", "rate lock", "float down", "lock period",
                "conditional approval", "clear to close", "CTC",
                "debt consolidation", "cash-out", "net tangible benefit",
            ],
            "weight": 1.3,
        },
        "MORTGAGE_COMPLIANCE": {
            "patterns": [
                "TILA", "RESPA", "TRID", "QM rule", "ability-to-repay",
                "HMDA", "Fair Housing Act", "ECOA", "CRA",
                "Dodd-Frank", "CFPB", "FHFA", "Fannie Mae", "Freddie Mac",
                "Ginnie Mae", "GSE", "conforming limit", "FHA guidelines",
                "VA eligibility", "USDA rural development",
            ],
            "weight": 1.2,
        },
        "MORTGAGE_MARKET": {
            "patterns": [
                "Federal Reserve", "Fed funds rate", "10-year Treasury", "yield curve",
                "MBS", "mortgage-backed securities", "secondary market",
                "primary market", "origination volume", "refinance boom",
                "purchase market", "housing inventory", "affordability index",
                "median home price", "Case-Shiller index", "NAR", "MBA",
            ],
            "weight": 1.1,
        },
    },
    "relationship_patterns": {
        "determines": ["Fed rate determines mortgage rate", "credit score determines approval", "LTV determines PMI"],
        "requires": ["FHA requires MIP", "VA requires funding fee", "QM requires ATR"],
        "impacts": ["rate hike impacts affordability", "inventory impacts price", "DTI impacts qualification"],
        "protects": ["PMI protects lender", "title insurance protects buyer", "escrow protects both"],
    },
    "authority_weights": {
        "MORTGAGE_PRODUCT": 1.5, "MORTGAGE_METRIC": 1.5, "MORTGAGE_PROCESS": 1.3,
        "MORTGAGE_COMPLIANCE": 1.2, "MORTGAGE_MARKET": 1.1, "ORG": 0.8, "PERSON": 0.6,
    },
}


# ─── Healthcare Vertical Model ────────────────────────────────────────
HEALTHCARE_MODEL = {
    "name": "Healthcare Vertical Model",
    "version": "1.0.0",
    "vertical": "healthcare",
    "description": "Domain-specific SLM for healthcare — conditions, treatments, providers, compliance",
    "entity_patterns": {
        "MEDICAL_CONDITION": {
            "patterns": [
                "diabetes", "hypertension", "cardiovascular disease", "heart disease",
                "cancer", "depression", "anxiety disorder", "COPD", "asthma",
                "obesity", "chronic kidney disease", "Alzheimer's", "dementia",
                "stroke", "COVID-19", "long COVID", "autoimmune disease",
                "arthritis", "osteoporosis", "metabolic syndrome",
            ],
            "weight": 1.5,
        },
        "MEDICAL_TREATMENT": {
            "patterns": [
                "chemotherapy", "immunotherapy", "radiation therapy", "surgery",
                "physical therapy", "cognitive behavioral therapy", "CBT",
                "dialysis", "transplant", "stent", "bypass surgery",
                "medication adherence", "clinical trial", "FDA approval",
                "off-label use", "biosimilar", "generic drug",
                "telemedicine", "telehealth", "remote patient monitoring",
            ],
            "weight": 1.5,
        },
        "HEALTHCARE_METRIC": {
            "patterns": [
                "HEDIS", "CAHPS", "patient satisfaction", "readmission rate",
                "mortality rate", "morbidity", "quality-adjusted life year", "QALY",
                "cost per patient", "length of stay", "LOS",
                "net promoter score", "patient engagement", "care gap",
                "value-based care", "fee-for-service", "capitation",
                "risk adjustment", "HCC coding", "RAF score",
            ],
            "weight": 1.4,
        },
        "HEALTHCARE_COMPLIANCE": {
            "patterns": [
                "HIPAA", "HITECH", "PHI", "ePHI", "EHR", "EMR",
                "meaningful use", "MACRA", "MIPS", "APM",
                "CMS", "Medicare", "Medicaid", "ACA", "COBRA",
                "prior authorization", "formulary", "network adequacy",
                "credentialing", "accreditation", "Joint Commission", "NCQA",
            ],
            "weight": 1.3,
        },
        "HEALTHCARE_PROVIDER": {
            "patterns": [
                "primary care physician", "PCP", "specialist", "hospitalist",
                "nurse practitioner", "NP", "physician assistant", "PA",
                "ACO", "accountable care organization", "IPA", "MSO",
                "health system", "integrated delivery network", "IDN",
                "urgent care", "ambulatory surgery center", "ASC",
            ],
            "weight": 1.1,
        },
    },
    "relationship_patterns": {
        "treats": ["medication treats condition", "therapy treats disorder", "surgery treats disease"],
        "requires": ["HIPAA requires consent", "Medicare requires documentation", "surgery requires clearance"],
        "measures": ["HEDIS measures quality", "CAHPS measures satisfaction", "QALY measures outcomes"],
        "impacts": ["comorbidity impacts outcome", "adherence impacts recovery", "access impacts health"],
    },
    "authority_weights": {
        "MEDICAL_CONDITION": 1.5, "MEDICAL_TREATMENT": 1.5, "HEALTHCARE_METRIC": 1.4,
        "HEALTHCARE_COMPLIANCE": 1.3, "HEALTHCARE_PROVIDER": 1.1, "ORG": 0.8,
    },
}


# ─── Finance Vertical Model ───────────────────────────────────────────
FINANCE_MODEL = {
    "name": "Finance Vertical Model",
    "version": "1.0.0",
    "vertical": "finance",
    "description": "Domain-specific SLM for personal and institutional finance — investing, banking, taxes",
    "entity_patterns": {
        "FINANCE_INSTRUMENT": {
            "patterns": [
                "stock", "equity", "bond", "ETF", "mutual fund", "index fund",
                "options", "futures", "derivatives", "REITs", "treasury bond",
                "corporate bond", "municipal bond", "CD", "certificate of deposit",
                "annuity", "life insurance", "term life", "whole life",
                "401k", "IRA", "Roth IRA", "HSA", "529 plan",
                "cryptocurrency", "Bitcoin", "Ethereum", "DeFi",
            ],
            "weight": 1.5,
        },
        "FINANCE_METRIC": {
            "patterns": [
                "P/E ratio", "EPS", "earnings per share", "dividend yield",
                "ROI", "return on investment", "ROE", "return on equity",
                "alpha", "beta", "Sharpe ratio", "expense ratio",
                "compound annual growth rate", "CAGR", "total return",
                "net asset value", "NAV", "book value", "market cap",
                "debt-to-equity ratio", "current ratio", "quick ratio",
                "EBITDA", "free cash flow", "FCF", "operating margin",
            ],
            "weight": 1.5,
        },
        "FINANCE_STRATEGY": {
            "patterns": [
                "dollar-cost averaging", "DCA", "value investing", "growth investing",
                "dividend investing", "momentum trading", "swing trading",
                "day trading", "buy and hold", "passive investing",
                "portfolio diversification", "asset allocation", "rebalancing",
                "tax-loss harvesting", "tax-advantaged", "estate planning",
                "financial independence", "FIRE", "retirement planning",
            ],
            "weight": 1.3,
        },
        "FINANCE_MARKET": {
            "patterns": [
                "bull market", "bear market", "market correction", "recession",
                "inflation", "deflation", "stagflation", "interest rate",
                "Federal Reserve", "FOMC", "quantitative easing", "QE",
                "yield curve inversion", "credit spread", "VIX",
                "S&P 500", "Dow Jones", "NASDAQ", "Russell 2000",
            ],
            "weight": 1.2,
        },
        "FINANCE_COMPLIANCE": {
            "patterns": [
                "SEC", "FINRA", "fiduciary duty", "suitability standard",
                "accredited investor", "Reg D", "Reg A", "IPO", "SPAC",
                "insider trading", "wash sale rule", "capital gains tax",
                "short-term capital gains", "long-term capital gains",
                "qualified dividend", "AMT", "alternative minimum tax",
            ],
            "weight": 1.1,
        },
    },
    "relationship_patterns": {
        "drives": ["inflation drives rates", "earnings drive stock price", "Fed drives market"],
        "measures": ["P/E measures valuation", "Sharpe measures risk-return", "beta measures volatility"],
        "impacts": ["recession impacts portfolio", "rate hike impacts bonds", "tax impacts returns"],
        "reduces": ["diversification reduces risk", "hedging reduces exposure", "DCA reduces timing risk"],
    },
    "authority_weights": {
        "FINANCE_INSTRUMENT": 1.5, "FINANCE_METRIC": 1.5, "FINANCE_STRATEGY": 1.3,
        "FINANCE_MARKET": 1.2, "FINANCE_COMPLIANCE": 1.1, "ORG": 0.8,
    },
}


# ─── Legal Vertical Model ─────────────────────────────────────────────
LEGAL_MODEL = {
    "name": "Legal Vertical Model",
    "version": "1.0.0",
    "vertical": "legal",
    "description": "Domain-specific SLM for legal — practice areas, statutes, procedure, compliance",
    "entity_patterns": {
        "LEGAL_PRACTICE": {
            "patterns": [
                "personal injury", "medical malpractice", "wrongful death",
                "criminal defense", "DUI", "drug charges", "white collar crime",
                "family law", "divorce", "child custody", "child support",
                "estate planning", "probate", "trust", "power of attorney",
                "real estate law", "landlord-tenant", "eviction",
                "employment law", "wrongful termination", "discrimination",
                "immigration law", "visa", "green card", "asylum",
                "bankruptcy", "Chapter 7", "Chapter 13", "Chapter 11",
                "intellectual property", "patent", "trademark", "copyright",
            ],
            "weight": 1.5,
        },
        "LEGAL_PROCESS": {
            "patterns": [
                "complaint", "summons", "deposition", "discovery", "subpoena",
                "interrogatories", "motion to dismiss", "summary judgment",
                "trial", "verdict", "appeal", "settlement", "mediation",
                "arbitration", "class action", "statute of limitations",
                "injunction", "restraining order", "contempt of court",
                "habeas corpus", "plea bargain", "arraignment",
            ],
            "weight": 1.4,
        },
        "LEGAL_CONCEPT": {
            "patterns": [
                "negligence", "liability", "duty of care", "breach of contract",
                "damages", "punitive damages", "compensatory damages",
                "preponderance of evidence", "beyond reasonable doubt",
                "attorney-client privilege", "work product doctrine",
                "due process", "equal protection", "first amendment",
                "fourth amendment", "fifth amendment", "Miranda rights",
                "mens rea", "actus reus", "respondeat superior",
            ],
            "weight": 1.3,
        },
        "LEGAL_COMPLIANCE": {
            "patterns": [
                "GDPR", "CCPA", "HIPAA", "ADA", "Title VII", "FMLA",
                "FLSA", "OSHA", "SEC regulations", "Dodd-Frank",
                "SOX", "Sarbanes-Oxley", "anti-money laundering", "AML",
                "know your customer", "KYC", "FCPA", "RICO",
            ],
            "weight": 1.2,
        },
    },
    "relationship_patterns": {
        "establishes": ["contract establishes obligation", "statute establishes standard", "precedent establishes rule"],
        "requires": ["negligence requires duty", "contract requires consideration", "crime requires intent"],
        "triggers": ["breach triggers liability", "injury triggers damages", "violation triggers penalty"],
        "protects": ["privilege protects communication", "amendment protects rights", "immunity protects officer"],
    },
    "authority_weights": {
        "LEGAL_PRACTICE": 1.5, "LEGAL_PROCESS": 1.4, "LEGAL_CONCEPT": 1.3,
        "LEGAL_COMPLIANCE": 1.2, "ORG": 0.8, "PERSON": 0.7,
    },
}


# ─── Insurance Vertical Model ─────────────────────────────────────────
INSURANCE_MODEL = {
    "name": "Insurance Vertical Model",
    "version": "1.0.0",
    "vertical": "insurance",
    "description": "Domain-specific SLM for insurance — auto, life, health, P&C, underwriting",
    "entity_patterns": {
        "INSURANCE_PRODUCT": {
            "patterns": [
                "term life insurance", "whole life insurance", "universal life",
                "variable life", "final expense insurance",
                "auto insurance", "collision coverage", "comprehensive coverage",
                "liability coverage", "uninsured motorist", "PIP",
                "homeowners insurance", "renters insurance", "condo insurance",
                "health insurance", "ACA plan", "COBRA", "HMO", "PPO", "EPO",
                "disability insurance", "short-term disability", "long-term disability",
                "umbrella policy", "commercial general liability", "CGL",
                "professional liability", "E&O", "D&O", "cyber insurance",
                "business interruption", "workers compensation",
            ],
            "weight": 1.5,
        },
        "INSURANCE_METRIC": {
            "patterns": [
                "premium", "deductible", "copay", "coinsurance", "out-of-pocket maximum",
                "coverage limit", "policy limit", "per-occurrence limit",
                "loss ratio", "combined ratio", "expense ratio",
                "claims frequency", "claims severity", "subrogation",
                "actual cash value", "ACV", "replacement cost value", "RCV",
                "agreed value", "stated value", "reinsurance",
            ],
            "weight": 1.5,
        },
        "INSURANCE_PROCESS": {
            "patterns": [
                "underwriting", "risk assessment", "actuarial", "claims adjuster",
                "first notice of loss", "FNOL", "claims investigation",
                "independent medical exam", "IME", "appraisal",
                "subrogation", "contribution", "salvage",
                "policy exclusion", "rider", "endorsement", "binder",
                "certificate of insurance", "COI", "declarations page",
            ],
            "weight": 1.3,
        },
        "INSURANCE_COMPLIANCE": {
            "patterns": [
                "NAIC", "state insurance commissioner", "admitted carrier",
                "surplus lines", "Lloyd's of London", "A.M. Best rating",
                "solvency ratio", "risk-based capital", "RBC",
                "McCarran-Ferguson", "DOI", "department of insurance",
                "appointed agent", "licensed producer", "E&S market",
            ],
            "weight": 1.2,
        },
    },
    "relationship_patterns": {
        "covers": ["policy covers loss", "rider covers additional risk", "umbrella covers excess"],
        "determines": ["underwriting determines premium", "risk determines coverage", "credit determines rate"],
        "excludes": ["policy excludes flood", "exclusion excludes intentional act", "rider excludes preexisting"],
        "pays": ["insurer pays claim", "reinsurer pays excess", "subrogation pays recovery"],
    },
    "authority_weights": {
        "INSURANCE_PRODUCT": 1.5, "INSURANCE_METRIC": 1.5, "INSURANCE_PROCESS": 1.3,
        "INSURANCE_COMPLIANCE": 1.2, "ORG": 0.8, "PERSON": 0.6,
    },
}


# ─── SLM Manager ──────────────────────────────────────────────────────

class SLMManager:
    """
    Manages Vertical Small Language Models (SLMs).
    Supports: SaaS, Mortgage, Healthcare, Finance, Legal, Insurance.
    """

    def __init__(self):
        self._models: Dict[str, Dict] = {
            "saas": SAAS_MODEL,
            "mortgage": MORTGAGE_MODEL,
            "healthcare": HEALTHCARE_MODEL,
            "finance": FINANCE_MODEL,
            "legal": LEGAL_MODEL,
            "insurance": INSURANCE_MODEL,
        }
        self._active_model: Optional[str] = "saas"

    def get_model(self, vertical: str) -> Optional[Dict]:
        return self._models.get(vertical)

    def get_entity_patterns(self, vertical: str) -> Dict:
        model = self._models.get(vertical)
        if model:
            return model.get("entity_patterns", {})
        return {}

    def get_authority_weights(self, vertical: str) -> Dict[str, float]:
        model = self._models.get(vertical)
        if model:
            return model.get("authority_weights", {})
        return {}

    def adjust_authority_score(self, entity_type: str, base_score: float, vertical: str = "saas") -> float:
        weights = self.get_authority_weights(vertical)
        weight = weights.get(entity_type, 1.0)
        return min(base_score * weight, 1.0)

    def get_available_verticals(self) -> List[Dict]:
        return [
            {
                "vertical": key,
                "name": model["name"],
                "version": model["version"],
                "description": model["description"],
                "entity_types": list(model.get("entity_patterns", {}).keys()),
                "entity_count": sum(
                    len(v["patterns"])
                    for v in model.get("entity_patterns", {}).values()
                ),
            }
            for key, model in self._models.items()
        ]

    def is_domain_entity(self, text: str, vertical: str = "saas") -> Optional[Dict]:
        patterns = self.get_entity_patterns(vertical)
        text_lower = text.lower()
        for entity_type, config in patterns.items():
            for pattern in config["patterns"]:
                if pattern.lower() == text_lower or pattern.lower() in text_lower:
                    return {
                        "text": text,
                        "type": entity_type,
                        "weight": config.get("weight", 1.0),
                        "vertical": vertical,
                    }
        return None

    def enrich_entities(self, entities: List[Dict], vertical: str = "saas") -> List[Dict]:
        enriched = []
        for entity in entities:
            domain_match = self.is_domain_entity(entity["text"], vertical)
            if domain_match:
                entity["type"] = domain_match["type"]
                entity["domain_weight"] = domain_match["weight"]
                entity["vertical"] = vertical
            enriched.append(entity)
        return enriched


# Singleton instance
slm_manager = SLMManager()
