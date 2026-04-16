import { useState, useEffect } from 'react';
import api from '../services/api';

function MetricGauge({ percent, color }) {
  return (
    <div className="w-12 h-12 rounded-full border-4 flex items-center justify-center relative shadow-sm" style={{ borderColor: 'var(--bg-elevated)', borderTopColor: color, transform: 'rotate(-45deg)' }}>
      <div style={{ transform: 'rotate(45deg)' }} className="text-[10px] font-mono font-bold">
        {(percent * 100).toFixed(0)}
      </div>
    </div>
  );
}

export default function AnalysisDashboard() {
  const [keyword, setKeyword] = useState('');
  const [content, setContent] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const saved = localStorage.getItem('qontint_keyword');
    if (saved) setKeyword(saved);
  }, []);

  const handleAnalyze = async () => {
    if (!content.trim() || !keyword.trim()) return;
    setLoading(true); setError(null);
    try { const data = await api.analyzeContent(content, keyword); setAnalysis(data); }
    catch (err) { setError(err.message); }
    finally { setLoading(false); }
  };

  const passFail = analysis?.pass_fail;
  const passColor = passFail === 'PASS' ? 'var(--status-pass)' : passFail === 'FAIL' ? 'var(--status-fail)' : 'var(--text-muted)';

  return (
    <div className="flex flex-col xl:flex-row h-[calc(100vh-80px)] w-full max-w-[1600px] mx-auto animate-fade-in overflow-hidden border-t" style={{ borderColor: 'var(--border-default)' }}>
      
      {/* 1. INPUT ZONE (Left 25%) */}
      <div className="w-full xl:w-1/4 flex-shrink-0 flex flex-col border-r h-full overflow-y-auto" style={{ borderColor: 'var(--border-default)', background: 'var(--bg-primary)' }}>
        <div className="p-8 pb-4">
          <p className="text-[10px] uppercase tracking-[0.2em] font-bold mb-8" style={{ color: 'var(--text-muted)' }}>1. Data Context</p>
          <div className="flex flex-col gap-6">
            <div>
              <label className="text-[11px] font-bold uppercase tracking-widest mb-3 block" style={{ color: 'var(--text-primary)' }}>Target Query</label>
              <input type="text" value={keyword} onChange={e => setKeyword(e.target.value)}
                className="w-full h-12 px-4 text-sm transition-all shadow-sm border-2 focus:outline-none"
                style={{ background: 'var(--bg-surface)', borderColor: 'transparent', color: 'var(--text-primary)' }}
                onFocus={e => e.target.style.borderColor = 'var(--accent-copper)'}
                onBlur={e => e.target.style.borderColor = 'transparent'} />
            </div>
            <div className="flex-1 flex flex-col">
              <label className="text-[11px] font-bold uppercase tracking-widest mb-3 block" style={{ color: 'var(--text-primary)' }}>Source Content</label>
              <textarea value={content} onChange={e => setContent(e.target.value)} rows={15}
                className="w-full p-4 text-sm resize-none shadow-sm border-2 focus:outline-none flex-1"
                style={{ background: 'var(--bg-surface)', borderColor: 'transparent', color: 'var(--text-primary)', lineHeight: 1.6 }}
                onFocus={e => e.target.style.borderColor = 'var(--accent-copper)'}
                onBlur={e => e.target.style.borderColor = 'transparent'} />
            </div>
          </div>
        </div>
        
        <div className="mt-auto p-8 border-t" style={{ borderColor: 'var(--border-default)', background: 'var(--bg-elevated)' }}>
          <button onClick={handleAnalyze} disabled={loading || !content.trim() || !keyword.trim()}
            className="w-full h-14 text-[13px] uppercase tracking-[0.15em] font-bold transition-all shadow-md flex items-center justify-center gap-3 disabled:opacity-40"
            style={{ background: 'var(--accent-copper)', color: '#fff' }}
            onMouseEnter={e => { if(!loading) e.currentTarget.style.transform = 'translateY(-2px)' }}
            onMouseLeave={e => { if(!loading) e.currentTarget.style.transform = 'translateY(0)' }}>
            {loading ? <span className="animate-pulse">Processing...</span> : 'Run Analysis'}
          </button>
        </div>
      </div>

      {/* 2. INSIGHT ZONE (Center 50%) */}
      <div className="w-full xl:w-2/4 flex-shrink-0 flex flex-col h-full overflow-y-auto px-12 py-10" style={{ background: 'var(--bg-surface)' }}>
        {!analysis ? (
          <div className="flex-1 flex flex-col items-center justify-center text-center opacity-40">
            <span className="text-[40px] mb-4" style={{ fontFamily: 'var(--font-serif)' }}>§</span>
            <p className="text-sm font-medium tracking-wide">Enter data on the left to populate insights.</p>
          </div>
        ) : (
          <div className="flex flex-col gap-12 animate-fade-in max-w-3xl mx-auto w-full">
            <div className="flex items-center gap-6 pb-6 border-b" style={{ borderColor: 'var(--border-default)' }}>
              <p className="text-[10px] uppercase tracking-[0.2em] font-bold" style={{ color: 'var(--text-muted)' }}>2. Semantic Evaluation</p>
              <span className="text-xs font-mono px-2 py-1 rounded-sm" style={{ background: 'var(--bg-primary)', color: 'var(--text-muted)' }}>Model: XGBoost Contextual</span>
            </div>

            {/* Favorable Banner */}
            <div className="w-full p-8 rounded-sm flex items-center justify-between"
              style={{ background: passFail === 'PASS' ? 'rgba(124,143,110,0.05)' : 'rgba(196,126,126,0.05)', borderLeft: `8px solid ${passColor}` }}>
              <div>
                <h2 className="text-4xl mb-2" style={{ fontFamily: 'var(--font-serif)', color: 'var(--text-primary)' }}>
                  {passFail === 'PASS' ? 'Favorable Trajectory' : 'Content Deficient'}
                </h2>
                <p className="text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>Based on NLP cross-reference with top 10 competitors</p>
              </div>
              <span className="text-6xl pt-2 pl-4" style={{ color: passColor, fontFamily: 'var(--font-serif)' }}>{passFail === 'PASS' ? '✓' : '✗'}</span>
            </div>

            {/* Factor Insights */}
            <div className="grid grid-cols-2 gap-8">
              <div>
                <h4 className="text-[10px] uppercase tracking-[0.2em] font-bold mb-6" style={{ color: 'var(--text-primary)' }}>Entity Discovery</h4>
                <div className="flex flex-wrap gap-2">
                  {analysis.entities_found?.map((e, i) => (
                    <span key={i} className="px-3 py-1.5 rounded-sm text-xs transition-colors"
                      style={{ background: 'var(--bg-primary)', color: 'var(--text-secondary)' }}>
                      {e.text}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <h4 className="text-[10px] uppercase tracking-[0.2em] font-bold mb-6" style={{ color: 'var(--accent-gold)' }}>Priority Missing Entities</h4>
                <div className="flex flex-col gap-2 border-l pl-4" style={{ borderColor: 'var(--accent-gold)' }}>
                  {analysis.missing_entities?.slice(0, 5).map((e, i) => (
                    <div key={i} className="flex justify-between text-sm py-1">
                      <span className="font-semibold" style={{ color: 'var(--text-primary)' }}>{e.text}</span>
                      <span className="font-mono opacity-60">{(e.authority_score * 100).toFixed(0)}%</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            
            {/* Context Quality */}
            <div className="pt-4 border-t" style={{ borderColor: 'var(--border-default)' }}>
              <div className="flex justify-between items-center mb-6">
                <h4 className="text-[10px] uppercase tracking-[0.2em] font-bold" style={{ color: 'var(--text-primary)' }}>Writing Quality Matrix</h4>
                <span className="text-[10px] font-mono bg-black text-white px-2 py-1 uppercase tracking-widest">{analysis.intent_type} Intent</span>
              </div>
              <p className="text-sm leading-loose" style={{ color: 'var(--text-secondary)' }}>
                This document registers a composition quality score of <strong style={{ color:'var(--text-primary)' }}>{(analysis.content_quality * 100).toFixed(0)}%</strong>. 
                It matches structural intent alignment heavily with top SERP results ({(analysis.intent_alignment * 100).toFixed(0)}%), indicating correct format deployment.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* 3. METRIC ZONE (Right 25%) */}
      <div className="w-full xl:w-1/4 flex-shrink-0 flex flex-col border-l h-full overflow-y-auto p-8" style={{ borderColor: 'var(--border-default)', background: 'var(--bg-primary)' }}>
        {!analysis ? (
          <div className="opacity-0" />
        ) : (
          <div className="animate-fade-in pb-10">
            <p className="text-[10px] uppercase tracking-[0.2em] font-bold mb-10" style={{ color: 'var(--text-muted)' }}>3. Pure Metrics</p>
            
            <div className="flex items-center justify-between p-6 mb-10 rounded-sm" style={{ background: '#1a1a1a', color: '#fff' }}>
              <span className="text-xs uppercase tracking-[0.2em] font-bold opacity-60">Forecast Rank</span>
              <span className="text-4xl" style={{ fontFamily: 'var(--font-serif)' }}>#{analysis.predicted_rank}</span>
            </div>

            <div className="flex flex-col gap-8">
              {[
                { label: 'Total Novelty', val: analysis.novelty_score, col: 'var(--accent-copper)' },
                { label: 'Entity Cov.', val: analysis.entity_coverage, col: 'var(--accent-sage)' },
                { label: 'Rel. Completeness', val: analysis.relationship_completeness, col: 'var(--accent-teal)' },
                { label: 'Auth. Score', val: analysis.authority_score, col: 'var(--accent-gold)' },
              ].map(m => (
                <div key={m.label} className="flex items-center justify-between">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-widest" style={{ color: 'var(--text-primary)' }}>{m.label}</p>
                    <p className="text-[10px] font-mono mt-1 opacity-60">Weight factor</p>
                  </div>
                  <MetricGauge percent={m.val} color={m.col} />
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
