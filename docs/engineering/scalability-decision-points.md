# Scalability decision points (DATA-11 / Track B B11)

This note records where catalog trust and verification workflows will need scaling decisions as ISKONNECT grows beyond solo-operator maintenance.

## Verification freshness SLA

- **30 days** (`STALE_VERIFICATION_DAYS`): active listings with stale `last_verified_at` are moved to `needs_review` by `catalog_maintenance`.
- **90 days** (`VERIFICATION_FRESH_DAYS`): admin dashboards and maintenance job metrics treat verification older than 90 days as SLA breach (`expired_verification`, `provider_verification_sla`).

Decision point: when verified catalog exceeds ~500 live rows, split maintenance into provider-scoped jobs so one slow provider does not block global cache invalidation.

## Organization canonicalization

Provider strings are normalized through the `organizations` table on persist and staging import warns on `unknown_provider`. Search filters prefer organization `canonical_name` over raw `provider`.

Decision point: at ~200 distinct providers, add alias review queue and block publish when `organization_id` is null after import.

## Public freshness surface

Search cards and detail pages expose `FreshnessChipRow` (last verified, link status, needs verification). API payloads include `freshness_chips` from `build_freshness_chips`.

Decision point: if card payload size grows, serve chips only on detail and match rows; keep search cards to a single chip.

## Admin throughput

`GET /admin/dashboard/catalog-health` aggregates verification age buckets and top providers past SLA.

Decision point: when verification throughput exceeds ~50 listings/week, add assignee queues and per-bundle SLA targets instead of a single global dashboard.
