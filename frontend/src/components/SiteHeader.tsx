import { Link } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { Logo } from "./Logo";
import { getStoredUser, clearToken, clearStoredUser } from "@/lib/api";
import type { User } from "@/lib/types";

const nav = [
  { to: "/", label: "Home" },
  { to: "/analyze", label: "Analyze" },
  { to: "/youtube", label: "YouTube" },
  { to: "/dashboard", label: "Dashboard" },
  { to: "/graph", label: "Graph" },
  { to: "/pricing", label: "Pricing" },
] as const;

export function SiteHeader() {
  const [user, setUser] = useState<User | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    setUser(getStoredUser());
    const onStorage = () => setUser(getStoredUser());
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  const handleLogout = () => {
    clearToken();
    clearStoredUser();
    setUser(null);
    window.location.href = "/";
  };

  return (
    <header className="sticky top-0 z-40 border-b border-border/60 bg-background/80 backdrop-blur-xl">
      <div className="container mx-auto flex h-16 items-center justify-between px-6 lg:px-8">
        <Link to="/" className="transition-opacity hover:opacity-80">
          <Logo />
        </Link>

        {/* Desktop nav */}
        <nav className="hidden items-center gap-1 md:flex">
          {nav.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              activeOptions={{ exact: item.to === "/" }}
              activeProps={{ className: "text-foreground bg-surface-raised/60" }}
              inactiveProps={{ className: "text-muted-foreground hover:text-foreground hover:bg-surface-raised/40" }}
              className="rounded-md px-3 py-1.5 text-sm font-medium transition-colors"
            >
              {item.to === "/youtube" ? (
                <span className="flex items-center gap-1">
                  <span className="text-red-400">▶</span>
                  {item.label}
                </span>
              ) : (
                item.label
              )}
            </Link>
          ))}
        </nav>

        {/* Auth controls */}
        <div className="flex items-center gap-2">
          {user ? (
            <div className="relative">
              <button
                id="user-menu-btn"
                onClick={() => setMenuOpen((v) => !v)}
                className="flex items-center gap-2 rounded-md border border-border-strong px-3 py-1.5 text-sm font-medium transition-colors hover:bg-surface-raised/50"
              >
                <span className="flex h-6 w-6 items-center justify-center rounded-full bg-accent/20 font-display text-xs font-bold text-accent">
                  {user.name?.[0]?.toUpperCase() ?? user.email[0].toUpperCase()}
                </span>
                <span className="hidden max-w-28 truncate sm:block">{user.name || user.email}</span>
                <span className="rounded-sm bg-accent/15 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-accent">
                  {user.plan}
                </span>
                <svg className="h-3.5 w-3.5 text-muted-foreground" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="1.5" fill="none" strokeLinecap="round" />
                </svg>
              </button>
              {menuOpen && (
                <>
                  <div className="fixed inset-0 z-10" onClick={() => setMenuOpen(false)} />
                  <div className="absolute right-0 top-full z-20 mt-1 w-48 rounded-xl border border-border bg-surface shadow-elevated">
                    <div className="border-b border-border px-4 py-3">
                      <div className="text-xs font-semibold text-foreground truncate">{user.email}</div>
                      <div className="mt-0.5 text-[11px] text-muted-foreground">{user.analyses_count} analyses</div>
                    </div>
                    <div className="p-1">
                      <Link to="/dashboard" search={{ keyword: "", vertical: "saas", intent: "informational" }} onClick={() => setMenuOpen(false)}
                        className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-foreground/80 hover:bg-surface-raised/60">
                        📊 Dashboard
                      </Link>
                      <Link to="/pricing" onClick={() => setMenuOpen(false)}
                        className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-foreground/80 hover:bg-surface-raised/60">
                        ⬆ Upgrade plan
                      </Link>
                      <button onClick={handleLogout}
                        className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-destructive hover:bg-destructive/10">
                        Sign out
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>
          ) : (
            <>
              <Link
                to="/auth/login"
                className="hidden rounded-md px-4 py-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground sm:inline-flex"
              >
                Log in
              </Link>
              <Link
                to="/auth/signup"
                className="inline-flex items-center gap-1.5 rounded-md bg-accent px-4 py-2 text-sm font-semibold text-accent-foreground shadow-[0_0_20px_-6px_var(--accent)] transition-all hover:bg-accent-glow"
              >
                Get started
                <span aria-hidden>→</span>
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
