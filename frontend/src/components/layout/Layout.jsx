import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { useState } from 'react';

const navItems = [
  { path: '/', label: 'Input', icon: '⌕' },
  { path: '/analyze', label: 'Analysis', icon: '◉' },
  { path: '/editor', label: 'Editor', icon: '✎' },
  { path: '/graph', label: 'Graph', icon: '⬡' },
  { path: '/predict', label: 'Predict', icon: '◈' },
  { path: '/recommend', label: 'Suggest', icon: '★' },
];

export default function Layout() {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();

  return (
    <div className="flex h-screen overflow-hidden" style={{ background: 'var(--bg-primary)' }}>
      {/* ─── Sidebar ───────────────────────────────── */}
      <aside
        className="flex flex-col border-r transition-all duration-300 flex-shrink-0"
        style={{
          width: collapsed ? '60px' : '220px',
          background: 'var(--bg-sidebar)',
          borderColor: 'var(--border-default)',
        }}
      >
        {/* Logo */}
        <div
          className="flex items-center gap-3 h-20 border-b"
          style={{
            borderColor: 'var(--border-default)',
            padding: collapsed ? '0 14px' : '0 24px',
          }}
        >
          <div
            className="w-8 h-8 rounded-sm flex items-center justify-center font-bold text-sm flex-shrink-0"
            style={{
              background: 'var(--accent-copper)',
              color: '#fff',
              fontFamily: 'var(--font-serif)',
              fontSize: '16px',
              letterSpacing: '0.02em',
            }}
          >
            Q
          </div>
          {!collapsed && (
            <div className="animate-fade-in">
              <h1
                className="text-base tracking-tight"
                style={{
                  color: 'var(--text-primary)',
                  fontFamily: 'var(--font-serif)',
                  fontWeight: 600,
                  letterSpacing: '0.01em',
                }}
              >
                Qontint
              </h1>
              <p
                className="text-[10px] uppercase tracking-widest"
                style={{ color: 'var(--text-muted)', fontWeight: 500 }}
              >
                Authority OS
              </p>
            </div>
          )}
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-6 overflow-y-auto" style={{ padding: collapsed ? '24px 8px' : '24px 12px' }}>
          <div className="space-y-1">
            {!collapsed && (
              <p
                className="text-[9px] uppercase tracking-[0.2em] mb-4"
                style={{ color: 'var(--text-muted)', paddingLeft: '12px', fontWeight: 600 }}
              >
                Navigation
              </p>
            )}
            {navItems.map(item => {
              const isActive = location.pathname === item.path;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className="flex items-center gap-3 rounded-sm transition-all duration-200"
                  style={{
                    padding: collapsed ? '10px 0' : '9px 12px',
                    justifyContent: collapsed ? 'center' : 'flex-start',
                    background: isActive ? 'var(--bg-elevated)' : 'transparent',
                    color: isActive ? 'var(--accent-copper)' : 'var(--text-secondary)',
                    fontWeight: isActive ? 600 : 400,
                    fontSize: '13px',
                    letterSpacing: '0.02em',
                  }}
                  onMouseEnter={e => {
                    if (!isActive) {
                      e.currentTarget.style.background = 'var(--bg-hover)';
                      e.currentTarget.style.color = 'var(--text-primary)';
                    }
                  }}
                  onMouseLeave={e => {
                    if (!isActive) {
                      e.currentTarget.style.background = 'transparent';
                      e.currentTarget.style.color = 'var(--text-secondary)';
                    }
                  }}
                >
                  <span className="text-sm flex-shrink-0 w-5 text-center opacity-60">{item.icon}</span>
                  {!collapsed && <span>{item.label}</span>}
                </NavLink>
              );
            })}
          </div>
        </nav>

        {/* Bottom */}
        <div className="border-t" style={{ borderColor: 'var(--border-default)' }}>
          {!collapsed && (
            <div className="px-5 py-4">
              <div className="flex items-center gap-1.5 text-[10px] uppercase tracking-widest" style={{ color: 'var(--text-muted)' }}>
                <span className="w-1.5 h-1.5 rounded-full" style={{ background: 'var(--accent-sage)' }} />
                Active
              </div>
            </div>
          )}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="flex items-center justify-center w-full h-11 transition-colors duration-200 cursor-pointer border-t"
            style={{
              borderColor: 'var(--border-default)',
              color: 'var(--text-muted)',
              fontSize: '12px',
            }}
            onMouseEnter={e => e.currentTarget.style.background = 'var(--bg-hover)'}
            onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
          >
            {collapsed ? '→' : '←'}
          </button>
        </div>
      </aside>

      {/* ─── Main Content ──────────────────────────── */}
      <main className="flex-1 overflow-y-auto">
        {/* Header Bar — thin, minimal */}
        <header
          className="sticky top-0 z-10 flex items-center justify-between h-14 px-8 border-b"
          style={{
            background: 'rgba(247, 244, 239, 0.92)',
            backdropFilter: 'blur(8px)',
            borderColor: 'var(--border-default)',
          }}
        >
          <div className="flex items-center gap-4">
            <h2
              className="text-sm"
              style={{
                color: 'var(--text-primary)',
                fontFamily: 'var(--font-serif)',
                fontWeight: 600,
                fontSize: '16px',
              }}
            >
              {navItems.find(n => n.path === location.pathname)?.label || 'Qontint'}
            </h2>
            <span
              className="text-[10px] uppercase tracking-[0.15em] px-2.5 py-1 rounded-sm"
              style={{
                background: 'var(--bg-elevated)',
                color: 'var(--accent-copper)',
                fontWeight: 600,
                border: '1px solid var(--border-default)',
              }}
            >
              SaaS
            </span>
          </div>
          <div className="flex items-center gap-2 text-[11px]" style={{ color: 'var(--text-muted)' }}>
            <span className="w-1.5 h-1.5 rounded-full" style={{ background: 'var(--accent-sage)' }} />
            <span className="tracking-wide">System Active</span>
          </div>
        </header>

        {/* Page Content */}
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
