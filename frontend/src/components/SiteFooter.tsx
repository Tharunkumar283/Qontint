import { Logo } from "./Logo";

export function SiteFooter() {
  return (
    <footer className="mt-32 border-t border-border/60 bg-surface/40">
      <div className="container mx-auto grid grid-cols-2 gap-10 px-6 py-14 md:grid-cols-5 lg:px-8">
        <div className="col-span-2">
          <Logo />
          <p className="mt-4 max-w-xs text-sm leading-relaxed text-muted-foreground">
            The Semantic Authority Operating System. Predict rankings before you publish.
          </p>
          <div className="mt-6 inline-flex items-center gap-2 rounded-full border border-border-strong/60 bg-surface-raised/40 px-3 py-1 text-xs text-muted-foreground">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-success" />
            All systems operational
          </div>
        </div>
        {[
          { title: "Product", items: ["Features", "Verticals", "Pricing", "Changelog"] },
          { title: "Resources", items: ["Docs", "API", "Methodology", "Status"] },
          { title: "Company", items: ["About", "Blog", "Careers", "Contact"] },
        ].map((col) => (
          <div key={col.title}>
            <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              {col.title}
            </div>
            <ul className="mt-4 space-y-2.5">
              {col.items.map((it) => (
                <li key={it}>
                  <a className="text-sm text-foreground/80 transition-colors hover:text-foreground">{it}</a>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div className="border-t border-border/60">
        <div className="container mx-auto flex flex-col items-start justify-between gap-3 px-6 py-6 text-xs text-muted-foreground sm:flex-row sm:items-center lg:px-8">
          <div>© {new Date().getFullYear()} Qontint Inc. — Semantic Authority OS.</div>
          <div className="flex gap-5">
            <a>Privacy</a>
            <a>Terms</a>
            <a>Security</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
