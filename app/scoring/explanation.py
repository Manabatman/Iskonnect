"""
Deterministic match explanation generator.
Produces breakdown and plain-language explanation for every score.
"""

from app.matching.hard_filters import DEADLINE_PASSED_MESSAGE
from app.matching.scoring_port import ScoringPayload
from app.taxonomy.equity_groups import EQUITY_GROUPS

__all__ = ["DEADLINE_PASSED_MESSAGE", "build_breakdown", "build_explanation", "build_why_not_higher", "build_improvement_suggestions", "assess_confidence"]


def _get_equity_match_reason(equity_flags: dict[str, bool], priority_groups: list[str]) -> str | None:
    """Return the first matching equity group's RA reference for explanation (uses profile_flag like scoring)."""
    for group in priority_groups or []:
        if not group:
            continue
        flag_key = group.lower().replace(" ", "_").replace("/", "_")
        profile_flag = EQUITY_GROUPS.get(group, {}).get("profile_flag") or f"is_{flag_key}"
        if equity_flags.get(flag_key) or equity_flags.get(profile_flag) or equity_flags.get(group):
            info = EQUITY_GROUPS.get(group, {})
            ra = info.get("ra_reference", group)
            return f"{group} ({ra})"
    return None


def build_breakdown(
    components: dict[str, float],
    payload: ScoringPayload,
    normalized_weights: dict[str, float],
) -> dict:
    """
    Build structured breakdown compatible with MatchBreakdownSchema.
    normalized_weights: per-component weights after excluding not-applicable factors (sum to 1.0).
    """
    def _row(comp_key: str, status: str, user_val: str, req_val: str) -> dict:
        nw = normalized_weights.get(comp_key, 0.0)
        if status == "not_applicable" or nw <= 0:
            return {
                "status": status,
                "user_value": user_val,
                "requirement_value": req_val,
                "score": None,
                "weighted": 0.0,
                "max_possible": 0.0,
            }
        sc = components.get(comp_key, 0.0)
        return {
            "status": status,
            "user_value": user_val,
            "requirement_value": req_val,
            "score": sc,
            "weighted": round(sc * nw * 100, 1),
            "max_possible": round(nw * 100, 1),
        }

    def _academic_detail() -> tuple[str, str, str]:
        gwa = payload.gwa_normalized
        min_gwa = payload.min_gwa_required
        if gwa is None:
            return ("not_provided", "Not provided", "N/A" if min_gwa is None else f"Min: {min_gwa:.0f}%")
        if min_gwa is None:
            return ("met", f"GWA: {gwa:.1f}%", "No minimum")
        if gwa >= min_gwa + 10:
            return ("exceeded", f"GWA: {gwa:.1f}%", f"Min: {min_gwa:.0f}% (exceeds by {gwa - min_gwa:.0f})")
        if gwa >= min_gwa:
            return ("met", f"GWA: {gwa:.1f}%", f"Min: {min_gwa:.0f}%")
        return ("not_met", f"GWA: {gwa:.1f}%", f"Min: {min_gwa:.0f}%")

    def _socioeconomic_detail() -> tuple[str, str, str]:
        income = payload.household_income_annual
        threshold = payload.max_income_threshold
        st = (payload.scholarship_type or "").lower().strip()
        merit_types = ("merit", "merit-based", "academic")
        if st in merit_types:
            return ("met", "N/A", "Merit-based — income not used in ranking")
        if threshold is None:
            return ("met", "N/A", "No income limit")
        if income is not None:
            if income <= threshold:
                return ("met", f"PHP {income:,}", f"Max: PHP {threshold:,}")
            return ("not_met", f"PHP {income:,}", f"Max: PHP {threshold:,}")
        return ("not_provided", "Not provided", f"Max: PHP {threshold:,}")

    def _field_detail() -> tuple[str, str, str]:
        level = (payload.field_match_level or "none").strip().lower()
        labels = {
            "exact": "Exact match",
            "broad": "Broad match",
            "partial": "Partial match",
            "none": "No match",
        }
        user = labels.get(level, level)
        if not payload.has_field_restriction:
            disp = user if level != "none" else "—"
            return ("not_applicable", disp, "Open to all fields")
        if level == "none":
            return ("not_met", "No course match", "Course eligibility")
        if level == "partial":
            return ("partial", user, "Course eligibility")
        return ("met", user, "Course eligibility")

    def _geographic_detail() -> tuple[str, str, str]:
        level = (payload.geographic_match_level or "none").strip().lower()
        profile_region = getattr(payload, "profile_region", None) or ""
        profile_city = getattr(payload, "profile_city", None) or ""
        eligible_regions = getattr(payload, "eligible_regions", None) or []
        eligible_cities = getattr(payload, "eligible_cities", None) or []

        user_display = profile_region or profile_city or "Not provided"
        if profile_region and profile_city:
            user_display = f"{profile_region}, {profile_city}"
        elif profile_city:
            user_display = profile_city

        if not eligible_regions and not eligible_cities:
            req_display = "Nationwide"
        elif eligible_cities:
            req_display = ", ".join(eligible_cities[:3])
            if len(eligible_cities) > 3:
                req_display += f" (+{len(eligible_cities) - 3} more)"
        else:
            req_display = ", ".join(str(r) for r in eligible_regions[:3])
            if len(eligible_regions) > 3:
                req_display += f" (+{len(eligible_regions) - 3} more)"

        if not payload.has_geographic_restriction:
            return ("not_applicable", user_display, "Nationwide (no location restriction)")
        if level == "none":
            return ("not_met", user_display, req_display)
        return ("met", user_display, req_display)

    def _equity_detail() -> tuple[str, str, str]:
        match_count = 0
        for group in payload.priority_groups or []:
            flag_key = group.lower().replace(" ", "_").replace("/", "_")
            profile_flag = EQUITY_GROUPS.get(group, {}).get("profile_flag") or f"is_{flag_key}"
            if payload.equity_flags.get(flag_key) or payload.equity_flags.get(profile_flag) or payload.equity_flags.get(group):
                match_count += 1
        if not payload.priority_groups:
            return ("met", "N/A", "No priority groups")
        if match_count > 0:
            return ("matched", f"{match_count} group(s) matched", "Priority groups")
        return ("not_met", "No match", "Priority groups")

    ac_status, ac_user, ac_req = _academic_detail()
    soc_status, soc_user, soc_req = _socioeconomic_detail()
    field_status, field_user, field_req = _field_detail()
    geo_status, geo_user, geo_req = _geographic_detail()
    eq_status, eq_user, eq_req = _equity_detail()

    return {
        "academic": _row("academic", ac_status, ac_user, ac_req),
        "socioeconomic": _row("income", soc_status, soc_user, soc_req),
        "field_relevance": _row("field_alignment", field_status, field_user, field_req),
        "geographic": _row("geographic", geo_status, geo_user, geo_req),
        "priority_group": _row("equity_priority", eq_status, eq_user, eq_req),
    }


