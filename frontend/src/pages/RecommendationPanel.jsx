import { useState, useEffect } from 'react';
import api from '../services/api';

function FeedInput({ keyword, setKeyword, content, setContent, onAnalyze, loading }) {
  return (
    <div className="w-full md:w-80 flex-shrink-0 flex flex-col p-8 border-r h-full bg-white z-10 relative shadow-sm" style={{ borderColor: 'var(--border-default)' }}>
      <h2 className="text-xl mb-8 font-light" style={{ fontFamily: 'var(--font-serif)', color: 'var(--text-primary)' }}>Feed Configuration</h2>
      <div className="flex flex-col gap-6 flex-1">
        <div>
          <label className="text-[10px] uppercase tracking-widest font-bold text-gray-500 mb-3 block">Keyword Target</label>
          <input type="text" value={keyword} onChange={e => setKeyword(e.target.value)}
            className="w-full border-b pb-2 text-sm focus:outline-none transition-colors"
            style={{ borderColor: 'var(--border-default)', background: 'transparent' }}
            onFocus={e => e.target.style.borderColor = 'var(--accent-copper)'}
            onBlur={e => e.target.style.borderColor = 'var(--border-default)'} />
        </div>
        <div className="flex-1 flex flex-col">
          <label className="text-[10px] uppercase tracking-widest font-bold text-gray-500 mb-3 block">Content Body</label>
          <textarea value={content} onChange={e => setContent(e.target.value)}
            className="w-full flex-1 border resize-none p-3 text-sm focus:outline-none transition-colors bg-gray-50"
            style={{ borderColor: 'var(--border-light)' }}
            onFocus={e => e.target.style.borderColor = 'var(--accent-copper)'}
            onBlur={e => e.target.style.borderColor = 'var(--border-light)'} />
        </div>
      </div>
      <button onClick={onAnalyze} disabled={loading || !keyword || !content}
        className="w-full mt-6 h-12 text-xs uppercase tracking-widest font-bold bg-black text-white hover:bg-gray-800 transition-colors disabled:opacity-40">
        {loading ? 'Scanning...' : 'Generate Feed'}
      </button>
    </div>
  );
}

export default function RecommendationPanel() {
  const [keyword, setKeyword] = useState('');
  const [content, setContent] = useState('');
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const saved = localStorage.getItem('qontint_keyword');
    if (saved) setKeyword(saved);
  }, []);

  const handleRecommend = async () => {
    setLoading(true); setError(null);
    try { const data = await api.getRecommendations(content, keyword); setRecommendations(data); }
    catch (err) { setError(err.message); }
    finally { setLoading(false); }
  };

  return (
    <div className="flex flex-col md:flex-row h-[calc(100vh-80px)] w-full overflow-hidden" style={{ background: 'var(--bg-primary)' }}>
      
      {/* 1. INPUT ZONE (Sticky Left Sidebar) */}
      <FeedInput keyword={keyword} setKeyword={setKeyword} content={content} setContent={setContent} onAnalyze={handleRecommend} loading={loading} />

      {/* 2. PRIMARY ACTION ZONE (The Vertical Feed) */}
      <div className="flex-1 h-full overflow-y-auto relative">
        {!recommendations && !loading && (
          <div className="absolute inset-0 flex flex-col items-center justify-center opacity-30">
             <span className="text-6xl mb-4" style={{ fontFamily: 'var(--font-serif)' }}>☵</span>
             <p className="text-sm font-medium tracking-wide">Generate to populate discovery feed.</p>
          </div>
        )}

        {error && <div className="p-4 m-8 bg-red-100 text-red-800 text-sm">{error}</div>}

        {recommendations && (
          <div className="w-full max-w-4xl mx-auto py-12 animate-fade-in flex flex-col">
            
            {/* Feed Header */}
            <div className="px-8 pb-8 border-b" style={{ borderColor: 'var(--border-default)' }}>
              <div className="flex items-end justify-between">
                <div>
                  <p className="text-[10px] uppercase tracking-[0.2em] font-bold text-gray-400 mb-2">Discovery Feed</p>
                  <h3 className="text-3xl" style={{ fontFamily: 'var(--font-serif)' }}>Actionable Enhancements</h3>
                </div>
                <div className="text-right">
                  <p className="text-[10px] uppercase tracking-widest font-bold text-gray-400 mb-1">Growth Index</p>
                  <p className="text-xl font-mono text-green-700">+{(recommendations.potential_novelty_gain * 100).toFixed(1)}%</p>
                </div>
              </div>
            </div>

            {/* The Feed */}
            <div className="flex flex-col">
              {recommendations.recommendations?.map((rec, i) => (
                <div key={i} className="group w-full flex flex-col md:flex-row items-start md:items-center justify-between p-8 border-b hover:bg-white transition-colors"
                  style={{ borderColor: 'var(--border-light)' }}>
                  
                  {/* Entity Information */}
                  <div className="flex-1 pr-12 min-w-0">
                    <div className="flex items-center gap-3 mb-2">
                       <span className="text-[10px] uppercase tracking-widest font-bold px-2 py-0.5 bg-gray-100 text-gray-500 rounded-sm">
                         {rec.entity_type}
                       </span>
                       <span className="text-[10px] font-mono text-gray-400"><span style={{color:'var(--accent-copper)'}}>{(rec.authority_score*100).toFixed(0)}</span> Auth</span>
                    </div>
                    <h4 className="text-xl font-medium truncate mb-2" style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-serif)' }}>
                      {rec.entity}
                    </h4>
                    <p className="text-sm leading-relaxed text-gray-600 truncate group-hover:whitespace-normal group-hover:overflow-visible transition-all">
                      {rec.suggestion}
                    </p>
                  </div>

                  {/* Feed Action */}
                  <div className="mt-4 md:mt-0 flex-shrink-0">
                    <button className="px-6 h-10 border border-gray-300 rounded-sm text-[11px] uppercase tracking-widest font-bold text-gray-700 hover:bg-black hover:text-white hover:border-black transition-all"
                      onClick={() => setContent(prev => prev + '\n' + `${rec.entity}: `)}>
                      Inject
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
