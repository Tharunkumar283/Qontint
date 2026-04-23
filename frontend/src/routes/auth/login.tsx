import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { login } from "@/lib/api";

export const Route = createFileRoute("/auth/login")({
  head: () => ({
    meta: [
      { title: "Sign in — Qontint" },
      { name: "description", content: "Sign in to Qontint to access AI-powered content ranking predictions." },
    ],
  }),
  component: LoginPage,
});

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) return;
    setLoading(true);
    setError("");
    try {
      const res = await login({ email, password });
      if (res.success) {
        navigate({ to: "/dashboard", search: { keyword: "best saas pricing", vertical: "saas", intent: "informational" } });
      } else {
        setError(res.error || "Login failed");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative flex min-h-[calc(100vh-4rem)] items-center justify-center px-4">
      <div aria-hidden className="pointer-events-none absolute inset-0 grid-bg opacity-40" />
      <div className="relative w-full max-w-md">
        {/* Glow */}
        <div aria-hidden className="absolute -inset-4 rounded-3xl bg-accent/10 blur-3xl" />

        <div className="relative rounded-2xl border border-border-strong/70 bg-surface/90 p-8 shadow-elevated backdrop-blur-xl">
          {/* Header */}
          <div className="text-center">
            <div className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-accent/15 text-2xl">
              ⚡
            </div>
            <h1 className="mt-4 font-display text-2xl font-semibold tracking-tight">Welcome back</h1>
            <p className="mt-1 text-sm text-muted-foreground">
              Sign in to your Qontint account
            </p>
          </div>

          {/* Form */}
          <form onSubmit={onSubmit} className="mt-8 space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Email
              </label>
              <input
                id="login-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@company.com"
                required
                className="mt-1.5 w-full rounded-md border border-border-strong bg-background/60 px-4 py-2.5 text-sm outline-none transition-colors placeholder:text-muted-foreground/50 focus:border-accent focus:ring-2 focus:ring-accent/25"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Password
              </label>
              <input
                id="login-password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="mt-1.5 w-full rounded-md border border-border-strong bg-background/60 px-4 py-2.5 text-sm outline-none transition-colors placeholder:text-muted-foreground/50 focus:border-accent focus:ring-2 focus:ring-accent/25"
              />
            </div>

            {error && (
              <div className="rounded-md border border-destructive/40 bg-destructive/10 px-4 py-2.5 text-sm text-destructive">
                ⚠ {error}
              </div>
            )}

            <button
              id="login-submit"
              type="submit"
              disabled={loading || !email || !password}
              className="w-full rounded-md bg-accent px-4 py-2.5 text-sm font-semibold text-accent-foreground shadow-[0_0_20px_-6px_var(--accent)] transition-all hover:bg-accent-glow disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-accent-foreground/30 border-t-accent-foreground" />
                  Signing in…
                </span>
              ) : (
                "Sign in →"
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="my-6 flex items-center gap-3">
            <div className="flex-1 border-t border-border" />
            <span className="text-xs text-muted-foreground">or</span>
            <div className="flex-1 border-t border-border" />
          </div>

          {/* Demo login */}
          <button
            onClick={() => { setEmail("demo@qontint.app"); setPassword("demo123"); }}
            className="w-full rounded-md border border-border-strong px-4 py-2.5 text-sm font-medium text-foreground/80 transition-colors hover:bg-surface-raised/50"
          >
            Use demo credentials
          </button>

          <p className="mt-6 text-center text-sm text-muted-foreground">
            Don't have an account?{" "}
            <Link to="/auth/signup" className="font-medium text-accent hover:underline">
              Sign up for free
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
