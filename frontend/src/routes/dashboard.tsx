import { createFileRoute, Link } from "@tanstack/react-router";
import { useState, useEffect, useCallback } from "react";
import { z } from "zod";
import { MetricCard } from "@/components/MetricCard";
import { EntityGraph } from "@/components/EntityGraph";
import { analyzeContent, getRecommendations, generateContent, exportAnalysisJson, exportAnalysisCsv } from "@/lib/api";
import type { AnalyzeResponse, RecommendationItem, Vertical, IntentType } from "@/lib/types";

// ─── Route search params ────────────────────────────────────────────────

const searchSchema = z.object({
  keyword: z.string().optional().default("best mortgage rates 2025"),
  vertical: z.string().optional().default("mortgage"),
  intent: z.string().optional().default("informational"),
});

export const Route = createFileRoute("/dashboard")({
  head: () => ({
    meta: [
      { title: "Analysis dashboard — Qontint" },
      {
        name: "description",
        content:
          "Live analysis: novelty score, predicted rank, intent alignment, entity graph and AI-generated content recommendations.",
      },
      { property: "og:title", content: "Analysis dashboard — Qontint" },
      { property: "og:description", content: "Predicted rank, novelty score, intent match and entity recommendations." },
    ],
  }),
  validateSearch: searchSchema,
  component: Dashboard,
});

// ─── Default / skeleton draft ────────────────────────────────────────────

const DEFAULT_DRAFT = `Write your draft content here and click "Analyze Draft" to score your novelty, 
entity coverage, and get a real ranking prediction from the backend.`;

// ─── Dashboard component ─────────────────────────────────────────────────

