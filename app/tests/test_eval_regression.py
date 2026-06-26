"""
Regression gate: synthetic 100x200 evaluation must meet recall/precision floors.

Thresholds are set from post-remediation empirical baselines; fail CI if matching
quality regresses.
"""

from eval.run_eval import run_full_evaluation

# Post-remediation PROD baselines (update only when intentionally changing matching policy)
PROD_RECALL_MIN = 0.99
PROD_PRECISION_MIN = 0.995
PROD_FP_MAX = 10
PROD_SENIOR_HIGH_RECALL_MIN = 0.95
PROD_EXPLANATION_COVERAGE_MIN = 0.95


def test_matching_eval_prod_recall_and_precision():
    report = run_full_evaluation()
    prod = report["prod"]
    assert prod["recall"] >= PROD_RECALL_MIN, (
        f"PROD recall {prod['recall']:.3f} < {PROD_RECALL_MIN}; FN causes: {prod['fn_causes']}"
    )
    assert prod["precision"] >= PROD_PRECISION_MIN, (
        f"PROD precision {prod['precision']:.3f} < {PROD_PRECISION_MIN}; FP causes: {prod['fp_causes']}"
    )
    assert prod["confusion"]["FP"] <= PROD_FP_MAX, (
        f"PROD FP {prod['confusion']['FP']} > {PROD_FP_MAX}"
    )


def test_matching_eval_senior_high_recall():
    report = run_full_evaluation()
    sh_recall, n = report["prod"]["recall_by_level"].get("senior high", (0, 0))
    assert n > 0, "expected senior-high eligible pairs in synthetic dataset"
    assert sh_recall >= PROD_SENIOR_HIGH_RECALL_MIN, (
        f"senior-high recall {sh_recall:.3f} < {PROD_SENIOR_HIGH_RECALL_MIN}"
    )


def test_matching_eval_explanation_coverage():
    report = run_full_evaluation()
    cov = report["prod"]["explanation_coverage"]
    assert cov is not None
    assert cov >= PROD_EXPLANATION_COVERAGE_MIN, (
        f"explanation coverage {cov:.3f} < {PROD_EXPLANATION_COVERAGE_MIN}"
    )
