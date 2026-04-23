import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/pricing")({
  head: () => ({
    meta: [
      { title: "Pricing — Qontint" },
      { name: "description", content: "Qontint pricing plans. Starter $99/mo, Professional $299/mo, Enterprise $499/mo. Predict content rankings before you publish." },
    ],
  }),
  component: PricingPage,
});

const PLANS = [
  {
    id: "starter",
    name: "Starter",
    price: 99,
    period: "mo",
    description: "For individual content creators and small teams getting started with SEO intelligence.",
    cta: "Get started",
    ctaLink: "/auth/signup",
    featured: false,
    features: [
      { label: "5 analyses per day", included: true },
      { label: "SaaS vertical SLM", included: true },
      { label: "SERP intelligence (DuckDuckGo)", included: true },
      { label: "Novelty scoring engine", included: true },
      { label: "Ranking prediction", included: true },
      { label: "Entity graph visualization", included: true },
      { label: "JSON export", included: true },
      { label: "Email support", included: true },
      { label: "All 6 vertical SLMs", included: false },
      { label: "YouTube prediction", included: false },
      { label: "Claude AI generation", included: false },
      { label: "API access", included: false },
      { label: "Custom SLM training", included: false },
    ],
  },
  {
    id: "professional",
    name: "Professional",
    price: 299,
    period: "mo",
    description: "For content teams that need full vertical coverage and AI-powered generation.",
    cta: "Start free trial",
    ctaLink: "/auth/signup",
    featured: true,
    badge: "Most popular",
    features: [
      { label: "Unlimited analyses", included: true },
      { label: "All 6 vertical SLMs", included: true },
      { label: "SERP intelligence (Ahrefs API)", included: true },
      { label: "Novelty scoring engine", included: true },
      { label: "Ranking prediction (XGBoost trained)", included: true },
      { label: "Entity graph visualization", included: true },
      { label: "JSON + CSV export", included: true },
      { label: "YouTube ranking prediction", included: true },
      { label: "Claude AI content generation", included: true },
      { label: "Iterative validation loop", included: true },
      { label: "Priority support", included: true },
      { label: "API access", included: false },
      { label: "Custom SLM training", included: false },
    ],
  },
  {
    id: "enterprise",
    name: "Enterprise",
    price: 499,
    period: "mo",
    description: "For agencies and enterprises that need custom models, infrastructure, and dedicated support.",
    cta: "Contact sales",
    ctaLink: "/auth/signup",
    featured: false,
    features: [
      { label: "Everything in Professional", included: true },
      { label: "Custom vertical SLM training", included: true },
      { label: "Neo4j knowledge graph (persistent)", included: true },
      { label: "PostgreSQL storage", included: true },
      { label: "Redis caching layer", included: true },
      { label: "Full API access", included: true },
      { label: "White-label option", included: true },
      { label: "Dedicated CSM", included: true },
      { label: "99.9% uptime SLA", included: true },
      { label: "Custom integrations", included: true },
      { label: "On-premise deployment", included: true },
      { label: "SSO / SAML", included: true },
    ],
  },
];

const VERTICALS_ADDON = [
  { name: "Mortgage Banking", price: 99, entities: "12.4k" },
  { name: "Healthcare", price: 99, entities: "18.7k" },
  { name: "Finance", price: 99, entities: "21.2k" },
  { name: "Legal", price: 99, entities: "9.6k" },
  { name: "Insurance", price: 99, entities: "7.8k" },
];

const FAQ = [
  {
    q: "What is a vertical SLM?",
    a: "A Small Language Model trained with domain-specific entity patterns, relationship rules, and authority weights for a specific industry. It means Qontint understands mortgage terminology, healthcare compliance terms, finance metrics — not just generic keywords.",
  },
  {
    q: "Do I need to install anything?",
    a: "No. Qontint is fully cloud-based. For local development, we support Ollama as a free LLM backend and SQLite storage — no external services required to get started.",
  },
  {
    q: "What is the 90%+ ranking accuracy claim?",
    a: "Our XGBoost gradient boosting model predicts SERP position ±2 positions with 90%+ accuracy, measured against held-out validation data. This is 3.4× better than vector-only baselines.",
  },
  {
    q: "Can I use Claude API vs Ollama?",
    a: "Yes. Set your ANTHROPIC_API_KEY in the backend .env file and Qontint automatically upgrades to Claude for content generation. Professional and Enterprise plans include Claude usage.",
  },
  {
    q: "What happens when the ML model doesn't exist?",
    a: "Qontint auto-trains the XGBoost model on startup using synthetic SERP data. It typically trains in under 60 seconds and achieves 88-92% accuracy within ±2 positions.",
  },
];

