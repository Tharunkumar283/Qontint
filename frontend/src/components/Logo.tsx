export function Logo({ className = "" }: { className?: string }) {
  return (
    <div className={`flex items-center gap-2.5 ${className}`}>
      <div className="relative h-7 w-7">
        <div className="absolute inset-0 rounded-md bg-accent/20 blur-md" aria-hidden />
        <svg viewBox="0 0 32 32" className="relative h-7 w-7" aria-hidden>
          <defs>
            <linearGradient id="qg" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="oklch(78% 0.16 56.34)" />
              <stop offset="100%" stopColor="oklch(60% 0.16 56.34)" />
            </linearGradient>
          </defs>
          <circle cx="16" cy="16" r="13" fill="none" stroke="url(#qg)" strokeWidth="2" />
          <circle cx="16" cy="16" r="4" fill="url(#qg)" />
          <line x1="22" y1="22" x2="28" y2="28" stroke="url(#qg)" strokeWidth="2.5" strokeLinecap="round" />
          <circle cx="6" cy="10" r="1.5" fill="oklch(78% 0.16 56.34)" />
          <circle cx="26" cy="8" r="1.5" fill="oklch(78% 0.16 56.34)" />
          <circle cx="8" cy="24" r="1.5" fill="oklch(78% 0.16 56.34)" />
        </svg>
      </div>
      <div className="flex items-baseline gap-1.5">
        <span className="font-display text-lg font-semibold tracking-tight">Qontint</span>
        <span className="hidden sm:inline rounded-full border border-border-strong/60 bg-surface-raised/60 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wider text-muted-foreground">
          OS
        </span>
      </div>
    </div>
  );
}
