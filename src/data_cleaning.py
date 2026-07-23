"""Shared data-cleaning helpers for the AI governance replication project."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def project_path(*parts: str) -> Path:
    """Build an absolute path rooted at the project directory."""
    return PROJECT_ROOT.joinpath(*parts)


def ensure_parent_dir(path: Path) -> None:
    """Create the parent directory for a file path if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)


def load_csv(path: Path | str) -> pd.DataFrame:
    """Load a CSV file using consistent project defaults."""
    return pd.read_csv(path)


def save_csv(dataframe: pd.DataFrame, path: Path | str) -> None:
    """Save a dataframe to CSV, creating parent folders as needed."""
    output_path = Path(path)
    ensure_parent_dir(output_path)
    dataframe.to_csv(output_path, index=False)


def normalize_text_columns(
    dataframe: pd.DataFrame,
    columns: Iterable[str],
) -> pd.DataFrame:
    """Trim whitespace and collapse blank strings for selected columns."""
    cleaned = dataframe.copy()
    for column in columns:
        if column not in cleaned.columns:
            continue
        cleaned[column] = (
            cleaned[column]
            .astype("string")
            .str.strip()
            .replace({"": pd.NA, "nan": pd.NA})
        )
    return cleaned
