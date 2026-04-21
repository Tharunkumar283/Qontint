import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { collectSerp } from "@/lib/api";
import type { Vertical, IntentType } from "@/lib/types";

export const Route = createFileRoute("/analyze")({
  head: () => ({
    meta: [
      { title: "Analyze a keyword — Qontint" },
      {
        name: "description",
        content: "Run a full Qontint semantic authority analysis on any keyword. Predict rank in under 10 seconds.",
      },
      { property: "og:title", content: "Analyze a keyword — Qontint" },
      {
        property: "og:description",
        content: "Run SERP, entity, novelty, and rank prediction on any keyword in under 10 seconds.",
      },
    ],
  }),
  component: AnalyzePage,
});

const verticals: { id: Vertical; label: string; desc: string }[] = [
  { id: "mortgage", label: "Mortgage", desc: "Rates, refinancing, lending products" },
  { id: "healthcare", label: "Healthcare", desc: "Conditions, treatments, providers" },
  { id: "finance", label: "Finance", desc: "Investing, banking, taxes" },
  { id: "saas", label: "SaaS", desc: "B2B software & dev tools" },
  { id: "legal", label: "Legal", desc: "Practice areas, statutes" },
  { id: "insurance", label: "Insurance", desc: "Auto, life, health, P&C" },
];

const examples = [
  "best mortgage rates 2025",
  "how to refinance student loans",
  "kubernetes vs docker compose",
  "ozempic side effects",
  "small business tax deductions",
];

type PipelinePhase = "idle" | "serp" | "ready" | "error";

