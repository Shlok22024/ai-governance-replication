"""Derived evidence-quality index for requirement-level coding.

`confidence_index` expresses confidence in the CODING DECISION, not in the
implementation outcome. It is a deterministic function of the evidence fields
below and is never hand-entered.

Two branches, because two different claims are being scored:

  evidence_found = Yes  ->  confidence in a positive coding.
                            Driven by specificity and temporal fit.
  evidence_found = No   ->  confidence in the negative claim "the public record
                            is silent." Driven by search scope and breadth.

Consequence, and the point of the redesign: an `Unable to verify` row reached
after an exhaustive multi-source search scores High. It is a strong, well
supported finding about public verifiability, not a weak one.
"""

from __future__ import annotations

import pandas as pd


EVIDENCE_FOUND = ["Yes", "No"]

EVIDENCE_SPECIFICITY = [
    "Requirement-specific",
    "Program-level",
    "Agency-level",
    "Generic/context-only",
]

EVIDENCE_TEMPORAL_FIT = [
    "Current and directly applicable",
    "Historical but applicable",
    "Current but policy context changed",
    "Undated or unclear",
    "Not applicable",
]

SEARCH_SCOPE = ["Exhaustive", "Targeted", "Cursory", "Not searched", "Not recorded"]

CONFIDENCE_LEVELS = ["High", "Medium", "Low"]

_TEMPORAL_CAPPED_AT_MEDIUM = {"Current but policy context changed"}
_TEMPORAL_FORCES_LOW = {"Undated or unclear"}

_STRONG_SEARCH = {"Exhaustive", "Targeted"}


def confidence_index(row: pd.Series) -> str:
    """Return High / Medium / Low for one coded requirement row."""
    found = row["evidence_found"]
    scope = row.get("search_scope")
    n_sources = row.get("sources_checked")
    n_sources = 0 if pd.isna(n_sources) else int(n_sources)

    if found == "No":
        return _no_evidence_branch(scope, n_sources)
    return _evidence_branch(row, scope)


def _no_evidence_branch(scope: str, n_sources: int) -> str:
    """Confidence that the public record is genuinely silent."""
    if scope == "Exhaustive" and n_sources >= 4:
        return "High"
    if scope in _STRONG_SEARCH and n_sources >= 2:
        return "Medium"
    return "Low"


def _evidence_branch(row: pd.Series, scope: str) -> str:
    """Confidence that located evidence supports the assigned status."""
    specificity = row["evidence_specificity"]
    temporal = row["evidence_temporal_fit"]

    if scope in ("Cursory", "Not searched", "Not recorded"):
        return "Low"
    if temporal in _TEMPORAL_FORCES_LOW:
        return "Low"
    if specificity == "Generic/context-only":
        return "Low"

    if (
        specificity == "Requirement-specific"
        and temporal not in _TEMPORAL_CAPPED_AT_MEDIUM
    ):
        return "High"
    return "Medium"


def apply_confidence_index(df: pd.DataFrame) -> pd.DataFrame:
    """Add confidence_index and confidence_changed. Does not mutate input."""
    out = df.copy()
    out["confidence_index"] = out.apply(confidence_index, axis=1)
    if "previous_verification_confidence" in out.columns:
        out["confidence_changed"] = (
            out["confidence_index"] != out["previous_verification_confidence"]
        ).map({True: "Yes", False: "No"})
    return out


def validate_values(df: pd.DataFrame) -> list[str]:
    """Return a list of vocabulary and consistency violations."""
    problems: list[str] = []
    checks = {
        "evidence_found": EVIDENCE_FOUND,
        "evidence_specificity": EVIDENCE_SPECIFICITY,
        "evidence_temporal_fit": EVIDENCE_TEMPORAL_FIT,
        "search_scope": SEARCH_SCOPE,
    }
    for col, allowed in checks.items():
        if col not in df.columns:
            problems.append(f"missing column: {col}")
            continue
        bad = set(df[col].dropna().unique()) - set(allowed)
        if bad:
            problems.append(f"{col}: unexpected values {sorted(bad)}")

    if {"evidence_found", "evidence_specificity"} <= set(df.columns):
        leaked = df[(df.evidence_found == "No") & df.evidence_specificity.notna()]
        if len(leaked):
            problems.append(
                f"{len(leaked)} rows have evidence_specificity while "
                "evidence_found = No (must be blank)"
            )

    if {"evidence_found", "sources_checked"} <= set(df.columns):
        zero = df[(df.evidence_found == "Yes") & (df.sources_checked.fillna(0) < 1)]
        if len(zero):
            problems.append(
                f"{len(zero)} rows claim evidence_found = Yes with "
                "sources_checked < 1"
            )
    return problems


def check_collinearity(
    df: pd.DataFrame,
    status_col: str,
    index_col: str = "confidence_index",
    threshold: float = 0.70,
) -> pd.DataFrame:
    """Flag statuses that still map to a single confidence value."""
    tab = pd.crosstab(df[status_col], df[index_col])
    share = tab.div(tab.sum(axis=1), axis=0)
    flagged = share.max(axis=1) > threshold
    report = pd.DataFrame(
        {
            "n": tab.sum(axis=1),
            "dominant_value": share.idxmax(axis=1),
            "dominant_share": share.max(axis=1).round(3),
            "flagged": flagged,
        }
    )
    return report.sort_values("dominant_share", ascending=False)


def sources_checked_from_log(
    log: pd.DataFrame, id_col: str = "requirement_id", url_col: str = "url"
) -> pd.Series:
    """Count distinct URLs per requirement from data/raw/search_log.csv."""
    return log.groupby(id_col)[url_col].nunique()
