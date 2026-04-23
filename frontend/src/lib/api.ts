/**
 * Qontint — API Client
 * All calls go to VITE_API_URL (default: http://localhost:8000)
 */

import type {
  SerpCollectRequest, SerpCollectResponse,
  AnalyzeRequest, AnalyzeResponse,
  PredictRequest, PredictResponse,
  RecommendRequest, RecommendResponse,
  GenerateRequest, GenerateResponse,
  GraphResponse,
  AuthRequest, AuthResponse, User,
  YouTubeAnalyzeRequest, YouTubeAnalyzeResponse,
  YouTubePredictRequest, YouTubePredictResponse,
  ExportRequest,
} from "./types";

const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const V1 = `${BASE}/api/v1`;

// ─── Token storage ────────────────────────────────────────────────────────

export const getToken = (): string | null => localStorage.getItem("qontint_token");
export const setToken = (t: string) => localStorage.setItem("qontint_token", t);
export const clearToken = () => localStorage.removeItem("qontint_token");
export const getStoredUser = (): User | null => {
  try { return JSON.parse(localStorage.getItem("qontint_user") || "null"); }
  catch { return null; }
};
export const setStoredUser = (u: User) => localStorage.setItem("qontint_user", JSON.stringify(u));
export const clearStoredUser = () => localStorage.removeItem("qontint_user");

// ─── Generic fetch helpers ────────────────────────────────────────────────

function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function post<TReq, TRes>(path: string, body: TReq, withAuth = false): Promise<TRes> {
  const res = await fetch(`${V1}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(withAuth ? authHeaders() : {}),
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API ${path} failed (${res.status}): ${detail}`);
  }
  return res.json() as Promise<TRes>;
}

async function get<TRes>(path: string, withAuth = false): Promise<TRes> {
  const res = await fetch(`${V1}${path}`, {
    headers: withAuth ? authHeaders() : {},
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API ${path} failed (${res.status}): ${detail}`);
  }
  return res.json() as Promise<TRes>;
}

// ─── Health ────────────────────────────────────────────────────────────────

export async function checkHealth(): Promise<{ status: string }> {
  const res = await fetch(`${BASE}/health`);
  return res.json();
}

// ─── SERP ──────────────────────────────────────────────────────────────────

export async function collectSerp(req: SerpCollectRequest): Promise<SerpCollectResponse> {
  return post<SerpCollectRequest, SerpCollectResponse>("/serp/collect", req);
}

// ─── Analysis ──────────────────────────────────────────────────────────────

export async function analyzeContent(req: AnalyzeRequest): Promise<AnalyzeResponse> {
  return post<AnalyzeRequest, AnalyzeResponse>("/analyze", req);
}

// ─── Prediction ────────────────────────────────────────────────────────────

export async function predictRanking(req: PredictRequest): Promise<PredictResponse> {
  return post<PredictRequest, PredictResponse>("/predict", req);
}

// ─── Recommendations ───────────────────────────────────────────────────────

export async function getRecommendations(req: RecommendRequest): Promise<RecommendResponse> {
  return post<RecommendRequest, RecommendResponse>("/recommend", req);
}

// ─── Generation ────────────────────────────────────────────────────────────

export async function generateContent(req: GenerateRequest): Promise<GenerateResponse> {
  return post<GenerateRequest, GenerateResponse>("/generate", req);
}

// ─── Graph ─────────────────────────────────────────────────────────────────

export async function getGraph(keyword: string): Promise<GraphResponse> {
  return get<GraphResponse>(`/graph/${encodeURIComponent(keyword)}`);
}

// ─── Auth ──────────────────────────────────────────────────────────────────

export async function register(req: AuthRequest): Promise<AuthResponse> {
  const res = await post<AuthRequest, AuthResponse>("/auth/register", req);
  if (res.success && res.token && res.user) {
    setToken(res.token);
    setStoredUser(res.user);
  }
  return res;
}

export async function login(req: AuthRequest): Promise<AuthResponse> {
  const res = await post<AuthRequest, AuthResponse>("/auth/login", req);
  if (res.success && res.token && res.user) {
    setToken(res.token);
    setStoredUser(res.user);
  }
  return res;
}

export async function getMe(): Promise<User> {
  return get<User>("/auth/me", true);
}

export async function logout() {
  clearToken();
  clearStoredUser();
}

// ─── YouTube ───────────────────────────────────────────────────────────────

export async function analyzeYouTube(req: YouTubeAnalyzeRequest): Promise<YouTubeAnalyzeResponse> {
  return post<YouTubeAnalyzeRequest, YouTubeAnalyzeResponse>("/youtube/analyze", req);
}

export async function predictYouTube(req: YouTubePredictRequest): Promise<YouTubePredictResponse> {
  return post<YouTubePredictRequest, YouTubePredictResponse>("/youtube/predict", req);
}

// ─── Export ────────────────────────────────────────────────────────────────

export async function exportAnalysisJson(req: ExportRequest): Promise<void> {
  const res = await fetch(`${V1}/export/json`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error("Export failed");
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `qontint-${req.keyword.replace(/\s+/g, "-")}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

export async function exportAnalysisCsv(req: ExportRequest): Promise<void> {
  const res = await fetch(`${V1}/export/csv`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error("Export failed");
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `qontint-${req.keyword.replace(/\s+/g, "-")}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}
