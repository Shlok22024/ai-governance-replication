"""Build the simple summary-stats file for the portfolio project."""

from __future__ import annotations

import pandas as pd

from data_cleaning import load_csv, project_path


STATUS_ORDER = [
    "Implemented",
    "Not implemented",
    "Unknown / Unable to verify",
    "Excluded because deadline had not passed",
]

PAPER_STATUS_MAP = {
    "Implemented": "Implemented",
    "Not implemented": "Not implemented",
    "Unknown": "Unknown / Unable to verify",
    "Excluded": "Excluded because deadline had not passed",
}


def compute_kappa(dataframe: pd.DataFrame) -> float:
    """Compute Cohen's kappa for second-pass agreement against the paper appendix."""
    total = len(dataframe)
    paper_norm = dataframe["paper_appendix_status"].map(PAPER_STATUS_MAP)
    observed = (dataframe["replication_status"] == paper_norm).mean()
    second_pass_share = (
        dataframe["replication_status"].value_counts().reindex(STATUS_ORDER, fill_value=0) / total
    )
    paper_share = paper_norm.value_counts().reindex(STATUS_ORDER, fill_value=0) / total
    expected = float((second_pass_share * paper_share).sum())
    return (observed - expected) / (1 - expected)


def main() -> None:
    processed_dir = project_path("data", "processed")

    original_summary = load_csv(processed_dir / "implementation_status_summary.csv")
    second_pass = load_csv(processed_dir / "original_second_pass_recoding.csv")
    summary_2026 = load_csv(processed_dir / "implementation_status_summary_2026.csv")
    row_audit = load_csv(processed_dir / "row_audit_2026.csv")

    appendix_total = original_summary.loc[
        (original_summary["summary_basis"] == "aggregate_included_rows")
        & (original_summary["instrument"] == "Total")
    ].iloc[0]
    prose_total = original_summary.loc[
        (original_summary["summary_basis"] == "paper_published_narrative")
        & (original_summary["instrument"] == "Total")
    ].iloc[0]
    total_2026 = summary_2026.loc[
        (summary_2026["summary_basis"] == "comparable_baseline_45")
        & (summary_2026["instrument"] == "Total")
    ].iloc[0]

    second_pass_counts = second_pass["replication_status"].value_counts().to_dict()
    agreement_count = int((second_pass["agreement_with_paper"] == "Agree").sum())
    second_pass_total = len(second_pass)
    disagreement_count = second_pass_total - agreement_count
    kappa = compute_kappa(second_pass)

    downgraded = int(
        (row_audit["audit_decision"] == "Downgrade to Unable to verify").sum()
    )

    lines = [
        "# Summary Stats",
        "",
        "These are the main counts used in the README and report.",
        "",
        "## What the paper's appendix supports",
        f"- Rows in the counted checklist: `{int(appendix_total['total_requirements'])}`",
        f"- Appendix-based count: `Implemented {int(appendix_total['implemented_count'])}`, `Unknown {int(appendix_total['unknown_count'])}`, `Not implemented {int(appendix_total['not_implemented_count'])}`",
        f"- Paper text count: `Implemented {int(prose_total['implemented_count'])}`, `Unknown {int(prose_total['unknown_count'])}`, `Not implemented {int(prose_total['not_implemented_count'])}`",
        "",
        "## What I found in my own second check",
        f"- `Implemented`: `{int(second_pass_counts.get('Implemented', 0))}`",
        f"- `Not implemented`: `{int(second_pass_counts.get('Not implemented', 0))}`",
        f"- `Unknown / Unable to verify`: `{int(second_pass_counts.get('Unknown / Unable to verify', 0))}`",
        f"- `Excluded because deadline had not passed`: `{int(second_pass_counts.get('Excluded because deadline had not passed', 0))}`",
        f"- Agreement with the paper: `{agreement_count} of {second_pass_total}` (`{round(agreement_count / second_pass_total * 100, 1)}%`)",
        f"- Cohen's kappa: `{round(kappa, 2)}`",
        f"- Rows where my answer differed: `{disagreement_count}`",
        "",
        "## What newer public records showed on July 24, 2026",
        f"- `Implemented`: `{int(total_2026['implemented_count'])}`",
        f"- `Partially implemented`: `{int(total_2026['partially_implemented_count'])}`",
        f"- `Unable to verify`: `{int(total_2026['unable_to_verify_count'])}`",
        f"- `Not implemented`: `{int(total_2026['not_implemented_count'])}`",
        f"- `Superseded or replaced`: `{int(total_2026['superseded_or_replaced_count'])}`",
        f"- `No longer applicable`: `{int(total_2026['no_longer_applicable_count'])}`",
        "",
        "## Follow-up review of the hardest 2026 rows",
        f"- Rows reviewed again: `{len(row_audit)}`",
        f"- Rows moved to `Unable to verify`: `{downgraded}`",
    ]

    (processed_dir / "summary_stats.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
