import { type ReactNode } from "react";

export function MetricCard({
  label,
  value,
  delta,
  hint,
  accent = false,
  icon,
}: {
  label: string;
  value: ReactNode;
  delta?: string;
  hint?: string;
  accent?: boolean;
  icon?: ReactNode;
}) {
  return (
    <div className="group relative overflow-hidden rounded-xl border border-border bg-surface/60 p-5 transition-colors hover:border-border-strong">
      {accent && (
        <div
          aria-hidden
          className="pointer-events-none absolute -right-8 -top-8 h-32 w-32 rounded-full bg-accent/15 blur-2xl"
        />
      )}
      <div className="flex items-center justify-between">
        <div className="text-xs font-medium uppercase tracking-wider text-muted-foreground">{label}</div>
        {icon && <div className="text-muted-foreground/70">{icon}</div>}
      </div>
      <div
        className={`mt-3 font-display text-3xl font-semibold tabular-nums ${
          accent ? "gradient-text-accent" : "text-foreground"
        }`}
      >
        {value}
      </div>
      <div className="mt-2 flex items-center gap-2 text-xs">
        {delta && (
          <span className="rounded-md bg-success/10 px-1.5 py-0.5 font-medium text-success">{delta}</span>
        )}
        {hint && <span className="text-muted-foreground">{hint}</span>}
      </div>
    </div>
  );
}
