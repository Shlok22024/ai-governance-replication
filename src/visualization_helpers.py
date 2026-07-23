"""Reusable plotting helpers for the AI governance replication project."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


STATUS_COLORS = {
    "Implemented": "#1b9e77",
    "Unknown": "#7570b3",
    "Not implemented": "#d95f02",
}


def set_project_style() -> None:
    """Apply a clean plotting style for portfolio-ready figures."""
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams["figure.figsize"] = (12, 6)
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 11


def plot_policy_status_breakdown(
    dataframe: pd.DataFrame,
    title: str,
) -> plt.Figure:
    """Build a horizontal stacked bar chart from policy summary data."""
    set_project_style()

    figure, axis = plt.subplots()
    instruments = dataframe["instrument"]
    implemented = dataframe["implemented_pct"]
    unknown = dataframe["unknown_pct"]
    not_implemented = dataframe["not_implemented_pct"]

    axis.barh(
        instruments,
        implemented,
        color=STATUS_COLORS["Implemented"],
        label="Implemented",
    )
    axis.barh(
        instruments,
        unknown,
        left=implemented,
        color=STATUS_COLORS["Unknown"],
        label="Unknown",
    )
    axis.barh(
        instruments,
        not_implemented,
        left=implemented + unknown,
        color=STATUS_COLORS["Not implemented"],
        label="Not implemented",
    )

    axis.set_title(title)
    axis.set_xlabel("Percent of tracked requirements")
    axis.set_xlim(0, 100)
    axis.legend(
        frameon=False,
        ncol=3,
        bbox_to_anchor=(0.5, 1.02),
        loc="lower center",
    )

    for spine in ("top", "right"):
        axis.spines[spine].set_visible(False)

    figure.tight_layout()
    return figure


def save_figure(figure: plt.Figure, output_path: Path | str) -> None:
    """Save a matplotlib figure to disk."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(figure)
