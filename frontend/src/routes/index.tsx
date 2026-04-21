import { createFileRoute, Link } from "@tanstack/react-router";
import { MetricCard } from "@/components/MetricCard";
import { EntityGraph } from "@/components/EntityGraph";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Qontint — Predict Google rankings before you publish" },
      {
        name: "description",
        content:
          "Qontint is the Semantic Authority Operating System. Analyze SERPs, build knowledge graphs, score novelty, and forecast rank — all before you hit publish.",
      },
      { property: "og:title", content: "Qontint — Predict Google rankings before you publish" },
      {
        property: "og:description",
        content: "AI-powered SEO intelligence powered by NLP, knowledge graphs, and ranking ML.",
      },
    ],
  }),
  component: Index,
});

function Index() {
  return (
    <>
      <Hero />
      <LogoCloud />
      <PipelineSection />
      <ModulesSection />
      <VerticalsSection />
      <CTA />
    </>
  );
}

function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div aria-hidden className="absolute inset-0 grid-bg" />
      <div className="container relative mx-auto px-6 pb-20 pt-20 lg:px-8 lg:pb-28 lg:pt-28">
        <div className="grid items-center gap-16 lg:grid-cols-12">
          <div className="lg:col-span-6">
            <div className="inline-flex items-center gap-2 rounded-full border border-border-strong/60 bg-surface-raised/40 px-3 py-1 text-xs">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-accent" />
              <span className="font-medium text-foreground/90">Semantic Authority OS · v1.0</span>
              <span className="text-muted-foreground">— now in private beta</span>
            </div>
            <h1 className="mt-6 font-display text-5xl font-semibold leading-[1.05] tracking-tight text-balance lg:text-6xl">
              Know if your content will <span className="gradient-text-accent">rank on Google</span> before you publish.
            </h1>
            <p className="mt-6 max-w-xl text-lg leading-relaxed text-muted-foreground">
              Qontint analyzes the top 20 SERPs, extracts entities with NLP, builds a knowledge graph, scores
              novelty, and predicts your rank — with{" "}
              <span className="font-medium text-foreground">90%+ accuracy</span>.
            </p>
            <div className="mt-10 flex flex-wrap items-center gap-4">
              <Link
                to="/analyze"
                className="group inline-flex items-center gap-2 rounded-md bg-accent px-6 py-3 text-base font-semibold text-accent-foreground shadow-[0_0_30px_-8px_var(--accent)] transition-all hover:bg-accent-glow"
              >
                Predict my ranking
                <span className="transition-transform group-hover:translate-x-0.5">→</span>
              </Link>
              <Link
                to="/dashboard"
                className="inline-flex items-center gap-2 rounded-md border border-border-strong px-6 py-3 text-base font-medium text-foreground/90 transition-colors hover:bg-surface-raised/50"
              >
                See live demo
              </Link>
            </div>
            <dl className="mt-12 grid max-w-lg grid-cols-3 gap-6 border-t border-border/60 pt-8">
              {[
                { k: "90%+", v: "Rank accuracy" },
                { k: "<10s", v: "Per analysis" },
                { k: "20", v: "SERPs scanned" },
              ].map((s) => (
                <div key={s.v}>
                  <dt className="font-display text-2xl font-semibold gradient-text-accent">{s.k}</dt>
                  <dd className="mt-1 text-xs text-muted-foreground">{s.v}</dd>
                </div>
              ))}
            </dl>
          </div>

          <div className="lg:col-span-6">
            <HeroDashboardPreview />
          </div>
        </div>
      </div>
    </section>
  );
}

