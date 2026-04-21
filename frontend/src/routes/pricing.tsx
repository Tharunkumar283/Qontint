import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/pricing")({
  head: () => ({
    meta: [
      { title: "Pricing — Qontint" },
      { name: "description", content: "Simple per-seat pricing. Start free, scale to enterprise vertical SLMs." },
      { property: "og:title", content: "Pricing — Qontint" },
      { property: "og:description", content: "Plans for solo SEOs, content teams, and enterprises with custom SLMs." },
    ],
  }),
  component: PricingPage,
});

const tiers = [
  {
    name: "Starter",
    price: "$0",
    period: "free forever",
    desc: "Run your first ranking predictions.",
    cta: "Start free",
    features: ["10 analyses / month", "1 vertical SLM", "Basic recommendations", "Community support"],
  },
  {
    name: "Studio",
    price: "$79",
    period: "per seat / month",
    desc: "For SEO teams shipping content weekly.",
    cta: "Start trial",
    features: [
      "500 analyses / month",
      "All vertical SLMs",
      "Iterative validation loop",
      "Knowledge graph export",
      "Slack & email support",
    ],
    featured: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "annual contract",
    desc: "Custom SLMs, on-prem, SSO.",
    cta: "Contact sales",
    features: [
      "Unlimited analyses",
      "Custom vertical SLM training",
      "On-prem / private cloud",
      "SSO + SCIM",
      "Dedicated success engineer",
    ],
  },
];

function PricingPage() {
  return (
    <div className="container mx-auto px-6 py-16 lg:px-8 lg:py-24">
      <div className="mx-auto max-w-2xl text-center">
        <div className="text-xs font-medium uppercase tracking-wider text-accent">Pricing</div>
        <h1 className="mt-3 font-display text-4xl font-semibold tracking-tight text-balance lg:text-5xl">
          Pay for predictions, not promises.
        </h1>
        <p className="mt-4 text-muted-foreground">
          Every plan includes the full intelligence pipeline. Upgrade for more analyses and more verticals.
        </p>
      </div>

      <div className="mt-14 grid gap-5 lg:grid-cols-3">
        {tiers.map((t) => (
          <div
            key={t.name}
            className={`relative flex flex-col rounded-2xl border p-7 ${
              t.featured
                ? "border-accent/50 bg-accent/[0.04] shadow-[0_0_60px_-20px_var(--accent)]"
                : "border-border bg-surface/60"
            }`}
          >
            {t.featured && (
              <span className="absolute -top-2.5 left-7 rounded-full bg-accent px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-accent-foreground">
                Most popular
              </span>
            )}
            <div className="font-display text-lg font-semibold">{t.name}</div>
            <div className="mt-1 text-sm text-muted-foreground">{t.desc}</div>
            <div className="mt-6 flex items-baseline gap-2">
              <span className="font-display text-4xl font-semibold">{t.price}</span>
              <span className="text-xs text-muted-foreground">{t.period}</span>
            </div>
            <Link
              to="/analyze"
              className={`mt-6 inline-flex items-center justify-center rounded-md px-4 py-2.5 text-sm font-semibold transition-colors ${
                t.featured
                  ? "bg-accent text-accent-foreground hover:bg-accent-glow"
                  : "border border-border-strong text-foreground hover:bg-surface-raised/50"
              }`}
            >
              {t.cta}
            </Link>
            <ul className="mt-6 space-y-2.5 border-t border-border/60 pt-6 text-sm">
              {t.features.map((f) => (
                <li key={f} className="flex items-start gap-2.5">
                  <span className="mt-0.5 text-accent">✓</span>
                  <span className="text-foreground/85">{f}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
