/**
 * Stylized SVG knowledge graph visualization.
 * Accepts a `keyword` prop to fetch live data from /api/v1/graph/{keyword}.
 * Falls back to hardcoded demo data when no keyword or data is unavailable.
 */

import { useEffect, useState } from "react";
import { getGraph } from "@/lib/api";
import type { GraphNode as ApiNode, GraphEdge as ApiEdge } from "@/lib/types";

// ─── Internal SVG types ──────────────────────────────────────────────────

type SvgNode = {
  id: string;
  label: string;
  x: number;
  y: number;
  r: number;
  authority: number;
  group?: "primary" | "secondary" | "missing";
};

type SvgEdge = { from: string; to: string; weight: number };

// ─── Static demo data (shown when no keyword / API not ready) ─────────────

const demoNodes: SvgNode[] = [
  { id: "n1", label: "Mortgage Rates", x: 300, y: 200, r: 34, authority: 0.95, group: "primary" },
  { id: "n2", label: "APR", x: 130, y: 110, r: 22, authority: 0.74, group: "secondary" },
  { id: "n3", label: "Refinance", x: 470, y: 110, r: 24, authority: 0.78, group: "secondary" },
  { id: "n4", label: "FHA Loan", x: 110, y: 290, r: 20, authority: 0.66, group: "secondary" },
  { id: "n5", label: "Credit Score", x: 510, y: 320, r: 22, authority: 0.71, group: "secondary" },
  { id: "n6", label: "Down Payment", x: 300, y: 360, r: 19, authority: 0.6, group: "secondary" },
  { id: "n7", label: "Federal Reserve", x: 240, y: 70, r: 16, authority: 0.55, group: "missing" },
  { id: "n8", label: "Yield Curve", x: 380, y: 50, r: 14, authority: 0.5, group: "missing" },
  { id: "n9", label: "Discount Points", x: 560, y: 220, r: 14, authority: 0.45, group: "missing" },
];

const demoEdges: SvgEdge[] = [
  { from: "n1", to: "n2", weight: 0.8 },
  { from: "n1", to: "n3", weight: 0.9 },
  { from: "n1", to: "n4", weight: 0.6 },
  { from: "n1", to: "n5", weight: 0.7 },
  { from: "n1", to: "n6", weight: 0.65 },
  { from: "n2", to: "n7", weight: 0.4 },
  { from: "n2", to: "n8", weight: 0.35 },
  { from: "n3", to: "n9", weight: 0.45 },
  { from: "n3", to: "n5", weight: 0.5 },
  { from: "n4", to: "n6", weight: 0.45 },
  { from: "n5", to: "n6", weight: 0.4 },
];

// ─── API → SVG mappers ────────────────────────────────────────────────────

const SVG_W = 640;
const SVG_H = 420;

/**
 * Place nodes in a simple circle layout.
 * The highest-authority node goes to the centre.
 */
function layoutNodes(apiNodes: ApiNode[]): SvgNode[] {
  if (apiNodes.length === 0) return [];

  const sorted = [...apiNodes].sort((a, b) => b.authority - a.authority);
  const cx = SVG_W / 2;
  const cy = SVG_H / 2;
  const radius = Math.min(cx, cy) * 0.7;

  return sorted.map((n, i) => {
    const isCenter = i === 0;
    const angle = ((2 * Math.PI) / (sorted.length - 1)) * (i - 1) - Math.PI / 2;
    const x = isCenter ? cx : cx + radius * Math.cos(angle);
    const y = isCenter ? cy : cy + radius * Math.sin(angle);
    const r = isCenter ? 32 : 10 + n.authority * 16;
    const group: SvgNode["group"] = isCenter ? "primary" : n.authority > 0.5 ? "secondary" : "missing";

    return { id: n.id, label: n.label, x, y, r, authority: n.authority, group };
  });
}

function mapEdges(apiEdges: ApiEdge[], nodeIds: Set<string>): SvgEdge[] {
  return apiEdges
    .filter((e) => nodeIds.has(e.source) && nodeIds.has(e.target))
    .map((e) => ({ from: e.source, to: e.target, weight: e.weight }));
}

// ─── Component ────────────────────────────────────────────────────────────