def build_why_not_higher(
    components: dict[str, float],
    payload: ScoringPayload,
    normalized_weights: dict[str, float],
) -> list[str]:
    """Top gaps between max possible and actual weighted contribution (plain language)."""
    labels = {
        "academic": "Academic (GWA)",
        "income": "Income / financial fit",
        "field_alignment": "Field of study",
        "geographic": "Location match",
        "equity_priority": "Priority groups",
    }
    rows: list[tuple[float, str]] = []
    st_all = (payload.scholarship_type or "").lower().strip()
    merit = st_all in ("merit", "merit-based", "academic")
    for comp_key, label in labels.items():
        w = normalized_weights.get(comp_key, 0.0)
        if w <= 0:
            continue
        if comp_key == "income" and merit:
            continue
        max_pts = w * 100.0
        actual = components[comp_key] * w * 100.0
        gap = max_pts - actual
        if gap < 1.0:
            continue
        if comp_key == "academic" and payload.gwa_normalized is None and payload.min_gwa_required is not None:
            rows.append((gap, f"{label}: add your GWA — academic part is provisional (~{gap:.0f} pts below the max for this factor)."))
        elif comp_key == "income":
            if not payload.max_income_threshold:
                continue
            if payload.household_income_annual is None and payload.income_bracket is None:
                rows.append((gap, f"{label}: add income or bracket — this part is provisional (~{gap:.0f} pts below the max)."))
            else:
                rows.append((gap, f"{label}: about {gap:.0f} pts below the max — lower income vs the ceiling scores higher for need-based programs."))
        elif comp_key == "field_alignment":
            rows.append((gap, f"{label}: about {gap:.0f} pts below the max — a stronger course match would help."))
        elif comp_key == "geographic":
            rows.append((gap, f"{label}: about {gap:.0f} pts below the max — a stronger city/region match would help."))
        elif comp_key == "equity_priority":
            rows.append((gap, f"{label}: about {gap:.0f} pts below the max — more overlapping priority groups would add points."))
        else:
            rows.append((gap, f"{label}: about {gap:.0f} pts below the maximum for this factor."))

    rows.sort(key=lambda x: x[0], reverse=True)
    return [msg for _, msg in rows[:2]]


