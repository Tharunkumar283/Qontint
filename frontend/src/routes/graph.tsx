import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { z } from "zod";
import { EntityGraph } from "@/components/EntityGraph";
import { getGraph } from "@/lib/api";
import type { GraphResponse } from "@/lib/types";

const searchSchema = z.object({
  keyword: z.string().optional().default("best mortgage rates 2025"),
});

export const Route = createFileRoute("/graph")({
  head: () => ({
    meta: [
      { title: "Knowledge Graph — Qontint" },
      {
        name: "description",
        content:
          "Explore the entity authority graph powering Qontint's ranking predictions. Nodes weighted by PageRank.",
      },
      { property: "og:title", content: "Knowledge Graph — Qontint" },
      { property: "og:description", content: "PageRank-weighted entity authority graph for any keyword." },
    ],
  }),
  validateSearch: searchSchema,
  component: GraphPage,
});

function GraphPage() {
  const { keyword } = Route.useSearch();
  const [graphData, setGraphData] = useState<GraphResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    setError("");
    getGraph(keyword)
      .then(setGraphData)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load graph"))
      .finally(() => setLoading(false));
  }, [keyword]);

  const top = graphData?.stats.top_entities ?? [];
  const stats = graphData?.stats;

  return (
    <div className="container mx-auto px-6 py-12 lg:px-8 lg:py-16">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <div className="text-xs font-medium uppercase tracking-wider text-accent">Module 03</div>
          <h1 className="mt-2 font-display text-4xl font-semibold tracking-tight lg:text-5xl">
            Entity Authority Graph
          </h1>
          <p className="mt-3 max-w-2xl text-muted-foreground">
            Built from the top 20 SERPs for <span className="font-medium text-foreground">"{keyword}"</span>. Nodes are
            entities, edges are co-occurrence. PageRank assigns each node an authority score from 0 to 1.
          </p>
        </div>
        <div className="flex gap-2 text-xs">
          {["1d", "7d", "30d", "90d"].map((r, i) => (
            <button
              key={r}
              className={`rounded-md border px-3 py-1.5 ${
                i === 2
                  ? "border-accent/60 bg-accent/[0.06] text-foreground"
                  : "border-border bg-surface/60 text-muted-foreground hover:text-foreground"
              }`}
            >
              {r}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="mt-6 rounded-md border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive">
          ⚠ {error}
        </div>
      )}

      <div className="mt-10 grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          {loading ? (
            <div className="h-[520px] animate-pulse rounded-xl border border-border bg-surface/40" />
          ) : (
            <EntityGraph keyword={keyword} height={520} />
          )}
        </div>
        <div className="space-y-6">
          <div className="rounded-xl border border-border bg-surface/60 p-5">
            <div className="font-display text-base font-semibold">Top entities by PageRank</div>
            {loading ? (
              <div className="mt-4 space-y-3">
                {Array.from({ length: 6 }).map((_, i) => (
                  <div key={i} className="h-10 animate-pulse rounded bg-surface-raised" />
                ))}
              </div>
            ) : top.length === 0 ? (
              <p className="mt-4 text-sm text-muted-foreground">No graph data yet. Run an analysis first.</p>
            ) : (
              <ul className="mt-4 space-y-3">
                {top.slice(0, 6).map((e) => (
                  <li key={e.text}>
                    <div className="flex items-center justify-between text-sm">
                      <span className="font-medium">{e.text}</span>
                      <span className="font-mono text-muted-foreground">{e.authority_score.toFixed(2)}</span>
                    </div>
                    <div className="mt-1.5 h-1.5 overflow-hidden rounded-full bg-surface-raised">
                      <div
                        className="h-full bg-gradient-to-r from-accent to-accent-glow transition-all duration-700"
                        style={{ width: `${e.authority_score * 100}%` }}
                      />
                    </div>
                    <div className="mt-1 text-[11px] text-muted-foreground">{e.frequency} occurrences</div>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div className="rounded-xl border border-border bg-surface/60 p-5">
            <div className="font-display text-base font-semibold">Graph stats</div>
            <dl className="mt-4 grid grid-cols-2 gap-4 text-sm">
              {[
                ["Nodes", loading ? "—" : String(stats?.total_nodes ?? 0)],
                ["Edges", loading ? "—" : String(stats?.total_edges ?? 0)],
                ["Avg Authority", loading ? "—" : (stats?.avg_authority ?? 0).toFixed(2)],
                ["Top Entities", loading ? "—" : String(top.length)],
              ].map(([k, v]) => (
                <div key={k}>
                  <dt className="text-xs text-muted-foreground">{k}</dt>
                  <dd className="font-display text-xl font-semibold tabular-nums">{v}</dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
}
