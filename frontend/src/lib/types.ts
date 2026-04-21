/**
 * Qontint — TypeScript types mirroring backend Pydantic schemas.
 * Keep in sync with backend/app/schemas/__init__.py
 */

// ─── Enums ──────────────────────────────────────────────────────────────

export type Vertical = "saas" | "mortgage" | "healthcare" | "finance" | "legal" | "insurance";
export type IntentType = "informational" | "transactional" | "navigational" | "commercial";
export type PassFail = "PASS" | "FAIL" | "PENDING";

// ─── Shared ─────────────────────────────────────────────────────────────

export interface EntityResponse {
  text: string;
  type: string;
  authority_score: number;
  frequency: number;
}

// ─── SERP ───────────────────────────────────────────────────────────────

export interface SerpCollectRequest {
  keyword: string;
  vertical: Vertical;
}

export interface SerpResultResponse {
  position: number;
  url: string;
  title?: string;
  snippet?: string;
  content_length?: number;
}

export interface SerpCollectResponse {
  keyword: string;
  vertical: string;
  total_results: number;
  results: SerpResultResponse[];
  collected_at: string;
}

// ─── Analysis ───────────────────────────────────────────────────────────

export interface AnalyzeRequest {
  content: string;
  keyword: string;
  vertical: Vertical;
}

export interface AnalyzeResponse {
  keyword: string;
  novelty_score: number;
  entity_novelty: number;
  relationship_novelty: number;
  semantic_diversity: number;
  predicted_rank: number;
  confidence_score: number;
  intent_alignment: number;
  intent_type: string;
  entity_coverage: number;
  relationship_completeness: number;
  authority_score: number;
  content_quality: number;
  pass_fail: string;
  entities_found: EntityResponse[];
  missing_entities: EntityResponse[];
  recommendations: Record<string, unknown>[];
  analyzed_at: string;
}

// ─── Prediction ─────────────────────────────────────────────────────────

export interface PredictRequest {
  content: string;
  keyword: string;
  vertical: Vertical;
}

export interface FeatureBreakdown {
  entity_coverage: number;
  relationship_completeness: number;
  authority_score: number;
  content_quality: number;
}

export interface PredictResponse {
  predicted_position: number;
  confidence: number;
  features: FeatureBreakdown;
  pass_fail: string;
}

// ─── Recommendations ────────────────────────────────────────────────────

export interface RecommendRequest {
  content: string;
  keyword: string;
  vertical: Vertical;
}

export interface RecommendationItem {
  entity: string;
  entity_type: string;
  authority_score: number;
  relevance_score: number;
  suggestion: string;
  context: string;
}

export interface RecommendResponse {
  keyword: string;
  current_novelty: number;
  recommendations: RecommendationItem[];
  potential_novelty_gain: number;
}

// ─── Generation ─────────────────────────────────────────────────────────

export interface GenerateRequest {
  keyword: string;
  vertical: Vertical;
  intent: IntentType;
  guidelines?: string;
  use_authority_entities?: boolean;
}

export interface GenerateResponse {
  content: string;
  keyword: string;
  intent: string;
  entities_used: string[];
  authority_entities: EntityResponse[];
  estimated_novelty: number;
  word_count: number;
}

// ─── Graph ───────────────────────────────────────────────────────────────

export interface GraphNode {
  id: string;
  label: string;
  type: string;
  authority: number;
  frequency: number;
  size: number;
}

export interface GraphEdge {
  source: string;
  target: string;
  relationship: string;
  weight: number;
}

export interface GraphStats {
  total_nodes: number;
  total_edges: number;
  avg_authority: number;
  top_entities: EntityResponse[];
}

export interface GraphResponse {
  keyword: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: GraphStats;
}