def build_explanation(
    components: dict[str, float],
    payload: ScoringPayload,
) -> list[str]:
    """Build plain-language explanation strings for the student."""
    lines: list[str] = []
    if payload.gwa_normalized is not None and payload.min_gwa_required is not None:
        if payload.gwa_normalized >= payload.min_gwa_required + 10:
            lines.append(f"GWA {payload.gwa_normalized:.0f}% exceeds minimum {payload.min_gwa_required:.0f}%")
        elif payload.gwa_normalized >= payload.min_gwa_required:
            lines.append(f"GWA {payload.gwa_normalized:.0f}% meets minimum requirement")
    elif payload.gwa_normalized is None:
        lines.append("GWA not provided — score may change when added")
    if payload.household_income_annual is not None and payload.max_income_threshold is not None:
        st = (payload.scholarship_type or "").lower().strip()
        if st not in ("merit", "merit-based", "academic") and payload.household_income_annual <= payload.max_income_threshold:
            lines.append(f"Income PHP {payload.household_income_annual:,} within ceiling PHP {payload.max_income_threshold:,}")
    if payload.has_field_restriction:
        if payload.field_match_level in ("exact", "broad"):
            lines.append("Course/field alignment")
        elif payload.field_match_level == "partial":
            lines.append("Partial course alignment")
    if payload.has_geographic_restriction:
        if payload.geographic_match_level == "city":
            lines.append("Exact LGU/city match")
        elif payload.geographic_match_level == "region":
            lines.append("Region match")
        elif payload.geographic_match_level == "island_group":
            lines.append("Island group match")
    equity_line = _get_equity_match_reason(payload.equity_flags, payload.priority_groups or [])
    if equity_line:
        lines.append(f"Equity priority: {equity_line}")

    if not lines:
        if not payload.has_field_restriction and not payload.has_geographic_restriction:
            lines.append("Open to all fields and nationwide — you meet the listed requirements.")
        elif not payload.has_field_restriction:
            lines.append("Open to all fields of study — you meet the listed requirements.")
        elif not payload.has_geographic_restriction:
            lines.append("Nationwide — no location restriction; you meet the listed requirements.")
        else:
            lines.append("You meet the listed eligibility requirements for this program.")

    return lines


def build_improvement_suggestions(components: dict[str, float], payload: ScoringPayload) -> list[str]:
    """
    Actionable tips when match scores are low or profile data is sparse.
    """
    suggestions: list[str] = []
    if payload.gwa_normalized is None:
        suggestions.append("Add your GPA/GWA to improve academic matching.")
    if payload.household_income_annual is None and payload.income_bracket is None:
        suggestions.append("Add household income or income bracket for better need-based matching.")
    if (
        payload.has_field_restriction
        and (payload.field_match_level or "").strip().lower() == "none"
    ):
        suggestions.append("Select your preferred courses or field of study to improve field alignment.")
    if (
        payload.has_geographic_restriction
        and (payload.geographic_match_level or "").strip().lower() == "none"
    ):
        suggestions.append("Add your region and city for geographic matching.")
    if components.get("academic", 1.0) < 0.6 and payload.gwa_normalized is not None:
        suggestions.append(
            "Your academic score is below this scholarship's typical range; consider programs with lower GWA floors."
        )
    return suggestions


def assess_confidence(payload: ScoringPayload) -> str:
    """
    Assess confidence based on data completeness for applicable scholarship requirements.
    """
    missing = 0
    if payload.gwa_normalized is None and payload.min_gwa_required is not None:
        missing += 1
    st = (payload.scholarship_type or "").lower().strip()
    merit = st in ("merit", "merit-based", "academic")
    if (
        not merit
        and payload.household_income_annual is None
        and payload.income_bracket is None
        and payload.max_income_threshold is not None
    ):
        missing += 1
    if missing >= 2:
        return "low"
    if missing >= 1:
        return "medium"
    return "high"