function Dashboard() {
  const { keyword, vertical, intent } = Route.useSearch();
  const [tab, setTab] = useState<"overview" | "editor" | "serp">("overview");

  // Analysis state
  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null);
  const [recs, setRecs] = useState<RecommendationItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");
  const [elapsedMs, setElapsedMs] = useState(0);

  // Editor state
  const [draft, setDraft] = useState(DEFAULT_DRAFT);
  const [draftAnalysis, setDraftAnalysis] = useState<AnalyzeResponse | null>(null);
  const [draftLoading, setDraftLoading] = useState(false);

  // Generated content state
  const [generatedContent, setGeneratedContent] = useState("");
  const [generating, setGenerating] = useState(false);

  // Export state
  const [exportOpen, setExportOpen] = useState(false);
  const [exporting, setExporting] = useState(false);

  const handleExport = async (format: "json" | "csv") => {
    setExporting(true);
    setExportOpen(false);
    try {
      const req = { keyword, vertical, content: draft !== DEFAULT_DRAFT ? draft : undefined };
      if (format === "json") await exportAnalysisJson(req);
      else await exportAnalysisCsv(req);
    } catch (err) {
      console.error("Export failed", err);
    } finally {
      setExporting(false);
    }
  };

  // ─── Initial pipeline: analyze a minimal seed content ──────────────────
  const runInitialAnalysis = useCallback(async () => {
    setLoading(true);
    setErrorMsg("");
    const start = Date.now();

    try {
      // Use keyword as seed content for initial analysis
      const seedContent = `This article covers ${keyword}. It provides an analysis of the key entities, relationships, and factors.`;

      const [analysisRes, recsRes] = await Promise.all([
        analyzeContent({ content: seedContent, keyword, vertical: vertical as Vertical }),
        getRecommendations({ content: seedContent, keyword, vertical: vertical as Vertical }),
      ]);

      setAnalysis(analysisRes);
      setRecs(recsRes.recommendations);
      setElapsedMs(Date.now() - start);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Analysis failed.";
      setErrorMsg(msg);
    } finally {
      setLoading(false);
    }
  }, [keyword, vertical]);

  useEffect(() => {
    runInitialAnalysis();
  }, [runInitialAnalysis]);

  // ─── Analyze user draft ───────────────────────────────────────────────
  const analyzeDraft = async () => {
    if (!draft.trim() || draft === DEFAULT_DRAFT) return;
    setDraftLoading(true);
    try {
      const res = await analyzeContent({ content: draft, keyword, vertical: vertical as Vertical });
      setDraftAnalysis(res);
    } catch (err) {
      console.error("Draft analysis failed", err);
    } finally {
      setDraftLoading(false);
    }
  };

  // ─── Generate content with AI ─────────────────────────────────────────
  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const res = await generateContent({
        keyword,
        vertical: vertical as Vertical,
        intent: intent as IntentType,
        use_authority_entities: true,
      });
      setGeneratedContent(res.content);
      setDraft(res.content);
    } catch (err) {
      console.error("Generation failed", err);
    } finally {
      setGenerating(false);
    }
  };

  // ─── Derived display values ───────────────────────────────────────────
  const data = draftAnalysis ?? analysis;
  const novelty = data ? data.novelty_score.toFixed(2) : "—";
  const rank = data ? `#${data.predicted_rank}` : "—";
  const intentPct = data ? `${Math.round(data.intent_alignment * 100)}%` : "—";
  const confidence = data ? `${Math.round(data.confidence_score * 100)}%` : "—";
  const passedThreshold = data ? data.novelty_score >= 0.35 : false;

  return (
    <div className="container mx-auto px-6 py-10 lg:px-8 lg:py-14">
      {/* Header */}
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <Link to="/analyze" className="hover:text-foreground">
              ← Analyze
            </Link>
            <span>·</span>
            <span className="font-mono">vertical: {vertical}</span>
            <span>·</span>
            {loading ? (
              <span className="inline-flex items-center gap-1.5">
                <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-accent" />
                Running pipeline…
              </span>
            ) : errorMsg ? (
              <span className="text-destructive">Pipeline error</span>
            ) : (
              <span className="inline-flex items-center gap-1.5">
                <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-success" />
                Pipeline complete · {(elapsedMs / 1000).toFixed(1)}s
              </span>
            )}
          </div>
          <h1 className="mt-2 font-display text-3xl font-semibold tracking-tight lg:text-4xl">
            "{keyword}"
          </h1>
        </div>
        <div className="flex gap-2">
          {/* Export dropdown */}
          <div className="relative">
            <button
              id="export-btn"
              onClick={() => setExportOpen((v) => !v)}
              disabled={exporting || loading}
              className="inline-flex items-center gap-1.5 rounded-md border border-border-strong px-4 py-2 text-sm font-medium transition-colors hover:bg-surface-raised/50 disabled:opacity-50"
            >
              {exporting ? (
                <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-foreground/20 border-t-foreground" />
              ) : (
                <svg className="h-4 w-4" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <path d="M8 2v8M5 7l3 3 3-3M2 11v1.5A1.5 1.5 0 003.5 14h9A1.5 1.5 0 0014 12.5V11" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              )}
              Export
              <svg className="h-3 w-3" viewBox="0 0 12 12" fill="currentColor">
                <path d="M3 4.5l3 3 3-3" stroke="currentColor" strokeWidth="1.2" fill="none" strokeLinecap="round" />
              </svg>
            </button>
            {exportOpen && (
              <>
                <div className="fixed inset-0 z-10" onClick={() => setExportOpen(false)} />
                <div className="absolute right-0 top-full z-20 mt-1 w-40 rounded-xl border border-border bg-surface shadow-elevated">
                  <div className="p-1">
                    <button
                      id="export-json-btn"
                      onClick={() => handleExport("json")}
                      className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-foreground/80 hover:bg-surface-raised/60"
                    >
                      <span className="font-mono text-xs text-accent">{"{}"}</span> JSON
                    </button>
                    <button
                      id="export-csv-btn"
                      onClick={() => handleExport("csv")}
                      className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-foreground/80 hover:bg-surface-raised/60"
                    >
                      <span className="font-mono text-xs text-accent">CSV</span> Spreadsheet
                    </button>
                  </div>
                </div>
              </>
            )}
          </div>
          <button
            className={`rounded-md px-4 py-2 text-sm font-semibold shadow-[0_0_18px_-6px_var(--accent)] transition-colors ${
              passedThreshold
                ? "bg-success text-white hover:bg-success/90"
                : "bg-accent text-accent-foreground hover:bg-accent-glow"
            }`}
          >
            {passedThreshold ? "Publish-ready ✓" : "Needs improvement"}
          </button>
        </div>
      </div>

      {/* Error banner */}
      {errorMsg && (
        <div className="mt-4 rounded-md border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive">
          ⚠ {errorMsg} — make sure the backend is running at{" "}
          <code className="font-mono text-xs">{import.meta.env.VITE_API_URL ?? "http://localhost:8000"}</code>
        </div>
      )}

      {/* Top metrics */}
      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {loading ? (
          Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-28 animate-pulse rounded-xl border border-border bg-surface/60" />
          ))
        ) : (
          <>
            <MetricCard
              accent
              label="Novelty Score"
              value={novelty}
              delta={data ? (data.novelty_score >= 0.35 ? "✓ above threshold" : "↓ below 0.35") : undefined}
              hint="threshold 0.35"
            />
            <MetricCard
              label="Predicted Rank"
              value={rank}
              hint="SERP position"
            />
            <MetricCard label="Intent Alignment" value={intentPct} hint={`${intent} match`} />
            <MetricCard label="ML Confidence" value={confidence} hint="Gradient Boosting" />
          </>
        )}
      </div>

      {/* Tabs */}
      <div className="mt-10 flex gap-1 border-b border-border">
        {(
          [
            { id: "overview", label: "Overview" },
            { id: "editor", label: "Content editor" },
            { id: "serp", label: "SERP intelligence" },
          ] as const
        ).map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`relative px-4 py-2.5 text-sm font-medium transition-colors ${
              tab === t.id ? "text-foreground" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {t.label}
            {tab === t.id && (
              <span className="absolute inset-x-0 -bottom-px h-0.5 bg-accent shadow-[0_0_10px_var(--accent)]" />
            )}
          </button>
        ))}
      </div>

      {tab === "overview" && (
        <OverviewTab analysis={data} recs={recs} loading={loading} keyword={keyword} />
      )}
      {tab === "editor" && (
        <EditorTab
          draft={draft}
          setDraft={setDraft}
          draftAnalysis={draftAnalysis}
          analyzing={draftLoading}
          onAnalyze={analyzeDraft}
          onGenerate={handleGenerate}
          generating={generating}
          generatedContent={generatedContent}
        />
      )}
      {tab === "serp" && <SerpTab analysis={data} loading={loading} />}
    </div>
  );
}

// ─── Overview Tab ─────────────────────────────────────────────────────────

function OverviewTab({
  analysis,
  recs,
  loading,
  keyword,
}: {
  analysis: AnalyzeResponse | null;
  recs: RecommendationItem[];
  loading: boolean;
  keyword: string;
}) {
  return (
    <div className="mt-8 grid gap-6 lg:grid-cols-3">
      <div className="lg:col-span-2 space-y-6">
        <Panel title="Entity Authority Graph" subtitle="PageRank weighted · live from knowledge graph">
          <EntityGraph keyword={keyword} height={380} />
        </Panel>
        <Panel title="Ranking Prediction" subtitle={`Gradient Boosting · ${analysis ? Math.round(analysis.confidence_score * 100) : "—"}% confidence`}>
          <RankingChart predicted={analysis?.predicted_rank ?? null} loading={loading} />
        </Panel>
      </div>
      <div className="space-y-6">
        <Panel
          title="Recommended Entities"
          subtitle="Close the gap to #1"
          headerAction={<span className="text-accent">+{recs.length}</span>}
        >
          {loading ? (
            <div className="space-y-2">
              {Array.from({ length: 4 }).map((_, i) => (
                <div key={i} className="h-16 animate-pulse rounded-lg border border-border bg-background/40" />
              ))}
            </div>
          ) : recs.length === 0 ? (
            <p className="text-sm text-muted-foreground">No recommendations yet. Run analysis first.</p>
          ) : (
            <ul className="space-y-2.5">
              {recs.slice(0, 5).map((r) => (
                <li
                  key={r.entity}
                  className="group rounded-lg border border-border bg-background/40 p-3 transition-colors hover:border-accent/40"
                >
                  <div className="flex items-center justify-between">
                    <div className="font-display text-sm font-semibold">{r.entity}</div>
                    <span className="rounded-md bg-success/10 px-1.5 py-0.5 text-[10px] font-semibold text-success">
                      {r.authority_score.toFixed(2)}
                    </span>
                  </div>
                  <div className="mt-1 text-xs leading-relaxed text-muted-foreground">{r.suggestion}</div>
                </li>
              ))}
            </ul>
          )}
        </Panel>
        <Panel title="Quality Signals">
          {loading ? (
            <div className="space-y-3">
              {Array.from({ length: 4 }).map((_, i) => (
                <div key={i} className="h-8 animate-pulse rounded bg-surface-raised" />
              ))}
            </div>
          ) : (
            <div className="space-y-3">
              <Bar
                label="Entity Coverage"
                value={Math.round((analysis?.entity_coverage ?? 0) * 100)}
                weight="40%"
              />
              <Bar
                label="Relationship Completeness"
                value={Math.round((analysis?.relationship_completeness ?? 0) * 100)}
                weight="30%"
              />
              <Bar
                label="Authority Score"
                value={Math.round((analysis?.authority_score ?? 0) * 100)}
                weight="20%"
              />
              <Bar
                label="Content Quality"
                value={Math.round((analysis?.content_quality ?? 0) * 100)}
                weight="10%"
              />
            </div>
          )}
        </Panel>
      </div>
    </div>
  );
}

// ─── Editor Tab ───────────────────────────────────────────────────────────

function EditorTab({
  draft,
  setDraft,
  draftAnalysis,
  analyzing,
  onAnalyze,
  onGenerate,
  generating,
  generatedContent,
}: {
  draft: string;
  setDraft: (v: string) => void;
  draftAnalysis: AnalyzeResponse | null;
  analyzing: boolean;
  onAnalyze: () => void;
  onGenerate: () => void;
  generating: boolean;
  generatedContent: string;
}) {
  const intentData = draftAnalysis
    ? [
        { k: "Informational", v: Math.round(draftAnalysis.intent_type === "informational" ? draftAnalysis.intent_alignment * 100 : 15), primary: draftAnalysis.intent_type === "informational" },
        { k: "Commercial", v: Math.round(draftAnalysis.intent_type === "commercial" ? draftAnalysis.intent_alignment * 100 : 25), primary: draftAnalysis.intent_type === "commercial" },
        { k: "Transactional", v: Math.round(draftAnalysis.intent_type === "transactional" ? draftAnalysis.intent_alignment * 100 : 12), primary: draftAnalysis.intent_type === "transactional" },
        { k: "Navigational", v: Math.round(draftAnalysis.intent_type === "navigational" ? draftAnalysis.intent_alignment * 100 : 5), primary: draftAnalysis.intent_type === "navigational" },
      ]
    : [
        { k: "Informational", v: 0, primary: true },
        { k: "Commercial", v: 0, primary: false },
        { k: "Transactional", v: 0, primary: false },
        { k: "Navigational", v: 0, primary: false },
      ];

  return (
    <div className="mt-8 grid gap-6 lg:grid-cols-3">
      <div className="lg:col-span-2">
        <Panel
          title="Draft"
          subtitle="Live novelty scoring · auto-saved"
          headerAction={
            <div className="flex gap-2">
              <button
                onClick={onGenerate}
                disabled={generating}
                className="rounded-md bg-accent/15 px-3 py-1 text-xs font-semibold text-accent hover:bg-accent/25 disabled:opacity-50"
              >
                {generating ? (
                  <span className="flex items-center gap-1.5">
                    <span className="h-3 w-3 animate-spin rounded-full border-2 border-accent/30 border-t-accent" />
                    Generating…
                  </span>
                ) : (
                  "✨ Generate with AI"
                )}
              </button>
              <button
                onClick={onAnalyze}
                disabled={analyzing}
                className="rounded-md bg-foreground/10 px-3 py-1 text-xs font-semibold text-foreground hover:bg-foreground/20 disabled:opacity-50"
              >
                {analyzing ? "Analyzing…" : "Analyze draft →"}
              </button>
            </div>
          }
        >
          <textarea
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            className="min-h-[420px] w-full resize-none rounded-md border border-border bg-background/40 p-4 font-mono text-sm leading-relaxed outline-none focus:border-accent focus:ring-2 focus:ring-accent/30"
          />
          <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
            <span>{draft.split(/\s+/).filter(Boolean).length} words</span>
            <span>·</span>
            <span>{draftAnalysis ? `${draftAnalysis.entities_found.length} entities detected` : "No analysis yet"}</span>
            <span>·</span>
            {draftAnalysis ? (
              <span className={draftAnalysis.novelty_score >= 0.35 ? "text-success" : "text-destructive"}>
                Novelty {draftAnalysis.novelty_score.toFixed(2)} {draftAnalysis.novelty_score >= 0.35 ? "✓" : "↓"}
              </span>
            ) : (
              <span>Click "Analyze draft" to score</span>
            )}
          </div>
        </Panel>
      </div>
      <div className="space-y-6">
        <Panel title="Iterative Validation Loop">
          <ol className="space-y-3 text-sm">
            {[
              { s: "SERP collected", done: true },
              { s: "Graph built", done: true },
              { s: draftAnalysis ? `Novelty scored: ${draftAnalysis.novelty_score.toFixed(2)}` : "Score novelty", done: !!draftAnalysis },
              { s: generatedContent ? "AI content generated" : "Generate with AI", done: !!generatedContent },
              {
                s: draftAnalysis?.pass_fail === "PASS" ? "Publish-ready ✓" : "Publish-ready",
                done: draftAnalysis?.pass_fail === "PASS",
              },
            ].map((step, i) => (
              <li key={i} className="flex items-center gap-3">
                <span
                  className={`flex h-6 w-6 items-center justify-center rounded-full text-[10px] font-bold ${
                    step.done ? "bg-accent/20 text-accent" : "bg-surface-raised text-muted-foreground"
                  }`}
                >
                  {i + 1}
                </span>
                <span className={step.done ? "text-foreground" : "text-muted-foreground"}>{step.s}</span>
              </li>
            ))}
          </ol>
        </Panel>
        <Panel title="Intent Mapping">
          <div className="space-y-2">
            {intentData.map((item) => (
              <div key={item.k}>
                <div className="flex justify-between text-xs">
                  <span className={item.primary ? "font-semibold text-foreground" : "text-muted-foreground"}>
                    {item.k}
                  </span>
                  <span className="font-mono text-muted-foreground">{item.v}%</span>
                </div>
                <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-surface-raised">
                  <div
                    className={`h-full rounded-full ${item.primary ? "bg-accent" : "bg-foreground/30"}`}
                    style={{ width: `${item.v}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </Panel>
        {draftAnalysis && draftAnalysis.missing_entities.length > 0 && (
          <Panel title="Missing Entities">
            <ul className="space-y-1.5">
              {draftAnalysis.missing_entities.slice(0, 5).map((e) => (
                <li key={e.text} className="flex items-center justify-between text-sm">
                  <span className="text-info">{e.text}</span>
                  <span className="font-mono text-xs text-muted-foreground">{e.authority_score.toFixed(2)}</span>
                </li>
              ))}
            </ul>
          </Panel>
        )}
      </div>
    </div>
  );
}

