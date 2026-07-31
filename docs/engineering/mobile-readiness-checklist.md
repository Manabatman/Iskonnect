# MOB-16 — Mobile readiness checklist (Phase 2 exit)

| Check | Status |
| --- | --- |
| Viewport meta (`width=device-width`, `viewport-fit=cover`) | ✅ |
| Touch targets ≥ 44px on chrome (navbar sheet, bottom nav, footer) | ✅ |
| Bottom nav on authenticated shells | ✅ |
| Safe-area insets (top/bottom) | ✅ |
| Filter bottom sheet on search (MOB-07) | ✅ |
| Reduced motion global guard | ✅ |
| Self-hosted fonts (no Google Fonts runtime) | ✅ |
| PWA manifest valid JSON | ✅ |
| Touch inventory post-viewport (MOB-01) | ✅ 0 violations (6 public routes) |
| Design system reference route `/design-system` | ✅ |

## Manual QA (360×640)
- [ ] Login → dashboard flow
- [ ] Search filters sheet opens/closes
- [ ] Profile builder stepper scroll
- [ ] Dark mode token contrast

## Known deferrals
- Full raw palette sweep (DS-09) — incremental; guarded paths enforced via DS-17
- Landing LAND-* redesign — Phase 5
