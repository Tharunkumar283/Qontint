import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const VERTICALS = [
  { id: 'saas', label: 'SaaS', active: true },
  { id: 'mortgage', label: 'Mortgage', active: false },
  { id: 'healthcare', label: 'Healthcare', active: false },
  { id: 'finance', label: 'Finance', active: false },
];

const RECENT_KEYWORDS = [
  'saas pricing strategies',
  'product-led growth',
  'customer retention saas',
];

export default function KeywordInput() {
  const [keyword, setKeyword] = useState('');
  const [vertical, setVertical] = useState('saas');
  const [loading, setLoading] = useState(false);
  const [serpData, setSerpData] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleCollect = async (kw) => {
    const target = kw || keyword;
    if (!target.trim()) return;
    setLoading(true); setError(null);
    try {
      const data = await api.collectSerp(target.trim(), vertical);
      setSerpData(data);
      localStorage.setItem('qontint_keyword', target.trim());
      localStorage.setItem('qontint_vertical', vertical);
    } catch (err) { setError(err.message); }
    finally { setLoading(false); }
  };

  return (
    <div className="min-h-[calc(100vh-100px)] flex flex-col justify-center items-center py-20 px-4 animate-fade-in">
      
      {/* 1. Primary Action Zone (Command Center) */}
      <div className="w-full max-w-3xl flex flex-col items-center">
        <h1 className="text-center mb-10 font-light" style={{ fontFamily: 'var(--font-serif)', fontSize: '64px', color: 'var(--text-primary)', lineHeight: 1.1, letterSpacing: '-0.02em' }}>
          Evaluate Content Potential
        </h1>
        
        <div className="w-full flex shadow-xl rounded-md relative z-10" style={{ background: 'var(--bg-surface)' }}>
          <div className="flex-1 relative flex items-center">
            <span className="absolute left-6 text-2xl opacity-40">⌕</span>
            <input
              type="text" value={keyword} onChange={e => setKeyword(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleCollect()}
              placeholder="Enter target keyword to analyze..."
              className="w-full h-20 pl-16 pr-6 text-xl bg-transparent focus:outline-none transition-all placeholder:font-light"
              style={{ color: 'var(--text-primary)' }}
            />
          </div>
          <button
            onClick={() => handleCollect()} disabled={loading || !keyword.trim()}
            className="h-20 px-12 rounded-r-md text-[13px] uppercase tracking-[0.15em] font-bold transition-all disabled:opacity-40 whitespace-nowrap"
            style={{ background: 'var(--text-primary)', color: '#fff' }}
            onMouseEnter={e => { if(!loading) e.currentTarget.style.background = '#000'; }}
            onMouseLeave={e => { if(!loading) e.currentTarget.style.background = 'var(--text-primary)'; }}
          >
            {loading ? 'Evaluating...' : 'Analyze Keyword'}
          </button>
        </div>
      </div>

      {/* 2. Utility Zone (Subordinate Layer Below) */}
      <div className="w-full max-w-2xl mt-12 flex flex-col items-center gap-6">
        {/* Industry Control */}
        <div className="flex items-center gap-4 border-t border-b py-3 w-full justify-center" style={{ borderColor: 'var(--border-default)' }}>
          <span className="text-[10px] uppercase tracking-[0.2em] font-bold" style={{ color: 'var(--text-muted)' }}>Sector:</span>
          {VERTICALS.map(v => (
            <button key={v.id} onClick={() => v.active && setVertical(v.id)} disabled={!v.active}
              className="text-[11px] font-semibold tracking-wider transition-colors"
              style={{ color: vertical === v.id ? 'var(--text-primary)' : 'var(--text-muted)', opacity: v.active ? 1 : 0.4 }}>
              {v.label}
            </button>
          ))}
        </div>

        {/* Quick Suggestion Chips */}
        <div className="flex gap-3 mt-4">
          {RECENT_KEYWORDS.map(kw => (
            <button key={kw} onClick={() => { setKeyword(kw); handleCollect(kw); }}
              className="px-4 py-2 rounded-full text-[11px] transition-all cursor-pointer shadow-sm"
              style={{ background: 'var(--bg-surface)', color: 'var(--text-secondary)' }}
              onMouseEnter={e => { e.currentTarget.style.background = 'var(--text-primary)'; e.currentTarget.style.color = '#fff'; }}
              onMouseLeave={e => { e.currentTarget.style.background = 'var(--bg-surface)'; e.currentTarget.style.color = 'var(--text-secondary)'; }}>
              {kw}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="mt-8 p-4 rounded-md mx-auto" style={{ background: 'rgba(196,126,126,0.1)', color: 'var(--accent-rose)' }}>
          {error}
        </div>
      )}

      {/* Results Portal Display */}
      {serpData && (
        <div className="w-full max-w-5xl mt-24 animate-fade-in">
          <div className="flex items-end justify-between border-b pb-6 mb-8" style={{ borderColor: 'var(--border-default)' }}>
            <div>
              <h3 className="text-3xl" style={{ fontFamily: 'var(--font-serif)', color: 'var(--text-primary)' }}>SERP Engine Validation</h3>
              <p className="text-[11px] uppercase tracking-widest font-mono mt-2" style={{ color: 'var(--text-muted)' }}>Top {serpData.total_results} Competitors Indexed</p>
            </div>
            <div className="flex gap-4">
              <button onClick={() => navigate('/editor')} className="px-6 h-12 text-[11px] uppercase tracking-widest font-bold transition-all border rounded-md"
                style={{ borderColor: 'var(--border-default)', color: 'var(--text-secondary)' }}
                onMouseEnter={e => e.currentTarget.style.background = 'var(--bg-elevated)'}
                onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>Skip to Editor</button>
              <button onClick={() => navigate('/analyze')} className="px-8 h-12 text-[11px] uppercase tracking-widest font-bold rounded-md shadow-md transition-all"
                style={{ background: 'var(--accent-copper)', color: '#fff' }}
                onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-2px)'}
                onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}>View Deep Analysis</button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {serpData.results?.slice(0, 10).map((r, i) => (
              <div key={i} className="flex gap-4 p-4 rounded-md" style={{ background: 'var(--bg-elevated)' }}>
                <span className="w-6 text-[10px] font-mono font-bold pt-1 opacity-50">0{r.position}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold truncate mb-1" style={{ color: 'var(--text-primary)' }}>{r.title}</p>
                  <p className="text-[10px] font-mono truncate" style={{ color: 'var(--text-muted)' }}>{r.url}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
