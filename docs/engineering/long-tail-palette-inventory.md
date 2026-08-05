# DS-18 — Long-tail raw palette inventory

Phase 2 tokenized **guarded paths** (see `scripts/check-design-tokens.mjs`). Remaining raw Tailwind palette utilities live primarily in:

- Landing sections (`components/landing/*`) — Phase 5
- Dashboard cards and profile builder steps — migrate in Phase 3+
- Admin/sponsor portals — lower traffic

## Migration strategy
1. Replace `bg-slate-*` / `text-slate-*` with `bg-background`, `text-foreground`, `text-muted-foreground`, `bg-muted`, `border-border`
2. Replace status colors with `Badge` variants or `bg-tone-*` utilities
3. Run `npm run audit:design-tokens` before merge

## Approximate counts (pre-Phase 2 audit)
~3,239 raw palette class usages codebase-wide; Phase 2 migrated chrome, auth login, badges, and UI primitives.
