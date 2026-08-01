# MATCH-02 Report — Strict eval oracle

## Objective

Measure engine over-inclusion against a fail-closed oracle baseline.

## Changes

- `eval/oracle.py`: `is_eligible(..., unknown_policy="lenient"|"strict")`.
- `eval/run_eval.py`: runs strict oracle paths; reports `over_inclusion_rate` (FP / (TP+FP) vs strict).
- `eval/generate_data.py`: four targeted sparse profiles (missing GWA, income, region, school).
- `test_eval_regression.py`: asserts strict mode output exists; **no threshold gate** on over-inclusion.

## Baseline

Over-inclusion rate (PROD path, strict oracle): **0.047%** (`0.000469`). Recorded in eval JSON output (`over_inclusion_rate.prod`). Threshold to be set in Phase 4 once real catalog data exists.

## Notes

Lenient oracle thresholds in CI are unchanged. Strict mode is report-only.