function HeroDashboardPreview() {
  return (
    <div className="relative">
      <div className="absolute -inset-4 rounded-3xl bg-accent/10 blur-2xl" aria-hidden />
      <div className="relative rounded-2xl border border-border-strong/70 bg-surface/80 p-5 backdrop-blur-xl shadow-[0_30px_80px_-30px_oklch(0%_0_0/0.8)]">
        <div className="mb-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex gap-1.5">
              <span className="h-2.5 w-2.5 rounded-full bg-foreground/15" />
              <span className="h-2.5 w-2.5 rounded-full bg-foreground/15" />
              <span className="h-2.5 w-2.5 rounded-full bg-foreground/15" />
            </div>
            <div className="ml-3 font-mono text-[11px] text-muted-foreground">
              qontint.app/analyze · "best mortgage rates 2025"
            </div>
          </div>
          <span className="rounded-full border border-success/30 bg-success/10 px-2 py-0.5 text-[10px] font-medium text-success">
            ● Live
          </span>
        </div>
        <div className="grid grid-cols-3 gap-3">
          <MetricCard accent label="Novelty" value="0.92" delta="+0.31" hint="vs SERP" />
          <MetricCard label="Predicted rank" value="#3" delta="↑ 12" hint="from #15" />
          <MetricCard label="Intent match" value="98%" hint="Informational" />
        </div>
        <div className="mt-3">
          <EntityGraph height={260} />
        </div>
        <div className="mt-3 grid grid-cols-3 gap-2 text-[11px]">
          {["+ Federal Reserve", "+ Yield Curve", "+ Discount Points"].map((s) => (
            <div
              key={s}
              className="rounded-md border border-info/30 bg-info/5 px-2 py-1.5 text-center font-medium text-info"
            >
              {s}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function LogoCloud() {
  return (
    <section className="border-y border-border/60 bg-surface/30 py-10">
      <div className="container mx-auto px-6 lg:px-8">
        <div className="text-center text-xs font-medium uppercase tracking-wider text-muted-foreground">
          Trusted by content teams across
        </div>
        <div className="mt-6 flex flex-wrap items-center justify-center gap-x-12 gap-y-4 font-display text-lg font-semibold text-foreground/40">
          {["Mortgage", "Healthcare", "Finance", "Legal", "SaaS", "Insurance"].map((v) => (
            <div key={v} className="transition-colors hover:text-foreground/70">
              {v}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

const pipeline = [
  { num: "01", title: "SERP Intelligence", desc: "Scrape & deduplicate the top 20 ranking results for any keyword." },
  { num: "02", title: "NLP Entity Extraction", desc: "Domain-tuned spaCy models pull entities, topics, relationships." },
  { num: "03", title: "Knowledge Graph", desc: "Neo4j builds an authority graph with PageRank-weighted entities." },
  { num: "04", title: "Novelty Scoring", desc: "Jaccard + graph diff — rejects derivative content below 0.35." },
  { num: "05", title: "Ranking Prediction", desc: "Gradient Boosting model forecasts position 1–20 with confidence." },
  { num: "06", title: "Recommendations", desc: "Surfaces missing high-authority entities to close the gap." },
];

function PipelineSection() {
  return (
    <section className="container mx-auto px-6 py-24 lg:px-8 lg:py-32">
      <div className="max-w-2xl">
        <div className="text-xs font-medium uppercase tracking-wider text-accent">The pipeline</div>
        <h2 className="mt-3 font-display text-4xl font-semibold tracking-tight text-balance lg:text-5xl">
          Intelligence first. Generation second.
        </h2>
        <p className="mt-4 text-lg text-muted-foreground">
          Qontint runs a closed-loop system: analyze, score, recommend, generate, validate — until your draft is
          ranking-ready.
        </p>
      </div>
      <div className="mt-14 grid gap-px overflow-hidden rounded-2xl border border-border bg-border md:grid-cols-2 lg:grid-cols-3">
        {pipeline.map((p) => (
          <div
            key={p.num}
            className="group relative bg-surface/60 p-7 transition-colors hover:bg-surface-raised/60"
          >
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs text-muted-foreground">{p.num}</span>
              <span className="h-1.5 w-1.5 rounded-full bg-accent/70 transition-all group-hover:bg-accent group-hover:shadow-[0_0_12px_var(--accent)]" />
            </div>
            <h3 className="mt-6 font-display text-xl font-semibold">{p.title}</h3>
            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{p.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function ModulesSection() {
  return (
    <section className="container mx-auto px-6 py-24 lg:px-8">
      <div className="grid gap-12 lg:grid-cols-12">
        <div className="lg:col-span-5">
          <div className="text-xs font-medium uppercase tracking-wider text-accent">Two-layer architecture</div>
          <h2 className="mt-3 font-display text-4xl font-semibold tracking-tight text-balance">
            Built like infrastructure, not a content tool.
          </h2>
          <p className="mt-4 text-muted-foreground">
            Qontint separates the intelligence core from the generation layer — so you get reliable predictions, not
            hopeful suggestions.
          </p>
        </div>
        <div className="grid gap-4 lg:col-span-7">
          {[
            {
              t: "Layer 1 — Intelligence Core",
              items: ["SERP Collector", "Entity Extractor", "Graph Builder", "Novelty Engine", "Ranking Predictor"],
              accent: true,
            },
            {
              t: "Layer 2 — Generation Layer",
              items: ["Content Generator", "Validation Loop", "Publishing Interface"],
            },
          ].map((b) => (
            <div
              key={b.t}
              className={`rounded-xl border p-6 ${
                b.accent ? "border-accent/40 bg-accent/[0.04]" : "border-border bg-surface/60"
              }`}
            >
              <div className="font-display text-base font-semibold">{b.t}</div>
              <div className="mt-4 flex flex-wrap gap-2">
                {b.items.map((i) => (
                  <span
                    key={i}
                    className="rounded-md border border-border-strong/60 bg-surface-raised/60 px-2.5 py-1 text-xs font-medium text-foreground/85"
                  >
                    {i}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function VerticalsSection() {
  const slms = [
    { name: "Mortgage", entities: "12.4k", status: "Production" },
    { name: "Healthcare", entities: "18.7k", status: "Production" },
    { name: "Finance", entities: "21.2k", status: "Beta" },
    { name: "Legal", entities: "9.6k", status: "Beta" },
    { name: "SaaS", entities: "14.1k", status: "Production" },
    { name: "Insurance", entities: "7.8k", status: "Training" },
  ];
  return (
    <section className="container mx-auto px-6 py-24 lg:px-8">
      <div className="rounded-3xl border border-border bg-surface/60 p-8 lg:p-14">
        <div className="grid gap-10 lg:grid-cols-2 lg:items-end">
          <div>
            <div className="text-xs font-medium uppercase tracking-wider text-accent">Vertical SLMs</div>
            <h2 className="mt-3 font-display text-4xl font-semibold tracking-tight text-balance">
              Small Language Models trained per industry.
            </h2>
            <p className="mt-4 max-w-xl text-muted-foreground">
              Domain-tuned NER, relationship detection, and ranking models — so your authority graph speaks your
              field's language.
            </p>
          </div>
          <Link
            to="/pricing"
            className="inline-flex w-fit items-center gap-2 rounded-md border border-border-strong px-5 py-2.5 text-sm font-medium hover:bg-surface-raised/50"
          >
            Request a vertical →
          </Link>
        </div>
        <div className="mt-10 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {slms.map((s) => (
            <div
              key={s.name}
              className="flex items-center justify-between rounded-xl border border-border bg-background/40 p-4"
            >
              <div>
                <div className="font-display text-base font-semibold">{s.name}</div>
                <div className="mt-0.5 font-mono text-xs text-muted-foreground">{s.entities} entities</div>
              </div>
              <span
                className={`rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider ${
                  s.status === "Production"
                    ? "bg-success/10 text-success"
                    : s.status === "Beta"
                      ? "bg-info/10 text-info"
                      : "bg-warning/10 text-warning"
                }`}
              >
                {s.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function CTA() {
  return (
    <section className="container mx-auto px-6 py-20 lg:px-8">
      <div className="relative overflow-hidden rounded-3xl border border-accent/30 bg-gradient-to-br from-surface to-surface-raised p-10 text-center lg:p-16">
        <div
          aria-hidden
          className="pointer-events-none absolute -top-20 left-1/2 h-64 w-[140%] -translate-x-1/2 rounded-full bg-accent/15 blur-3xl"
        />
        <h2 className="relative font-display text-4xl font-semibold tracking-tight text-balance lg:text-5xl">
          Stop guessing. Start <span className="gradient-text-accent">predicting</span>.
        </h2>
        <p className="relative mx-auto mt-4 max-w-xl text-muted-foreground">
          Run your first analysis in under 10 seconds. No credit card required.
        </p>
        <Link
          to="/analyze"
          className="relative mt-8 inline-flex items-center gap-2 rounded-md bg-accent px-7 py-3.5 text-base font-semibold text-accent-foreground shadow-[0_0_30px_-6px_var(--accent)] transition-all hover:bg-accent-glow"
        >
          Predict my ranking →
        </Link>
      </div>
    </section>
  );
}