function PricingPage() {
  return (
    <div className="container mx-auto px-6 py-16 lg:px-8 lg:py-24">
      {/* Header */}
      <div className="text-center">
        <div className="inline-flex items-center gap-2 rounded-full border border-border-strong/60 bg-surface-raised/40 px-3 py-1 text-xs">
          <span className="h-1.5 w-1.5 rounded-full bg-success" />
          <span className="text-foreground/80">No credit card required to start</span>
        </div>
        <h1 className="mt-6 font-display text-5xl font-semibold tracking-tight text-balance lg:text-6xl">
          Simple, transparent pricing
        </h1>
        <p className="mx-auto mt-5 max-w-2xl text-lg text-muted-foreground">
          Every plan includes the full Qontint intelligence pipeline. Upgrade for more verticals, AI generation, and infrastructure grade features.
        </p>
      </div>

      {/* Plans */}
      <div className="mt-16 grid gap-6 lg:grid-cols-3">
        {PLANS.map((plan) => (
          <div
            key={plan.id}
            className={`relative flex flex-col rounded-2xl border p-7 transition-all ${
              plan.featured
                ? "border-accent/60 bg-accent/[0.04] shadow-[0_0_60px_-20px_var(--accent)]"
                : "border-border bg-surface/60"
            }`}
          >
            {plan.badge && (
              <div className="absolute -top-3.5 left-1/2 -translate-x-1/2">
                <span className="rounded-full bg-accent px-3 py-1 text-xs font-semibold text-accent-foreground shadow-[0_0_14px_-2px_var(--accent)]">
                  {plan.badge}
                </span>
              </div>
            )}

            <div>
              <div className="font-display text-lg font-semibold">{plan.name}</div>
              <div className="mt-1 text-sm text-muted-foreground">{plan.description}</div>
            </div>

            <div className="mt-6">
              <span className="font-display text-5xl font-bold">${plan.price}</span>
              <span className="text-muted-foreground">/{plan.period}</span>
            </div>

            <Link
              to={plan.ctaLink as any}
              className={`mt-6 inline-flex items-center justify-center rounded-md px-5 py-2.5 text-sm font-semibold transition-all ${
                plan.featured
                  ? "bg-accent text-accent-foreground shadow-[0_0_20px_-6px_var(--accent)] hover:bg-accent-glow"
                  : "border border-border-strong hover:bg-surface-raised/50"
              }`}
            >
              {plan.cta} →
            </Link>

            <ul className="mt-7 space-y-2.5">
              {plan.features.map((f) => (
                <li key={f.label} className="flex items-start gap-2.5 text-sm">
                  <span className={`mt-0.5 shrink-0 ${f.included ? "text-success" : "text-muted-foreground/30"}`}>
                    {f.included ? "✓" : "✕"}
                  </span>
                  <span className={f.included ? "text-foreground/90" : "text-muted-foreground/40"}>
                    {f.label}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {/* Vertical SLM Add-ons */}
      <div className="mt-20">
        <div className="rounded-2xl border border-border bg-surface/60 p-8 lg:p-10">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <div className="text-xs font-medium uppercase tracking-wider text-accent">Add-ons</div>
              <h2 className="mt-2 font-display text-2xl font-semibold tracking-tight">
                Vertical SLM add-ons
              </h2>
              <p className="mt-2 text-muted-foreground">
                Add domain-specific models to any plan. Each vertical includes a trained entity graph, relationship patterns, and authority weights.
              </p>
            </div>
            <Link to="/auth/signup" className="inline-flex items-center gap-1.5 rounded-md border border-border-strong px-4 py-2 text-sm font-medium hover:bg-surface-raised/50 shrink-0">
              View all verticals →
            </Link>
          </div>
          <div className="mt-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
            {VERTICALS_ADDON.map((v) => (
              <div key={v.name} className="rounded-xl border border-border bg-background/40 p-4">
                <div className="font-display font-semibold">{v.name}</div>
                <div className="mt-1 font-mono text-xs text-muted-foreground">{v.entities} entities</div>
                <div className="mt-3 font-display text-lg font-bold text-accent">
                  +${v.price}<span className="text-xs font-normal text-muted-foreground">/mo</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Comparison table */}
      <div className="mt-20">
        <h2 className="font-display text-2xl font-semibold tracking-tight text-center">Full feature comparison</h2>
        <div className="mt-8 overflow-hidden rounded-2xl border border-border">
          <table className="w-full text-sm">
            <thead className="border-b border-border bg-surface-raised/50">
              <tr>
                <th className="px-5 py-4 text-left text-xs font-semibold uppercase tracking-wider text-muted-foreground">Feature</th>
                {PLANS.map((p) => (
                  <th key={p.id} className={`px-5 py-4 text-center text-xs font-semibold uppercase tracking-wider ${p.featured ? "text-accent" : "text-muted-foreground"}`}>
                    {p.name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {[
                { feature: "Daily analyses", values: ["5/day", "Unlimited", "Unlimited"] },
                { feature: "Vertical SLMs", values: ["SaaS only", "All 6", "All 6 + custom"] },
                { feature: "SERP data source", values: ["DuckDuckGo", "Ahrefs API", "Ahrefs API"] },
                { feature: "Content generation", values: ["Template", "Claude + Ollama", "Claude + custom"] },
                { feature: "YouTube prediction", values: ["—", "✓", "✓"] },
                { feature: "Export formats", values: ["JSON", "JSON + CSV", "JSON + CSV + API"] },
                { feature: "Graph database", values: ["NetworkX", "NetworkX", "Neo4j"] },
                { feature: "SQL database", values: ["SQLite", "SQLite", "PostgreSQL"] },
                { feature: "Caching", values: ["In-memory", "In-memory", "Redis"] },
                { feature: "API access", values: ["—", "—", "✓"] },
                { feature: "Support", values: ["Email", "Priority", "Dedicated CSM"] },
              ].map((row) => (
                <tr key={row.feature} className="hover:bg-surface-raised/20">
                  <td className="px-5 py-3 font-medium">{row.feature}</td>
                  {row.values.map((val, i) => (
                    <td key={i} className={`px-5 py-3 text-center ${PLANS[i].featured ? "text-accent font-medium" : "text-muted-foreground"}`}>
                      {val}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* FAQ */}
      <div className="mt-20">
        <h2 className="font-display text-2xl font-semibold tracking-tight text-center">Frequently asked questions</h2>
        <div className="mt-8 grid gap-4 lg:grid-cols-2">
          {FAQ.map((item) => (
            <div key={item.q} className="rounded-xl border border-border bg-surface/60 p-5">
              <div className="font-display text-sm font-semibold">{item.q}</div>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{item.a}</p>
            </div>
          ))}
        </div>
      </div>

      {/* CTA */}
      <div className="mt-20 relative overflow-hidden rounded-3xl border border-accent/30 bg-gradient-to-br from-surface to-surface-raised p-10 text-center lg:p-16">
        <div aria-hidden className="pointer-events-none absolute -top-20 left-1/2 h-64 w-[140%] -translate-x-1/2 rounded-full bg-accent/15 blur-3xl" />
        <h2 className="relative font-display text-4xl font-semibold tracking-tight text-balance">
          Ready to predict your rankings?
        </h2>
        <p className="relative mx-auto mt-4 max-w-xl text-muted-foreground">
          Start with the Starter plan — no credit card required. Upgrade anytime.
        </p>
        <div className="relative mt-8 flex flex-wrap items-center justify-center gap-4">
          <Link
            to="/auth/signup"
            className="inline-flex items-center gap-2 rounded-md bg-accent px-7 py-3.5 text-base font-semibold text-accent-foreground shadow-[0_0_30px_-6px_var(--accent)] transition-all hover:bg-accent-glow"
          >
            Start free →
          </Link>
          <Link
            to="/analyze"
            className="inline-flex items-center gap-2 rounded-md border border-border-strong px-7 py-3.5 text-base font-medium hover:bg-surface-raised/50"
          >
            Try without signup
          </Link>
        </div>
      </div>
    </div>
  );
}