export function EntityGraph({
  keyword,
  height = 420,
}: {
  keyword?: string;
  height?: number;
}) {
  const [nodes, setNodes] = useState<SvgNode[]>(demoNodes);
  const [edges, setEdges] = useState<SvgEdge[]>(demoEdges);
  const [fetching, setFetching] = useState(false);

  useEffect(() => {
    if (!keyword) return;

    setFetching(true);
    getGraph(keyword)
      .then((data) => {
        if (data.nodes.length > 0) {
          const svgNodes = layoutNodes(data.nodes);
          const nodeIds = new Set(svgNodes.map((n) => n.id));
          setNodes(svgNodes);
          setEdges(mapEdges(data.edges, nodeIds));
        }
        // If empty graph, keep demo data
      })
      .catch(() => {
        // Silently fall back to demo data
      })
      .finally(() => setFetching(false));
  }, [keyword]);

  const byId = Object.fromEntries(nodes.map((n) => [n.id, n]));

  const colorFor = (g?: SvgNode["group"]) => {
    if (g === "primary") return "var(--accent)";
    if (g === "missing") return "var(--info)";
    return "oklch(87.31% 0.0097 296.29)";
  };

  return (
    <div className="relative overflow-hidden rounded-xl border border-border bg-surface/40">
      <div className="absolute inset-0 grid-bg opacity-60" aria-hidden />
      {fetching && (
        <div className="absolute inset-0 flex items-center justify-center bg-background/40 backdrop-blur-sm z-10">
          <span className="h-6 w-6 animate-spin rounded-full border-2 border-accent/30 border-t-accent" />
        </div>
      )}
      <svg
        viewBox={`0 0 ${SVG_W} ${SVG_H}`}
        className="relative w-full"
        style={{ height }}
        role="img"
        aria-label="Entity authority knowledge graph"
      >
        <defs>
          <radialGradient id="nodeGradAccent" cx="35%" cy="35%">
            <stop offset="0%" stopColor="oklch(82% 0.16 56.34)" />
            <stop offset="100%" stopColor="oklch(60% 0.16 56.34)" />
          </radialGradient>
          <radialGradient id="nodeGradInfo" cx="35%" cy="35%">
            <stop offset="0%" stopColor="oklch(78% 0.13 230)" />
            <stop offset="100%" stopColor="oklch(55% 0.13 230)" />
          </radialGradient>
          <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="6" result="b" />
            <feMerge>
              <feMergeNode in="b" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {edges.map((e, i) => {
          const a = byId[e.from];
          const b = byId[e.to];
          if (!a || !b) return null;
          const dashed = b.group === "missing" || a.group === "missing";
          return (
            <line
              key={i}
              x1={a.x}
              y1={a.y}
              x2={b.x}
              y2={b.y}
              stroke="oklch(66.82% 0.0105 294.32)"
              strokeOpacity={0.25 + e.weight * 0.4}
              strokeWidth={0.6 + e.weight * 1.2}
              strokeDasharray={dashed ? "4 4" : undefined}
            />
          );
        })}

        {nodes.map((n) => {
          const isPrimary = n.group === "primary";
          const isMissing = n.group === "missing";
          const fill = isPrimary
            ? "url(#nodeGradAccent)"
            : isMissing
              ? "url(#nodeGradInfo)"
              : "oklch(30.86% 0.0064 286.77)";
          return (
            <g key={n.id} filter={isPrimary ? "url(#softGlow)" : undefined}>
              <circle
                cx={n.x}
                cy={n.y}
                r={n.r}
                fill={fill}
                stroke={colorFor(n.group)}
                strokeOpacity={isMissing ? 0.7 : 0.4}
                strokeWidth={isPrimary ? 1.2 : 1}
              />
              <text
                x={n.x}
                y={n.y + n.r + 14}
                textAnchor="middle"
                fontSize="11"
                fontFamily="Inter, sans-serif"
                fontWeight={500}
                fill={isPrimary ? "oklch(95.86% 0.0042 297.32)" : "oklch(77.11% 0.0107 295.41)"}
              >
                {n.label.length > 18 ? n.label.slice(0, 16) + "…" : n.label}
              </text>
              {isMissing && (
                <text x={n.x} y={n.y + 4} textAnchor="middle" fontSize="10" fill="oklch(95% 0 0)">
                  +
                </text>
              )}
            </g>
          );
        })}
      </svg>
      <div className="pointer-events-none absolute bottom-3 left-4 flex items-center gap-4 text-[11px] text-muted-foreground">
        <span className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full bg-accent" /> Core
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full bg-foreground/60" /> Covered
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full bg-info" /> Missing
        </span>
      </div>
    </div>
  );
}
