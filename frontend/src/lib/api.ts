/**
 * Qontint — API Client
 * All calls go to VITE_API_URL (default: http://localhost:8000)
 */

import type {
  SerpCollectRequest,
  SerpCollectResponse,
  AnalyzeRequest,
  AnalyzeResponse,
  PredictRequest,
  PredictResponse,
  RecommendRequest,
  RecommendResponse,
  GenerateRequest,
  GenerateResponse,
  GraphResponse,
} from "./types";

const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const V1 = `${BASE}/api/v1`;

// ─── Generic fetch helper ───────────────────────────────────────────────

async function post<TReq, TRes>(path: string, body: TReq): Promise<TRes> {
  const res = await fetch(`${V1}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API ${path} failed (${res.status}): ${detail}`);
  }

  return res.json() as Promise<TRes>;
}

async function get<TRes>(path: string): Promise<TRes> {
  const res = await fetch(`${V1}${path}`);

  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API ${path} failed (${res.status}): ${detail}`);
  }

  return res.json() as Promise<TRes>;
}

// ─── Health ─────────────────────────────────────────────────────────────

export async function checkHealth(): Promise<{ status: string }> {
  const res = await fetch(`${BASE}/health`);
  return res.json();
}

// ─── SERP ───────────────────────────────────────────────────────────────

export async function collectSerp(req: SerpCollectRequest): Promise<SerpCollectResponse> {
  return post<SerpCollectRequest, SerpCollectResponse>("/serp/collect", req);
}

// ─── Analysis ───────────────────────────────────────────────────────────

export async function analyzeContent(req: AnalyzeRequest): Promise<AnalyzeResponse> {
  return post<AnalyzeRequest, AnalyzeResponse>("/analyze", req);
}

// ─── Prediction ─────────────────────────────────────────────────────────

export async function predictRanking(req: PredictRequest): Promise<PredictResponse> {
  return post<PredictRequest, PredictResponse>("/predict", req);
}

// ─── Recommendations ────────────────────────────────────────────────────

export async function getRecommendations(req: RecommendRequest): Promise<RecommendResponse> {
  return post<RecommendRequest, RecommendResponse>("/recommend", req);
}

// ─── Generation ─────────────────────────────────────────────────────────

export async function generateContent(req: GenerateRequest): Promise<GenerateResponse> {
  return post<GenerateRequest, GenerateResponse>("/generate", req);
}

// ─── Graph ───────────────────────────────────────────────────────────────

export async function getGraph(keyword: string): Promise<GraphResponse> {
  return get<GraphResponse>(`/graph/${encodeURIComponent(keyword)}`);
}
