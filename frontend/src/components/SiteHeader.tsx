import { Link } from "@tanstack/react-router";
import { Logo } from "./Logo";

const nav = [
  { to: "/", label: "Home" },
  { to: "/analyze", label: "Analyze" },
  { to: "/dashboard", label: "Dashboard" },
  { to: "/graph", label: "Knowledge Graph" },
  { to: "/pricing", label: "Pricing" },
] as const;

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-border/60 bg-background/80 backdrop-blur-xl">
      <div className="container mx-auto flex h-16 items-center justify-between px-6 lg:px-8">
        <Link to="/" className="transition-opacity hover:opacity-80">
          <Logo />
        </Link>
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
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <button className="hidden rounded-md px-4 py-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground sm:inline-flex">
            Log in
          </button>
          <Link
            to="/analyze"
            className="inline-flex items-center gap-1.5 rounded-md bg-accent px-4 py-2 text-sm font-semibold text-accent-foreground shadow-[0_0_20px_-6px_var(--accent)] transition-all hover:bg-accent-glow"
          >
            Get started
            <span aria-hidden>→</span>
          </Link>
        </div>
      </div>
    </header>
  );
}
