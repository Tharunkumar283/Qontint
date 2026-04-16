import { useState, useEffect } from 'react';
import api from '../services/api';

function TopNavInput({ keyword, setKeyword, content, setContent, onPredict, loading }) {
  const [expanded, setExpanded] = useState(!keyword || !content);

  if (!expanded) {
    return (
      <div className="flex items-center justify-between p-4 border-b" style={{ borderColor: 'var(--border-default)', background: 'var(--bg-surface)' }}>
        <div className="flex items-center gap-6 text-xs">
          <span className="uppercase tracking-widest font-bold" style={{ color: 'var(--text-muted)' }}>Targeting:</span>
          <span className="font-medium" style={{ color: 'var(--text-primary)' }}>{keyword || 'None'}</span>
        </div>
        <button onClick={() => setExpanded(true)} className="text-[10px] uppercase tracking-widest font-bold underline" style={{ color: 'var(--text-secondary)' }}>Edit Configuration</button>
      </div>
    );
  }

  return (
    <div className="flex flex-col border-b" style={{ borderColor: 'var(--border-default)', background: 'var(--bg-primary)' }}>
      <div className="p-8 max-w-4xl flex flex-col gap-4">
        <p className="text-[10px] uppercase tracking-[0.2em] font-bold" style={{ color: 'var(--text-primary)' }}>Model Configuration</p>
        <input type="text" value={keyword} onChange={e => setKeyword(e.target.value)} placeholder="Enter Keyword..."
          className="w-full h-12 px-4 shadow-sm text-sm border focus:outline-none" style={{ borderColor: 'transparent' }} 
          onFocus={e => e.target.style.borderColor = 'var(--accent-copper)'} onBlur={e => e.target.style.borderColor = 'transparent'} />
        <textarea value={content} onChange={e => setContent(e.target.value)} placeholder="Paste Content..." rows={3}
          className="w-full p-4 shadow-sm text-sm border focus:outline-none resize-none" style={{ borderColor: 'transparent' }}
          onFocus={e => e.target.style.borderColor = 'var(--accent-copper)'} onBlur={e => e.target.style.borderColor = 'transparent'} />
        <div className="flex justify-end gap-4 mt-2">
          {keyword && content && (
            <button onClick={() => setExpanded(false)} className="px-6 h-12 text-xs uppercase tracking-widest font-bold" style={{ color: 'var(--text-muted)' }}>Cancel</button>
          )}
          <button onClick={() => { onPredict(); setExpanded(false); }} disabled={loading || !keyword || !content}
            className="px-8 h-12 text-xs uppercase tracking-widest font-bold text-white shadow-md transition-transform active:scale-95 disabled:opacity-40"
            style={{ background: 'var(--text-primary)' }}>
            {loading ? 'Evaluating...' : 'Predict Rank'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function RankingPrediction() {
  const [keyword, setKeyword] = useState('');
  const [content, setContent] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const saved = localStorage.getItem('qontint_keyword');
    if (saved) setKeyword(saved);
  }, []);

  const handlePredict = async () => {
    setLoading(true); setError(null);
    try { const data = await api.predictRanking(content, keyword); setPrediction(data); }
    catch (err) { setError(err.message); }
    finally { setLoading(false); }
  };

  return (
    <div className="min-h-[calc(100vh-80px)] w-full flex flex-col bg-white">
      {/* Utility Zone (Subordinate Input) */}
      <TopNavInput keyword={keyword} setKeyword={setKeyword} content={content} setContent={setContent} onPredict={handlePredict} loading={loading} />

      {error && <div className="p-4 mx-8 mt-8 bg-red-50 text-red-700 text-sm">{error}</div>}

      {!prediction && !loading && (
        <div className="flex-1 flex items-center justify-center text-center opacity-30 mt-20">
            <span className="text-8xl" style={{ fontFamily: 'var(--font-serif)' }}>◫</span>
        </div>
      )}

      {prediction && (
        <div className="flex-1 flex flex-col items-center animate-fade-in pb-20">
          
          {/* 1. PRIMARY ACTION ZONE (Top: Massive Banner) */}
          <div className="w-full py-24 flex flex-col items-center justify-center border-b" style={{ background: 'var(--bg-surface)', borderColor: 'var(--border-default)' }}>
            <p className="text-xs uppercase tracking-[0.3em] font-bold mb-8" style={{ color: 'var(--text-muted)' }}>Estimated Google Result Placement</p>
            <h1 className="text-[180px] leading-none mb-6" style={{ 
              fontFamily: 'var(--font-serif)', fontWeight: 300, 
              color: prediction.predicted_position <= 3 ? 'var(--accent-sage)' : prediction.predicted_position <= 10 ? 'var(--accent-teal)' : 'var(--text-primary)' 
            }}>
              #{prediction.predicted_position}
            </h1>
            <div className="flex gap-1">
               {Array.from({length: 10}).map((_, i) => (
                  <div key={i} className="w-8 h-2 transition-all opacity-20" 
                       style={{ background: i < prediction.predicted_position ? (prediction.predicted_position <= 3 ? 'var(--accent-sage)' : 'var(--text-primary)') : 'var(--border-light)', opacity: i < prediction.predicted_position ? 1 : 0.2 }} />
               ))}
            </div>
          </div>

          {/* 2. INSIGHT ZONE (Middle: Structured Metric Grid) */}
          <div className="w-full max-w-5xl mt-16 px-6">
            <h3 className="text-[10px] uppercase tracking-[0.2em] font-bold mb-8" style={{ color: 'var(--text-primary)' }}>Internal Variable Mapping</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 border" style={{ borderColor: 'var(--border-default)', background: 'var(--bg-primary)' }}>
              {[
                { l: 'Entity Novelty', v: prediction.features.entity_coverage },
                { l: 'Structure Completeness', v: prediction.features.relationship_completeness },
                { l: 'Semantic Weight', v: prediction.features.authority_score },
                { l: 'Composition Quality', v: prediction.features.content_quality },
              ].map((m, i) => (
                <div key={m.l} className="p-8 border-r last:border-r-0 border-b md:border-b-0" style={{ borderColor: 'var(--border-default)' }}>
                  <p className="text-[10px] font-bold uppercase tracking-widest mb-4 opacity-50">{m.l}</p>
                  <p className="text-2xl font-mono">{(m.v * 100).toFixed(0)}</p>
                </div>
              ))}
            </div>
          </div>

          {/* 3. UTILITY ZONE (Bottom: Context Data) */}
          <div className="w-full max-w-5xl mt-12 px-6">
             <div className="w-full p-6 border flex justify-between items-center bg-white" style={{ borderColor: 'var(--border-default)' }}>
                 <p className="text-sm font-semibold">Model Confidence</p>
                 <span className="px-3 py-1 bg-black text-white text-xs font-mono">{(prediction.confidence*100).toFixed(1)}%</span>
             </div>
          </div>
        </div>
      )}
    </div>
  );
}