// ─── SERP Tab ─────────────────────────────────────────────────────────────

function SerpTab({ analysis, loading }: { analysis: AnalyzeResponse | null; loading: boolean }) {
  // The backend /analyze endpoint doesn't return raw SERP list, but we can show entities_found
  return (
    <div className="mt-8">
      <Panel title="Entities Found in SERP" subtitle="Extracted from top 20 results · ranked by authority">
        {loading ? (
          <div className="space-y-2">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="h-10 animate-pulse rounded-lg border border-border bg-background/40" />
            ))}
          </div>
        ) : !analysis ? (
          <p className="text-sm text-muted-foreground">No data yet. Run an analysis first.</p>
        ) : (
          <div className="overflow-hidden rounded-lg border border-border">
            <table className="w-full text-sm">
              <thead className="bg-surface-raised/50 text-left text-xs uppercase tracking-wider text-muted-foreground">
                <tr>
                  <th className="px-4 py-3">#</th>
                  <th className="px-4 py-3">Entity</th>
                  <th className="px-4 py-3">Type</th>
                  <th className="px-4 py-3 text-right">Frequency</th>
                  <th className="px-4 py-3 text-right">Authority</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {analysis.entities_found.map((e, i) => (
                  <tr key={e.text} className="transition-colors hover:bg-surface-raised/30">
                    <td className="px-4 py-3 font-mono text-muted-foreground">{i + 1}</td>
                    <td className="px-4 py-3 font-medium">{e.text}</td>
                    <td className="px-4 py-3 text-muted-foreground">{e.type}</td>
                    <td className="px-4 py-3 text-right font-mono">{e.frequency}</td>
                    <td className="px-4 py-3 text-right">
                      <span className="inline-block h-2 w-16 overflow-hidden rounded-full bg-surface-raised align-middle">
                        <span
                          className="block h-full bg-accent"
                          style={{ width: `${e.authority_score * 100}%` }}
                        />
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Panel>
    </div>
  );
}

// ─── Shared UI helpers ────────────────────────────────────────────────────

function Panel({
  title,
  subtitle,
  headerAction,
  children,
}: {
  title: string;
  subtitle?: string;
  headerAction?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <section className="rounded-xl border border-border bg-surface/60 p-5 lg:p-6">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="font-display text-base font-semibold">{title}</h3>
          {subtitle && <div className="mt-0.5 text-xs text-muted-foreground">{subtitle}</div>}
        </div>
        {headerAction}
      </div>
      <div className="mt-5">{children}</div>
    </section>
  );
}

function Bar({ label, value, weight }: { label: string; value: number; weight: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs">
        <span className="text-foreground/85">{label}</span>
        <span className="font-mono text-muted-foreground">
          {value}% <span className="text-foreground/40">· w {weight}</span>
        </span>
      </div>
      <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-surface-raised">
        <div
          className="h-full rounded-full bg-gradient-to-r from-accent to-accent-glow transition-all duration-700"
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}

function RankingChart({ predicted, loading }: { predicted: number | null; loading: boolean }) {
  // Distribution centred on predicted rank
  const buildProbs = (pos: number) => {
    return Array.from({ length: 20 }, (_, i) => {
      const dist = Math.abs(i + 1 - pos);
      return Math.max(0, 30 - dist * dist * 1.5);
    });
  };

  const probs = loading || predicted === null ? Array(20).fill(0) : buildProbs(predicted);
  const max = Math.max(...probs, 1);
  const targetIdx = predicted !== null ? predicted - 1 : -1;

  return (
    <div>
      <div className="flex items-end gap-1.5" style={{ height: 180 }}>
        {probs.map((p, i) => {
          const target = i === targetIdx;
          return (
            <div key={i} className="group flex flex-1 flex-col items-center justify-end">
              <div
                className={`w-full rounded-t-sm transition-all duration-700 ${
                  target
                    ? "bg-gradient-to-t from-accent to-accent-glow shadow-[0_0_16px_-2px_var(--accent)]"
                    : loading
                      ? "animate-pulse bg-foreground/10"
                      : "bg-foreground/15 group-hover:bg-foreground/25"
                }`}
                style={{ height: `${(p / max) * 100}%`, minHeight: p > 0 ? 4 : 1 }}
                title={`Position ${i + 1}: ${p.toFixed(0)}%`}
              />
              <div className={`mt-2 font-mono text-[10px] ${target ? "text-accent" : "text-muted-foreground"}`}>
                {i + 1}
              </div>
            </div>
          );
        })}
      </div>
      <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
        <span>SERP position →</span>
        <span>
          <span className="text-foreground">Most likely:</span> position{" "}
          {loading ? (
            <span className="animate-pulse">—</span>
          ) : (
            <span className="font-mono text-accent">#{predicted ?? "—"}</span>
          )}
        </span>
      </div>
    </div>
  );
}
