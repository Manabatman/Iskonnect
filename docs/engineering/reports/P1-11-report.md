# P1-11 Report

## Objective

Harden API warm-up: shorten keepalive interval and add a second independent pinger.

## Files changed

- `.github/workflows/keepalive.yml` — every 5 minutes
- `.github/workflows/keepalive-secondary.yml` — offset cron pinger

## Tests

- [x] Workflow YAML valid (manual review)
