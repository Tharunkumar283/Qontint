import { useState, useEffect, useRef, useCallback } from 'react';
import api from '../services/api';

export default function GraphVisualization() {
  const [keyword, setKeyword] = useState('');
  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedNode, setSelectedNode] = useState(null);
  const canvasRef = useRef(null);
  const animFrameRef = useRef(null);
  const nodesRef = useRef([]);
  const edgesRef = useRef([]);
  const dragRef = useRef({ isDragging: false, node: null, offsetX: 0, offsetY: 0 });

  useEffect(() => {
    const saved = localStorage.getItem('qontint_keyword');
    if (saved) { setKeyword(saved); loadGraph(saved); }
  }, []);

  const loadGraph = async (kw) => {
    if (!kw?.trim()) return;
    setLoading(true);
    try { const data = await api.getGraph(kw.trim()); setGraphData(data); initializePositions(data); }
    catch (err) { console.error(err); }
    finally { setLoading(false); }
  };

  const initializePositions = (data) => {
    if (!data?.nodes?.length) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const cx = canvas.width / 2, cy = canvas.height / 2;

    nodesRef.current = data.nodes.map((n, i) => {
      const angle = (2 * Math.PI * i) / data.nodes.length;
      const radius = 140 + Math.random() * 200; // Spread out more for full screen
      return { ...n, x: cx + Math.cos(angle) * radius, y: cy + Math.sin(angle) * radius, vx: 0, vy: 0, radius: Math.max(8, n.size || 14) };
    });
    edgesRef.current = data.edges.map(e => ({
      sourceNode: nodesRef.current.find(n => n.id === e.source),
      targetNode: nodesRef.current.find(n => n.id === e.target),
      weight: e.weight
    })).filter(e => e.sourceNode && e.targetNode);
    startSimulation();
  };

  const startSimulation = () => {
    if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    const simulate = () => {
      const nodes = nodesRef.current, edges = edgesRef.current, canvas = canvasRef.current;
      if (!canvas || !nodes.length) return;
      
      // Auto-resize canvas visually
      const rect = canvas.parentElement.getBoundingClientRect();
      if(canvas.width !== rect.width || canvas.height !== rect.height) {
         canvas.width = rect.width;
         canvas.height = rect.height;
      }

      const ctx = canvas.getContext('2d'), cx = canvas.width / 2, cy = canvas.height / 2;

      for (let i = 0; i < nodes.length; i++) {
        const n = nodes[i];
        n.vx += (cx - n.x) * 0.0003; n.vy += (cy - n.y) * 0.0003;
        for (let j = i + 1; j < nodes.length; j++) {
          const o = nodes[j], dx = n.x - o.x, dy = n.y - o.y, dist = Math.sqrt(dx * dx + dy * dy) || 1;
          const force = 1200 / (dist * dist);
          n.vx += (dx / dist) * force; n.vy += (dy / dist) * force;
          o.vx -= (dx / dist) * force; o.vy -= (dy / dist) * force;
        }
      }
      for (const e of edges) {
        const dx = e.targetNode.x - e.sourceNode.x, dy = e.targetNode.y - e.sourceNode.y;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1, force = (dist - 160) * 0.002;
        e.sourceNode.vx += (dx / dist) * force; e.sourceNode.vy += (dy / dist) * force;
        e.targetNode.vx -= (dx / dist) * force; e.targetNode.vy -= (dy / dist) * force;
      }
      for (const n of nodes) {
        if (dragRef.current.isDragging && dragRef.current.node === n) continue;
        n.vx *= 0.85; n.vy *= 0.85; n.x += n.vx; n.y += n.vy;
        n.x = Math.max(30, Math.min(canvas.width - 30, n.x));
        n.y = Math.max(30, Math.min(canvas.height - 30, n.y));
      }

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (const e of edges) {
        ctx.beginPath(); ctx.moveTo(e.sourceNode.x, e.sourceNode.y); ctx.lineTo(e.targetNode.x, e.targetNode.y);
        ctx.strokeStyle = 'rgba(176, 137, 104, 0.1)'; ctx.lineWidth = Math.min(e.weight || 1, 3); ctx.stroke();
      }

      const colors = {
        METRIC: '#7c8f6e', CONCEPT: '#b08968', STRATEGY: '#6e8f8b',
        KEYWORD: '#c4a265', ORG: '#9c8578', PERSON: '#c47e7e',
      };
      
      for (const n of nodes) {
        const isSelected = selectedNode?.id === n.id;
        const color = colors[n.type] || '#9c9488';
        ctx.beginPath(); ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
        ctx.fillStyle = isSelected ? color : color + 'aa'; ctx.fill();
        
        if (isSelected) {
          ctx.strokeStyle = 'rgba(26,26,26,0.6)'; ctx.lineWidth = 1.5; ctx.stroke();
          ctx.beginPath(); ctx.arc(n.x, n.y, n.radius + 8, 0, Math.PI * 2);
          ctx.strokeStyle = color + '55'; ctx.lineWidth = 4; ctx.stroke();
        }
        
        ctx.fillStyle = isSelected ? '#000' : '#4a4a4a'; 
        ctx.font = isSelected ? `bold ${Math.max(11, n.radius * 0.9)}px Inter` : `${Math.max(10, n.radius * 0.8)}px Inter`; 
        ctx.textAlign = 'center';
        ctx.fillText(n.label.length > 20 ? n.label.substring(0, 20) + '…' : n.label, n.x, n.y + n.radius + 16);
      }
      animFrameRef.current = requestAnimationFrame(simulate);
    };
    simulate();
  };

  useEffect(() => { return () => { if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current); }; }, [selectedNode]);

  const handleCanvasClick = useCallback((e) => {
    const canvas = canvasRef.current; if (!canvas) return;
    const rect = canvas.getBoundingClientRect(), x = e.clientX - rect.left, y = e.clientY - rect.top;
    setSelectedNode(nodesRef.current.find(n => Math.sqrt((n.x - x) ** 2 + (n.y - y) ** 2) < n.radius + 6) || null);
  }, []);

  const handleMouseDown = useCallback((e) => {
    const canvas = canvasRef.current; if (!canvas) return;
    const rect = canvas.getBoundingClientRect(), x = e.clientX - rect.left, y = e.clientY - rect.top;
    const node = nodesRef.current.find(n => Math.sqrt((n.x - x) ** 2 + (n.y - y) ** 2) < n.radius + 6);
    if (node) dragRef.current = { isDragging: true, node, offsetX: node.x - x, offsetY: node.y - y };
  }, []);
  
  const handleMouseMove = useCallback((e) => {
    if (!dragRef.current.isDragging) return;
    const canvas = canvasRef.current; if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    dragRef.current.node.x = e.clientX - rect.left + dragRef.current.offsetX;
    dragRef.current.node.y = e.clientY - rect.top + dragRef.current.offsetY;
  }, []);
  
  const handleMouseUp = useCallback(() => { dragRef.current = { isDragging: false, node: null, offsetX: 0, offsetY: 0 }; }, []);

  return (
    <div className="relative w-full h-[calc(100vh-80px)] overflow-hidden" style={{ background: 'var(--bg-primary)' }}>
      
      {/* 2. DATA ZONE (Full Bleed Canvas) */}
      <canvas ref={canvasRef} 
        onClick={handleCanvasClick} onMouseDown={handleMouseDown} onMouseMove={handleMouseMove} onMouseUp={handleMouseUp} onMouseLeave={handleMouseUp}
        className="absolute inset-0 w-full h-full cursor-grab active:cursor-grabbing outline-none z-0" />

      {/* 1. INPUT ZONE (Floating Overlay Top-Left) */}
      <div className="absolute top-8 left-8 z-10 flex flex-col gap-4 p-6 rounded-md shadow-xl animate-fade-in" 
        style={{ background: 'rgba(255,255,255,0.85)', backdropFilter: 'blur(12px)', border: '1px solid rgba(0,0,0,0.05)', maxWidth: '340px' }}>
        <div>
          <label className="text-[10px] uppercase tracking-[0.2em] font-bold text-gray-500 mb-1 block">Data Mapping Tool</label>
          <h2 className="text-xl font-light" style={{ fontFamily: 'var(--font-serif)' }}>Graph Generation</h2>
        </div>
        <input type="text" value={keyword} onChange={e => setKeyword(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && loadGraph(keyword)} placeholder="Analyze keyword context…"
            className="w-full px-4 h-11 text-xs border-b-2 focus:outline-none transition-colors"
            style={{ background: 'var(--bg-surface)', borderColor: 'transparent' }}
            onFocus={e => e.target.style.borderColor = 'var(--accent-copper)'} onBlur={e => e.target.style.borderColor = 'transparent'} />
        <button onClick={() => loadGraph(keyword)} disabled={loading || !keyword.trim()}
            className="w-full h-11 text-[11px] uppercase tracking-widest font-bold bg-black text-white disabled:opacity-40 hover:bg-gray-800 transition-colors">
            {loading ? 'Mapping Engine...' : 'Initialize Map'}
        </button>
      </div>

      {/* 3. INSIGHT ZONE (Floating Overlay Bottom-Right / Right) */}
      {graphData && (
        <div className="absolute top-8 right-8 z-10 flex flex-col gap-6 w-80 h-[calc(100%-64px)] overflow-y-auto pb-8 animate-fade-in" style={{ pointerEvents: 'none' }}>
           
           {/* General Network Statistics */}
           <div className="p-6 rounded-md shadow-xl" style={{ background: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(12px)', pointerEvents: 'auto' }}>
              <p className="text-[10px] uppercase tracking-[0.2em] font-bold text-gray-500 mb-4 pb-2 border-b">Topography</p>
              <div className="flex flex-col gap-4 text-xs">
                <div className="flex justify-between font-semibold"><span className="text-gray-500">Entities</span><span>{graphData.stats.total_nodes}</span></div>
                <div className="flex justify-between font-semibold"><span className="text-gray-500">Connections</span><span>{graphData.stats.total_edges}</span></div>
                <div className="flex justify-between font-semibold"><span className="text-gray-500">Authority Range</span><span style={{color:'var(--accent-sage)'}}>{(graphData.stats.avg_authority * 100).toFixed(0)}%</span></div>
              </div>
           </div>

           {/* Focused Node (Conditional) */}
           {selectedNode && (
             <div className="p-6 rounded-md shadow-xl border-l-4" style={{ background: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(12px)', borderColor: 'var(--accent-copper)', pointerEvents: 'auto' }}>
                <p className="text-[10px] uppercase tracking-[0.2em] font-bold text-gray-500 mb-2">Entity Focus</p>
                <h3 className="text-2xl font-light mb-4" style={{ fontFamily: 'var(--font-serif)' }}>{selectedNode.label}</h3>
                <div className="flex justify-between items-center text-xs">
                   <span className="px-2 py-1 bg-gray-100 text-gray-600 font-mono font-bold uppercase tracking-widest text-[9px] rounded-sm">{selectedNode.type}</span>
                   <span className="font-mono font-bold" style={{color:'var(--accent-copper)'}}>{(selectedNode.authority * 100).toFixed(1)}% Weight</span>
                </div>
             </div>
           )}

           {/* Top Nodes Feed */}
           <div className="flex-1 min-h-0 flex flex-col p-6 rounded-md shadow-xl" style={{ background: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(12px)', pointerEvents: 'auto' }}>
              <p className="text-[10px] uppercase tracking-[0.2em] font-bold text-gray-500 mb-4 pb-2 border-b flex-shrink-0">Dominant Nodes</p>
              <div className="flex-1 overflow-y-auto pr-2 mt-2">
                {graphData.stats.top_entities.map((e, i) => (
                  <div key={i} className="flex items-center gap-3 py-2 border-b border-gray-100 last:border-0 hover:bg-gray-50 transition-colors">
                    <span className="text-[9px] font-bold text-gray-300 w-4">0{i+1}</span>
                    <span className="text-xs font-semibold text-gray-800 flex-1 truncate">{e.text}</span>
                    <span className="text-[10px] font-mono font-bold text-gray-500">{(e.authority_score * 100).toFixed(0)}</span>
                  </div>
                ))}
              </div>
           </div>
        </div>
      )}

      {/* Floating Legend Bottom Left */}
      {graphData && (
        <div className="absolute bottom-8 left-8 z-10 flex gap-4 px-5 py-3 rounded-md shadow-lg" style={{ background: 'rgba(255,255,255,0.9)', backdropFilter: 'blur(8px)', pointerEvents: 'none' }}>
            {[
              { l: 'Keyword', c: '#c4a265' }, { l: 'Metric', c: '#7c8f6e' }, { l: 'Concept', c: '#b08968' }, { l: 'Strategy', c: '#6e8f8b' }
            ].map(i => (
              <div key={i.l} className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full" style={{ background: i.c }} />
                <span className="text-[9px] uppercase tracking-widest font-bold text-gray-500">{i.l}</span>
              </div>
            ))}
        </div>
      )}
    </div>
  );
}
