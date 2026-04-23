import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { register } from "@/lib/api";
import type { Vertical } from "@/lib/types";

export const Route = createFileRoute("/auth/signup")({
  head: () => ({
    meta: [
      { title: "Create account — Qontint" },
      { name: "description", content: "Start predicting content rankings with Qontint. Free to start." },
    ],
  }),
  component: SignupPage,
});

const PLANS = [
  { id: "starter", label: "Starter", price: "$99/mo", features: ["5 analyses/day", "SaaS vertical", "JSON export", "Email support"] },
  { id: "professional", label: "Professional", price: "$299/mo", features: ["Unlimited analyses", "All 6 verticals", "CSV + JSON export", "Priority support", "YouTube prediction"] },
  { id: "enterprise", label: "Enterprise", price: "$499/mo", features: ["Everything in Pro", "Custom SLM training", "API access", "Dedicated CSM", "Neo4j + PostgreSQL"] },
];

function SignupPage() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [plan, setPlan] = useState("starter");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) return;
    if (password.length < 6) { setError("Password must be at least 6 characters"); return; }
    setLoading(true);
    setError("");
    try {
      const res = await register({ email, password, name, plan: plan as any });
      if (res.success) {
        navigate({ to: "/dashboard", search: { keyword: "best saas pricing", vertical: "saas", intent: "informational" } });
      } else {
        setError(res.error || "Registration failed");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative px-4 py-16">
      <div aria-hidden className="pointer-events-none absolute inset-0 grid-bg opacity-40" />
      <div className="relative mx-auto max-w-4xl">
        <div className="text-center">
          <h1 className="font-display text-4xl font-semibold tracking-tight">
            Start predicting rankings
          </h1>
          <p className="mt-3 text-muted-foreground">No credit card required. Cancel anytime.</p>
        </div>

        <div className="mt-12 grid gap-8 lg:grid-cols-2">
          {/* Plan selector */}
          <div>
            <h2 className="font-display text-lg font-semibold">Choose your plan</h2>
            <div className="mt-4 space-y-3">
              {PLANS.map((p) => {
                const active = plan === p.id;
                return (
                  <button
                    key={p.id}
                    type="button"
                    onClick={() => setPlan(p.id)}
                    className={`w-full rounded-xl border p-4 text-left transition-all ${
                      active
                        ? "border-accent/60 bg-accent/[0.06] shadow-[0_0_0_1px_var(--accent)]"
                        : "border-border bg-surface/60 hover:border-border-strong"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="font-display font-semibold">{p.label}</div>
                      <div className={`font-mono text-sm font-bold ${active ? "text-accent" : "text-foreground"}`}>
                        {p.price}
                      </div>
                    </div>
                    <ul className="mt-2 space-y-1">
                      {p.features.map((f) => (
                        <li key={f} className="flex items-center gap-2 text-xs text-muted-foreground">
                          <span className="text-success">✓</span> {f}
                        </li>
                      ))}
                    </ul>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Sign up form */}
          <div>
            <div className="relative rounded-2xl border border-border-strong/70 bg-surface/90 p-6 shadow-elevated backdrop-blur-xl">
              <div aria-hidden className="absolute -inset-4 -z-10 rounded-3xl bg-accent/8 blur-3xl" />
              <h2 className="font-display text-lg font-semibold">Create your account</h2>

              <form onSubmit={onSubmit} className="mt-5 space-y-4">
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    Full name
                  </label>
                  <input
                    id="signup-name"
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Jane Smith"
                    className="mt-1.5 w-full rounded-md border border-border-strong bg-background/60 px-4 py-2.5 text-sm outline-none placeholder:text-muted-foreground/50 focus:border-accent focus:ring-2 focus:ring-accent/25"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    Work email
                  </label>
                  <input
                    id="signup-email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@company.com"
                    required
                    className="mt-1.5 w-full rounded-md border border-border-strong bg-background/60 px-4 py-2.5 text-sm outline-none placeholder:text-muted-foreground/50 focus:border-accent focus:ring-2 focus:ring-accent/25"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    Password
                  </label>
                  <input
                    id="signup-password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Min. 6 characters"
                    required
                    className="mt-1.5 w-full rounded-md border border-border-strong bg-background/60 px-4 py-2.5 text-sm outline-none placeholder:text-muted-foreground/50 focus:border-accent focus:ring-2 focus:ring-accent/25"
                  />
                </div>

                {error && (
                  <div className="rounded-md border border-destructive/40 bg-destructive/10 px-4 py-2.5 text-sm text-destructive">
                    ⚠ {error}
                  </div>
                )}

                <div className="rounded-lg border border-border bg-surface-raised/40 p-3 text-xs text-muted-foreground">
                  Selected plan: <span className="font-semibold text-foreground capitalize">{plan}</span> ·{" "}
                  {PLANS.find((p) => p.id === plan)?.price}
                </div>

                <button
                  id="signup-submit"
                  type="submit"
                  disabled={loading || !email || !password}
                  className="w-full rounded-md bg-accent px-4 py-2.5 text-sm font-semibold text-accent-foreground shadow-[0_0_20px_-6px_var(--accent)] transition-all hover:bg-accent-glow disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-accent-foreground/30 border-t-accent-foreground" />
                      Creating account…
                    </span>
                  ) : (
                    "Create account →"
                  )}
                </button>

                <p className="text-center text-xs text-muted-foreground">
                  By signing up you agree to our Terms of Service and Privacy Policy.
                </p>
              </form>
            </div>

            <p className="mt-4 text-center text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link to="/auth/login" className="font-medium text-accent hover:underline">
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
