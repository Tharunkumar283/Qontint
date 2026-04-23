import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { z } from "zod";
import { analyzeYouTube, predictYouTube } from "@/lib/api";
import type { YouTubeAnalyzeResponse, YouTubePredictResponse } from "@/lib/types";

export const Route = createFileRoute("/youtube")({
  head: () => ({
    meta: [
      { title: "YouTube Ranking Prediction — Qontint" },
      { name: "description", content: "Predict how your video will perform on YouTube before publishing. Analyze top videos, extract topics, and get optimization recommendations." },
    ],
  }),
  component: YouTubePage,
});

type Tab = "analyze" | "predict";

function YouTubePage() {
  const [tab, setTab] = useState<Tab>("analyze");
  const [query, setQuery] = useState("");
  const [analyzeResult, setAnalyzeResult] = useState<YouTubeAnalyzeResponse | null>(null);
  const [analyzeLoading, setAnalyzeLoading] = useState(false);
  const [analyzeError, setAnalyzeError] = useState("");

  // Predict form state
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [tags, setTags] = useState("");
  const [outline, setOutline] = useState("");
  const [predictQuery, setPredictQuery] = useState("");
  const [predictResult, setPredictResult] = useState<YouTubePredictResponse | null>(null);
  const [predictLoading, setPredictLoading] = useState(false);
  const [predictError, setPredictError] = useState("");

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setAnalyzeLoading(true);
    setAnalyzeError("");
    try {
      const res = await analyzeYouTube({ query: query.trim(), max_videos: 10 });
      setAnalyzeResult(res);
      setPredictQuery(query.trim());
    } catch (err) {
      setAnalyzeError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setAnalyzeLoading(false);
    }
  };

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !predictQuery.trim()) return;
    setPredictLoading(true);
    setPredictError("");
    try {
      const res = await predictYouTube({
        title: title.trim(),
        description: description.trim(),
        tags: tags.split(",").map((t) => t.trim()).filter(Boolean),
        transcript_outline: outline.trim(),
        query: predictQuery.trim(),
      });
      setPredictResult(res);
    } catch (err) {
      setPredictError(err instanceof Error ? err.message : "Prediction failed");
    } finally {
      setPredictLoading(false);
    }
  };

  const examples = [
    "best mortgage rates 2025",
    "how to refinance a home loan",
    "saas pricing strategies",
    "ozempic side effects explained",
    "small business tax deductions",
  ];

  return (
    <div className="container mx-auto px-6 py-12 lg:px-8 lg:py-16">
      {/* Header */}
      <div className="max-w-3xl">
        <div className="inline-flex items-center gap-2 rounded-full border border-border-strong/60 bg-surface-raised/40 px-3 py-1 text-xs">
          <span className="font-mono text-red-400">▶</span>
          <span className="text-foreground/80">YouTube Ranking — NEW</span>
        </div>
        <h1 className="mt-5 font-display text-4xl font-semibold tracking-tight text-balance lg:text-5xl">
          Predict your YouTube ranking{" "}
          <span className="gradient-text-accent">before you publish</span>
        </h1>
        <p className="mt-4 max-w-2xl text-lg leading-relaxed text-muted-foreground">
          Qontint analyzes top-performing videos for any query — extracts topics, tags, and content patterns — then predicts how your planned video will rank before you hit upload.
        </p>
      </div>

      {/* Stats bar */}
      <div className="mt-8 flex flex-wrap gap-6 border-t border-b border-border/60 py-5 text-sm">
        {[
          { k: "Video content", v: "500h uploaded/min" },
          { k: "Competitor intelligence", v: "Top 10 analyzed" },
          { k: "Prediction accuracy", v: "Script + tags + title" },
        ].map((s) => (
          <div key={s.k}>
            <span className="text-muted-foreground">{s.k}: </span>
            <span className="font-semibold text-foreground">{s.v}</span>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="mt-10 flex gap-1 border-b border-border">
        {(["analyze", "predict"] as Tab[]).map((t) => (
          <button
            key={t}
            id={`youtube-tab-${t}`}
            onClick={() => setTab(t)}
            className={`relative px-5 py-2.5 text-sm font-medium capitalize transition-colors ${
              tab === t ? "text-foreground" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {t === "analyze" ? "🔍 Analyze Top Videos" : "🎯 Predict My Video"}
            {tab === t && (
              <span className="absolute inset-x-0 -bottom-px h-0.5 bg-accent shadow-[0_0_10px_var(--accent)]" />
            )}
          </button>
        ))}
      </div>

      {/* ── ANALYZE TAB ── */}
      {tab === "analyze" && (
        <div className="mt-8">
          <form onSubmit={handleAnalyze} className="max-w-2xl">
            <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Search query / keyword
            </label>
            <div className="mt-2 flex gap-2">
              <input
                id="yt-analyze-query"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. best mortgage rates 2025"
                className="flex-1 rounded-md border border-border-strong bg-background/60 px-4 py-2.5 text-sm outline-none placeholder:text-muted-foreground/50 focus:border-accent focus:ring-2 focus:ring-accent/25"
              />
              <button
                type="submit"
                disabled={analyzeLoading || !query.trim()}
                className="rounded-md bg-red-500 px-5 py-2.5 text-sm font-semibold text-white transition-all hover:bg-red-400 disabled:opacity-50"
              >
                {analyzeLoading ? (
                  <span className="flex items-center gap-2">
                    <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                    Analyzing…
                  </span>
                ) : (
                  "Analyze →"
                )}
              </button>
            </div>
            <div className="mt-2 flex flex-wrap gap-2">
              <span className="text-xs text-muted-foreground">Try:</span>
              {examples.map((ex) => (
                <button
                  key={ex}
                  type="button"
                  onClick={() => setQuery(ex)}
                  className="rounded-full border border-border bg-background/40 px-2.5 py-0.5 text-xs text-foreground/80 hover:border-accent/40"
                >
                  {ex}
                </button>
              ))}
            </div>
          </form>

          {analyzeError && (
            <div className="mt-4 max-w-2xl rounded-md border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive">
              ⚠ {analyzeError}
            </div>
          )}

          {analyzeResult && (
            <div className="mt-8 space-y-8">
              {/* Benchmarks */}
              <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                {[
                  { label: "Videos analyzed", value: String(analyzeResult.videos_analyzed) },
                  { label: "Avg engagement rate", value: `${(analyzeResult.benchmarks.avg_engagement_rate * 100).toFixed(1)}%` },
                  { label: "Optimal duration", value: analyzeResult.benchmarks.optimal_duration_range },
                  { label: "Optimal title", value: analyzeResult.benchmarks.optimal_title_length },
                ].map((m) => (
                  <div key={m.label} className="rounded-xl border border-border bg-surface/60 p-4">
                    <div className="text-xs text-muted-foreground">{m.label}</div>
                    <div className="mt-1 font-display text-2xl font-semibold">{m.value}</div>
                  </div>
                ))}
              </section>

              {/* Top Videos */}
              <section>
                <h2 className="font-display text-lg font-semibold">Top performing videos</h2>
                <div className="mt-4 space-y-3">
                  {analyzeResult.top_videos.slice(0, 5).map((v, i) => (
                    <div key={v.video_id} className="rounded-xl border border-border bg-surface/60 p-4">
                      <div className="flex items-start gap-3">
                        <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-red-500/15 font-mono text-xs font-bold text-red-400">
                          #{i + 1}
                        </span>
                        <div className="flex-1 min-w-0">
                          <div className="font-display text-sm font-semibold leading-tight">{v.title}</div>
                          <div className="mt-0.5 text-xs text-muted-foreground">{v.channel}</div>
                          <div className="mt-2 flex flex-wrap gap-3 text-xs text-muted-foreground">
                            <span>{v.views.toLocaleString()} views</span>
                            <span>·</span>
                            <span>{Math.round(v.duration_seconds / 60)}min</span>
                            <span>·</span>
                            <span className="text-success">{(v.engagement_rate * 100).toFixed(0)}% engagement</span>
                          </div>
                          {v.tags.length > 0 && (
                            <div className="mt-2 flex flex-wrap gap-1">
                              {v.tags.slice(0, 5).map((tag) => (
                                <span key={tag} className="rounded-full border border-border bg-surface-raised/60 px-2 py-0.5 text-[10px] font-medium text-muted-foreground">
                                  {tag}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              {/* Common Topics + Top Tags */}
              <div className="grid gap-6 lg:grid-cols-2">
                <section>
                  <h2 className="font-display text-lg font-semibold">Common topics</h2>
                  <ul className="mt-4 space-y-2">
                    {analyzeResult.common_topics.slice(0, 8).map((t) => (
                      <li key={t.term} className="flex items-center justify-between rounded-lg border border-border bg-surface/60 px-4 py-2.5 text-sm">
                        <span className="font-medium capitalize">{t.term}</span>
                        <span className="font-mono text-xs text-muted-foreground">×{t.frequency}</span>
                      </li>
                    ))}
                  </ul>
                </section>
                <section>
                  <h2 className="font-display text-lg font-semibold">High-performing tags</h2>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {analyzeResult.top_tags.slice(0, 15).map((t) => (
                      <span key={t.tag} className="rounded-full border border-accent/30 bg-accent/5 px-3 py-1 text-xs font-medium text-accent">
                        {t.tag}{" "}
                        <span className="text-muted-foreground">×{t.count}</span>
                      </span>
                    ))}
                  </div>
                  <button
                    className="mt-4 text-sm font-medium text-accent hover:underline"
                    onClick={() => { setPredictQuery(query); setTab("predict"); }}
                  >
                    Use these insights to predict my video →
                  </button>
                </section>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ── PREDICT TAB ── */}
      {tab === "predict" && (
        <div className="mt-8 grid gap-8 lg:grid-cols-2">
          {/* Form */}
          <form onSubmit={handlePredict} className="space-y-5">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Target query / keyword
              </label>
              <input
                id="yt-predict-query"
                value={predictQuery}
                onChange={(e) => setPredictQuery(e.target.value)}
                placeholder="e.g. best mortgage rates 2025"
                required
                className="mt-1.5 w-full rounded-md border border-border-strong bg-background/60 px-4 py-2.5 text-sm outline-none placeholder:text-muted-foreground/50 focus:border-accent focus:ring-2 focus:ring-accent/25"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Video title
              </label>
              <input
                id="yt-predict-title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Lowest Mortgage Rates in 2025 — How to Qualify"
                required
                className="mt-1.5 w-full rounded-md border border-border-strong bg-background/60 px-4 py-2.5 text-sm outline-none placeholder:text-muted-foreground/50 focus:border-accent focus:ring-2 focus:ring-accent/25"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Description
              </label>
              <textarea
                id="yt-predict-desc"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Write your video description (150-200 words recommended)…"
                rows={4}
                className="mt-1.5 w-full resize-none rounded-md border border-border-strong bg-background/60 px-4 py-2.5 text-sm outline-none placeholder:text-muted-foreground/50 focus:border-accent focus:ring-2 focus:ring-accent/25"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Tags (comma separated)
              </label>
              <input
                id="yt-predict-tags"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                placeholder="mortgage rates, refinance, home loan, FHA loan"
                className="mt-1.5 w-full rounded-md border border-border-strong bg-background/60 px-4 py-2.5 text-sm outline-none placeholder:text-muted-foreground/50 focus:border-accent focus:ring-2 focus:ring-accent/25"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Script outline / transcript
              </label>
              <textarea
                id="yt-predict-outline"
                value={outline}
                onChange={(e) => setOutline(e.target.value)}
                placeholder="Paste your script outline or key talking points here. The more detail, the better the prediction."
                rows={6}
                className="mt-1.5 w-full resize-none rounded-md border border-border-strong bg-background/60 px-4 py-2.5 text-sm outline-none placeholder:text-muted-foreground/50 focus:border-accent focus:ring-2 focus:ring-accent/25"
              />
            </div>

            {predictError && (
              <div className="rounded-md border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive">
                ⚠ {predictError}
              </div>
            )}

            <button
              id="yt-predict-submit"
              type="submit"
              disabled={predictLoading || !title.trim() || !predictQuery.trim()}
              className="w-full rounded-md bg-accent px-5 py-3 text-sm font-semibold text-accent-foreground shadow-[0_0_20px_-6px_var(--accent)] transition-all hover:bg-accent-glow disabled:opacity-50"
            >
              {predictLoading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="h-4 w-4 animate-spin rounded-full border-2 border-accent-foreground/30 border-t-accent-foreground" />
                  Predicting…
                </span>
              ) : (
                "Predict ranking potential →"
              )}
            </button>
          </form>

          {/* Results */}
          <div>
            {!predictResult ? (
              <div className="rounded-xl border border-dashed border-border bg-surface/40 p-8 text-center text-muted-foreground">
                <div className="text-4xl">🎬</div>
                <p className="mt-3 text-sm">Fill in your video details and click "Predict" to see how it will perform on YouTube.</p>
              </div>
            ) : (
              <div className="space-y-5">
                {/* Overall score */}
                <div className={`rounded-xl border p-6 text-center ${
                  predictResult.pass_threshold
                    ? "border-success/40 bg-success/5"
                    : "border-warning/40 bg-warning/5"
                }`}>
                  <div className="font-mono text-5xl font-bold">
                    {Math.round(predictResult.scores.overall * 100)}
                    <span className="text-2xl text-muted-foreground">/100</span>
                  </div>
                  <div className="mt-2 font-display text-xl font-semibold">{predictResult.predicted_tier}</div>
                  <div className="mt-1 text-sm text-muted-foreground">
                    Top {100 - predictResult.predicted_percentile}% of videos for this query
                  </div>
                  <div className={`mt-3 inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wider ${
                    predictResult.pass_threshold
                      ? "bg-success/15 text-success"
                      : "bg-warning/15 text-warning"
                  }`}>
                    {predictResult.pass_threshold ? "✓ Publishing-ready" : "⚠ Needs optimization"}
                  </div>
                </div>

                {/* Score breakdown */}
                <div className="rounded-xl border border-border bg-surface/60 p-5">
                  <h3 className="font-display text-sm font-semibold">Score breakdown</h3>
                  <div className="mt-4 space-y-3">
                    {[
                      { label: "Title optimization", key: "title_optimization", weight: "35%" },
                      { label: "Content depth", key: "content_depth", weight: "30%" },
                      { label: "Tag coverage", key: "tag_coverage", weight: "20%" },
                      { label: "Description quality", key: "description_quality", weight: "15%" },
                    ].map((s) => {
                      const val = Math.round((predictResult.scores as any)[s.key] * 100);
                      return (
                        <div key={s.key}>
                          <div className="flex justify-between text-xs">
                            <span className="text-foreground/85">{s.label}</span>
                            <span className="font-mono text-muted-foreground">{val}% · w {s.weight}</span>
                          </div>
                          <div className="mt-1.5 h-2 overflow-hidden rounded-full bg-surface-raised">
                            <div
                              className="h-full rounded-full bg-gradient-to-r from-accent to-accent-glow transition-all duration-700"
                              style={{ width: `${val}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Recommendations */}
                {predictResult.recommendations.length > 0 && (
                  <div className="rounded-xl border border-border bg-surface/60 p-5">
                    <h3 className="font-display text-sm font-semibold">Optimization recommendations</h3>
                    <ul className="mt-4 space-y-3">
                      {predictResult.recommendations.map((r, i) => (
                        <li key={i} className="rounded-lg border border-border bg-background/40 p-3">
                          <div className="flex items-center gap-2">
                            <span className={`rounded px-1.5 py-0.5 text-[10px] font-bold uppercase ${
                              r.priority === "HIGH" ? "bg-destructive/15 text-destructive" : "bg-warning/15 text-warning"
                            }`}>
                              {r.priority}
                            </span>
                            <span className="text-xs font-medium uppercase text-muted-foreground">{r.type}</span>
                            <span className="ml-auto text-xs font-semibold text-success">{r.impact}</span>
                          </div>
                          <p className="mt-1.5 text-xs leading-relaxed text-muted-foreground">{r.suggestion}</p>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
