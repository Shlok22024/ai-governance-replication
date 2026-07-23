"""Create the first reproducible table and figure from the paper summary."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_cleaning import project_path, save_csv
from visualization_helpers import plot_policy_status_breakdown, save_figure


def build_summary_table() -> pd.DataFrame:
    """Return the seeded policy-level summary from Table 1 of the paper."""
    return pd.DataFrame(
        [
            {
                "assessment_date": "2022-11",
                "instrument": "AI Leadership Order",
                "implemented_pct": 39,
                "unknown_pct": 57,
                "not_implemented_pct": 4,
                "notes": "Paper Table 1 summary as of November 2022.",
            },
            {
                "assessment_date": "2022-11",
                "instrument": "Trustworthy AI Order",
                "implemented_pct": 13,
                "unknown_pct": 75,
                "not_implemented_pct": 13,
                "notes": "Paper Table 1 summary as of November 2022.",
            },
            {
                "assessment_date": "2022-11",
                "instrument": "AI in Government Act",
                "implemented_pct": 17,
                "unknown_pct": 17,
                "not_implemented_pct": 67,
                "notes": "Paper Table 1 summary as of November 2022.",
            },
            {
                "assessment_date": "2022-11",
                "instrument": "Total",
                "implemented_pct": 27,
                "unknown_pct": 58,
                "not_implemented_pct": 16,
                "notes": "Paper Table 1 summary as of November 2022.",
            },
        ]
    )


def main() -> None:
    """Write the seeded summary table and the original-summary figure."""
    summary = build_summary_table()

    summary_output = project_path("outputs", "tables", "summary_table.csv")
    figure_output = project_path(
        "outputs",
        "figures",
        "implementation_status_original.png",
    )

    save_csv(summary, summary_output)
    figure = plot_policy_status_breakdown(
        summary,
        "Original Paper Summary of Federal AI Governance Implementation",
    )
    save_figure(figure, figure_output)

    print(f"Wrote {summary_output}")
    print(f"Wrote {figure_output}")


if __name__ == "__main__":
    main()
