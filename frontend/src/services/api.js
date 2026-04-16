const API_BASE = '/api/v1';

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `API Error: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`API call failed: ${endpoint}`, error);
      throw error;
    }
  }

  // ─── SERP ──────────────────────────────────────────────────────
  async collectSerp(keyword, vertical = 'saas') {
    return this.request('/serp/collect', {
      method: 'POST',
      body: JSON.stringify({ keyword, vertical }),
    });
  }

  // ─── Analysis ──────────────────────────────────────────────────
  async analyzeContent(content, keyword, vertical = 'saas') {
    return this.request('/analyze', {
      method: 'POST',
      body: JSON.stringify({ content, keyword, vertical }),
    });
  }

  // ─── Prediction ────────────────────────────────────────────────
  async predictRanking(content, keyword, vertical = 'saas') {
    return this.request('/predict', {
      method: 'POST',
      body: JSON.stringify({ content, keyword, vertical }),
    });
  }

  // ─── Generation ────────────────────────────────────────────────
  async generateContent(keyword, vertical = 'saas', intent = 'informational', guidelines = '') {
    return this.request('/generate', {
      method: 'POST',
      body: JSON.stringify({ keyword, vertical, intent, guidelines, use_authority_entities: true }),
    });
  }

  // ─── Recommendations ──────────────────────────────────────────
  async getRecommendations(content, keyword, vertical = 'saas') {
    return this.request('/recommend', {
      method: 'POST',
      body: JSON.stringify({ content, keyword, vertical }),
    });
  }

  // ─── Graph ─────────────────────────────────────────────────────
  async getGraph(keyword) {
    return this.request(`/graph/${encodeURIComponent(keyword)}`);
  }

  // ─── Workflow ──────────────────────────────────────────────────
  async runWorkflow(keyword, vertical = 'saas', intent = 'informational', guidelines = '') {
    return this.request('/workflow', {
      method: 'POST',
      body: JSON.stringify({ keyword, vertical, intent, guidelines }),
    });
  }
}

export const api = new ApiService();
export default api;
