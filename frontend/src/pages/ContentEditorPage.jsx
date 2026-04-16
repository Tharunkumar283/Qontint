import { useState, useEffect } from 'react';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Placeholder from '@tiptap/extension-placeholder';
import api from '../services/api';

function ToolbarButton({ label, isActive, onClick }) {
  return (
    <button
      onClick={onClick}
      className="w-10 h-10 flex items-center justify-center text-xs font-bold uppercase transition-all"
      style={{
        background: isActive ? 'var(--text-primary)' : 'transparent',
        color: isActive ? '#fff' : 'var(--text-secondary)',
      }}
      onMouseEnter={e => { if(!isActive) e.currentTarget.style.color = 'var(--text-primary)' }}
      onMouseLeave={e => { if(!isActive) e.currentTarget.style.color = 'var(--text-secondary)' }}
    >
      {label}
    </button>
  );
}

export default function ContentEditorPage() {
  const [keyword, setKeyword] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('qontint_keyword');
    if (saved) setKeyword(saved);
  }, []);

  const editor = useEditor({
    extensions: [
      StarterKit,
      Placeholder.configure({ placeholder: 'Start drafting your content here...' }),
    ],
    content: '',
    editorProps: { attributes: { class: 'prose prose-lg max-w-[800px] mx-auto focus:outline-none min-h-[500px] pb-32' } },
  });

  const handleGenerate = async () => {
    if (!keyword.trim()) return;
    setGenerating(true);
    try {
      const data = await api.generateContent(keyword);
      if (editor && data.content) editor.commands.setContent(data.content.replace(/\n/g, '<br>'));
    } catch (err) { console.error(err); }
    finally { setGenerating(false); }
  };

  const handleAnalyze = async () => {
    if (!editor || !keyword.trim()) return;
    const text = editor.getText();
    if (!text.trim()) return;
    setAnalyzing(true);
    try { const data = await api.analyzeContent(text, keyword); setAnalysis(data); }
    catch (err) { console.error(err); }
    finally { setAnalyzing(false); }
  };

  const wordCount = editor ? editor.getText().split(/\s+/).filter(Boolean).length : 0;

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] w-full animate-fade-in bg-white">
      
      {/* 1. UTILITY ZONE (Sticky Top Toolbar) */}
      <div className="flex items-center justify-between px-6 border-b h-16 flex-shrink-0 z-20 sticky top-0 bg-white" style={{ borderColor: 'var(--border-default)' }}>
        <div className="flex items-center gap-6">
          {/* Subtle Input */}
          <input type="text" value={keyword} onChange={e => setKeyword(e.target.value)} placeholder="Attach Target Keyword..." 
            className="w-64 h-10 px-4 text-xs font-semibold focus:outline-none border-b-2 transition-colors"
            style={{ borderColor: 'transparent', background: 'var(--bg-primary)' }}
            onFocus={e => e.target.style.borderColor = 'var(--text-primary)'} onBlur={e => e.target.style.borderColor = 'transparent'} />
          
          <div className="w-px h-6 bg-gray-200" />
          
          {/* Format Actions */}
          {editor && (
            <div className="flex gap-1" style={{ background: 'var(--bg-primary)' }}>
              <ToolbarButton label="B" isActive={editor.isActive('bold')} onClick={() => editor.chain().focus().toggleBold().run()} />
              <ToolbarButton label="I" isActive={editor.isActive('italic')} onClick={() => editor.chain().focus().toggleItalic().run()} />
              <div className="w-px h-10 bg-gray-200" />
              <ToolbarButton label="H1" isActive={editor.isActive('heading', { level: 1 })} onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()} />
              <ToolbarButton label="H2" isActive={editor.isActive('heading', { level: 2 })} onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()} />
              <ToolbarButton label="•" isActive={editor.isActive('bulletList')} onClick={() => editor.chain().focus().toggleBulletList().run()} />
            </div>
          )}
        </div>
        
        <div className="flex items-center gap-4">
          <span className="text-[10px] font-mono font-medium text-gray-400 mr-4">{wordCount} words authored</span>
          <button onClick={handleGenerate} disabled={generating || !keyword.trim()}
            className="px-6 h-10 text-[11px] uppercase tracking-widest font-bold transition-all disabled:opacity-40"
            style={{ color: 'var(--text-primary)' }}
            onMouseEnter={e => e.currentTarget.style.textDecoration = 'underline'}
            onMouseLeave={e => e.currentTarget.style.textDecoration = 'none'}>
            {generating ? 'Drafting...' : 'Autopilot'}
          </button>
          <button onClick={handleAnalyze} disabled={analyzing || !keyword.trim() || wordCount === 0}
            className="px-8 h-10 text-[11px] uppercase tracking-widest font-bold bg-black text-white transition-all disabled:opacity-40">
            {analyzing ? 'Evaluating...' : 'Score Document'}
          </button>
        </div>
      </div>

      {/* Split Pane Content */}
      <div className="flex flex-1 overflow-hidden">
        
        {/* 2. INPUT ZONE (Editor Canvas 70%) */}
        <div className="w-[70%] h-full overflow-y-auto pt-16">
          <EditorContent editor={editor} />
        </div>

        {/* 3. INSIGHT ZONE (Live Scoring 30%) */}
        <div className="w-[30%] h-full flex flex-col border-l overflow-y-auto" style={{ borderColor: 'var(--border-default)', background: 'var(--bg-primary)' }}>
            {!analysis ? (
              <div className="flex-1 flex flex-col items-center justify-center p-12 text-center">
                <span className="text-4xl text-gray-300 mb-6" style={{ fontFamily: 'var(--font-serif)' }}>✎</span>
                <p className="text-xs uppercase tracking-widest font-bold text-gray-400">Analysis Pending</p>
                <p className="text-sm font-medium text-gray-500 mt-2">Write content and click “Score Document” to project SERP positioning live.</p>
              </div>
            ) : (
              <div className="flex flex-col h-full">
                
                {/* Fixed Outcome Header */}
                <div className="p-8 border-b bg-white relative overflow-hidden" style={{ borderColor: 'var(--border-default)' }}>
                  <div className="absolute top-0 right-0 w-32 h-32 rounded-full blur-2xl opacity-10 -mr-10 -mt-10 pointer-events-none" 
                    style={{ background: analysis.predicted_rank <= 5 ? 'var(--status-pass)' : 'var(--status-fail)' }} />
                  <p className="text-[10px] uppercase tracking-[0.2em] font-bold text-gray-500 mb-4 relative z-10">Simulation Output</p>
                  <div className="flex items-end justify-between relative z-10">
                    <span className="text-7xl font-light" style={{ fontFamily: 'var(--font-serif)', lineHeight: 0.8 }}>#{analysis.predicted_rank}</span>
                    <span className="text-xs font-mono font-bold px-2 py-0.5" style={{
                      background: analysis.pass_fail === 'PASS' ? 'rgba(124,143,110,0.1)' : 'rgba(196,126,126,0.1)',
                      color: analysis.pass_fail === 'PASS' ? 'var(--status-pass)' : 'var(--status-fail)'
                    }}>{analysis.pass_fail}</span>
                  </div>
                </div>

                {/* Score Breakdown List */}
                <div className="flex-1 p-8 overflow-y-auto">
                  <p className="text-[10px] uppercase tracking-[0.2em] font-bold text-gray-500 mb-6">Component Indices</p>
                  <div className="flex flex-col gap-6">
                    {[
                      { l: 'Novelty Factor', v: analysis.novelty_score, c: 'var(--accent-copper)' },
                      { l: 'Entity Coverage', v: analysis.entity_coverage, c: 'var(--accent-sage)' },
                      { l: 'Alignment Match', v: analysis.intent_alignment, c: 'var(--accent-teal)' }
                    ].map(s => (
                      <div key={s.l} className="group">
                        <div className="flex justify-between items-baseline mb-2 text-xs">
                          <span className="font-semibold text-gray-700">{s.l}</span>
                          <span className="font-mono font-bold" style={{ color: s.c }}>{(s.v * 100).toFixed(0)}</span>
                        </div>
                        <div className="h-0.5 bg-gray-200 overflow-hidden">
                          <div className="h-0.5 transition-all duration-700" style={{ background: s.c, width: `${s.v * 100}%` }} />
                        </div>
                      </div>
                    ))}
                  </div>

                  {analysis.missing_entities?.length > 0 && (
                    <div className="mt-12">
                      <p className="text-[10px] uppercase tracking-[0.2em] font-bold text-gray-500 mb-6">Target Gaps</p>
                      <div className="flex flex-col gap-1 border-l-2 pl-4" style={{ borderColor: 'var(--accent-gold)' }}>
                        {analysis.missing_entities.slice(0, 6).map((e, i) => (
                          <div key={i} className="flex justify-between items-center py-1.5 text-sm">
                            <span className="text-gray-800 font-medium">{e.text}</span>
                            <button className="text-[9px] font-bold uppercase tracking-widest text-opacity-50 hover:text-opacity-100 transition-colors" 
                              style={{ color: 'var(--text-primary)' }} onClick={() => editor.chain().focus().insertContent(e.text).run()}>
                              Insert
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
        </div>
      </div>
    </div>
  );
}