function AnalyzePage() {
  const navigate = useNavigate();
  const [keyword, setKeyword] = useState("");
  const [vertical, setVertical] = useState<Vertical>("mortgage");
  const [intent, setIntent] = useState<IntentType>("informational");
  const [phase, setPhase] = useState<PipelinePhase>("idle");
  const [errorMsg, setErrorMsg] = useState("");

  const loading = phase === "serp";

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const kw = keyword.trim();
    if (!kw) return;

    setErrorMsg("");
    setPhase("serp");

    try {
      // Step 1 — collect SERP data & build graph on backend
      await collectSerp({ keyword: kw, vertical });

      // Step 2 — navigate to dashboard with analysis params
      navigate({
        to: "/dashboard",
        search: { keyword: kw, vertical, intent },
      });
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Something went wrong.";
      setErrorMsg(msg);
      setPhase("error");
    }
  };

  return (
    <div className="relative">
      <div aria-hidden className="absolute inset-0 grid-bg" />
      <div className="container relative mx-auto px-6 py-16 lg:px-8 lg:py-24">
        <div className="mx-auto max-w-3xl text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-border-strong/60 bg-surface-raised/40 px-3 py-1 text-xs">
            <span className="font-mono text-muted-foreground">/analyze</span>
            <span className="text-foreground/80">Real-time pipeline</span>
          </div>
          <h1 className="mt-5 font-display text-4xl font-semibold tracking-tight text-balance lg:text-5xl">
            What keyword should rank?
          </h1>
          <p className="mt-3 text-muted-foreground">
            Qontint will pull the top 20 SERPs, extract entities, score novelty, and predict your rank — in under 10
            seconds.
          </p>
        </div>

        <form
          onSubmit={onSubmit}
          className="relative mx-auto mt-12 max-w-3xl rounded-2xl border border-border-strong/70 bg-surface/80 p-6 backdrop-blur-xl shadow-elevated lg:p-8"
        >
          <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Target keyword
          </label>
          <div className="mt-2 flex flex-col gap-2 sm:flex-row">
            <input
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder="e.g. best mortgage rates 2025"
              className="flex-1 rounded-md border border-border-strong bg-background/60 px-4 py-3 text-base outline-none transition-colors placeholder:text-muted-foreground/60 focus:border-accent focus:ring-2 focus:ring-accent/30"
            />
            <button
              type="submit"
              disabled={loading || !keyword.trim()}
              className="inline-flex items-center justify-center gap-2 rounded-md bg-accent px-6 py-3 text-base font-semibold text-accent-foreground shadow-[0_0_24px_-8px_var(--accent)] transition-all hover:bg-accent-glow disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? (
                <>
                  <span className="h-4 w-4 animate-spin rounded-full border-2 border-accent-foreground/30 border-t-accent-foreground" />
                  {phase === "serp" ? "Collecting SERPs…" : "Running pipeline…"}
                </>
              ) : (
                <>Run analysis →</>
              )}
            </button>
          </div>

          {errorMsg && (
            <div className="mt-3 rounded-md border border-destructive/40 bg-destructive/10 px-4 py-2.5 text-sm text-destructive">
              ⚠ {errorMsg}
            </div>
          )}

          <div className="mt-3 flex flex-wrap items-center gap-2">
            <span className="text-xs text-muted-foreground">Try:</span>
            {examples.map((ex) => (
              <button
                key={ex}
                type="button"
                onClick={() => setKeyword(ex)}
                className="rounded-full border border-border bg-background/40 px-2.5 py-1 text-xs text-foreground/80 transition-colors hover:border-accent/40 hover:text-foreground"
              >
                {ex}
              </button>
            ))}
          </div>

          <div className="mt-8">
            <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Vertical SLM
            </label>
            <div className="mt-3 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
              {verticals.map((v) => {
                const active = vertical === v.id;
                return (
                  <button
                    type="button"
                    key={v.id}
                    onClick={() => setVertical(v.id)}
                    className={`rounded-lg border p-3 text-left transition-all ${
                      active
                        ? "border-accent/60 bg-accent/[0.06] shadow-[0_0_0_1px_var(--accent)]"
                        : "border-border bg-background/40 hover:border-border-strong"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="font-display text-sm font-semibold">{v.label}</div>
                      {active && <span className="text-accent">●</span>}
                    </div>
                    <div className="mt-1 text-xs text-muted-foreground">{v.desc}</div>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="mt-6">
            <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Search intent
            </label>
            <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
              {(["informational", "transactional", "navigational", "commercial"] as IntentType[]).map((i) => {
                const active = intent === i;
                return (
                  <button
                    key={i}
                    type="button"
                    onClick={() => setIntent(i)}
                    className={`rounded-md border px-3 py-2 text-sm capitalize transition-colors ${
                      active
                        ? "border-accent/60 bg-accent/[0.06] text-foreground"
                        : "border-border bg-background/40 text-muted-foreground hover:text-foreground"
                    }`}
                  >
                    {i}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="mt-6 flex items-center gap-4 border-t border-border/60 pt-4 text-xs text-muted-foreground">
            <PipelineStep label="SERP" active={phase === "serp"} done={phase === "ready"} />
            <PipelineStep label="NLP" />
            <PipelineStep label="Graph" />
            <PipelineStep label="Novelty" />
            <PipelineStep label="Rank" last />
          </div>
        </form>

        <div className="mx-auto mt-8 max-w-3xl text-center text-xs text-muted-foreground">
          Already have a draft?{" "}
          <Link to="/dashboard" className="font-medium text-foreground underline-offset-4 hover:underline">
            Open the editor →
          </Link>
        </div>
      </div>
    </div>
  );
}

function PipelineStep({
  label,
  last,
  active,
  done,
}: {
  label: string;
  last?: boolean;
  active?: boolean;
  done?: boolean;
}) {
  return (
    <>
      <span className="flex items-center gap-1.5">
        <span
          className={`h-1.5 w-1.5 rounded-full transition-colors ${
            done ? "bg-success" : active ? "animate-pulse bg-accent" : "bg-accent"
          }`}
        />
        <span className="font-medium text-foreground/80">{label}</span>
      </span>
      {!last && <span className="text-border-strong">→</span>}
    </>
  );
}
