"""Status and coding rules for the AI governance replication project."""

from __future__ import annotations

from typing import Iterable

import pandas as pd


ALLOWED_STATUSES = [
    "Implemented",
    "Partially implemented",
    "Not implemented",
    "Unable to verify",
    "No longer applicable",
]

ALLOWED_CONFIDENCE_LEVELS = ["High", "Medium", "Low"]

ALLOWED_REQUIREMENT_TYPES = [
    "Governance",
    "Transparency",
    "Risk management",
    "Reporting",
    "Procurement",
    "Workforce",
    "Standards",
    "Agency coordination",
]

STATUS_RANK = {
    "Implemented": 4,
    "Partially implemented": 3,
    "Unable to verify": 2,
    "Not implemented": 1,
    "No longer applicable": 0,
}


def validate_allowed_values(
    dataframe: pd.DataFrame,
    column: str,
    allowed_values: Iterable[str],
) -> list[str]:
    """Return a list of invalid values for a dataframe column."""
    if column not in dataframe.columns:
        return [f"Missing column: {column}"]

    allowed = set(allowed_values)
    observed = {
        value
        for value in dataframe[column].dropna().astype(str).unique().tolist()
        if value not in allowed
    }
    return sorted(observed)


def derive_status_change(original_status: str, updated_status: str) -> str:
    """Compare two status values and assign a simple change label."""
    if not original_status or not updated_status:
        return ""
    if original_status == updated_status:
        return "No change"
    if updated_status == "No longer applicable":
        return "No longer applicable"

    original_rank = STATUS_RANK.get(original_status)
    updated_rank = STATUS_RANK.get(updated_status)

    if original_rank is None or updated_rank is None:
        return "Needs review"
    if updated_rank > original_rank:
        return "Improved"
    if updated_rank < original_rank:
        return "Declined"
    return "Changed"


def add_status_change_column(
    dataframe: pd.DataFrame,
    original_column: str = "original_status",
    updated_column: str = "updated_2026_status",
    output_column: str = "status_change",
) -> pd.DataFrame:
    """Attach a derived status-change column to a dataframe."""
    updated = dataframe.copy()
    updated[output_column] = updated.apply(
        lambda row: derive_status_change(
            str(row.get(original_column, "")),
            str(row.get(updated_column, "")),
        ),
        axis=1,
    )
    return updated
