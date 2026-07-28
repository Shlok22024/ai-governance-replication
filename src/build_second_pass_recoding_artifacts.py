"""Build independent second-pass recoding artifacts for the 45-row baseline.

This script treats `data/raw/original_requirements.csv` as a requirement list only
during the recoding pass. It does not use `appendix_status` or `aggregate_status`
when assigning the independent `replication_status` values. Those paper-era fields
are joined back only after the second-pass decisions are complete.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from data_cleaning import load_csv, project_path, save_csv


SECOND_PASS_STATUS_ORDER = [
    "Implemented",
    "Not implemented",
    "Unknown / Unable to verify",
    "Excluded because deadline had not passed",
]

SECOND_PASS_DISPLAY_LABELS = {
    "Implemented": "Implemented",
    "Not implemented": "Not implemented",
    "Unknown / Unable to verify": "Unclear / unable to verify",
    "Excluded because deadline had not passed": "Excluded (deadline not passed)",
}

PAPER_TO_SECOND_PASS_STATUS = {
    "Implemented": "Implemented",
    "Not implemented": "Not implemented",
    "Unknown": "Unknown / Unable to verify",
    "Excluded": "Excluded because deadline had not passed",
}

CUTOFF_DATE = "2022-11-15"
CUTOFF_LABEL = "November 15, 2022"


def build_source_registry() -> dict[str, dict[str, str]]:
    """Return official public sources used for the second-pass recoding."""
    return {
        "EO13859": {
            "url": "https://www.federalregister.gov/documents/2019/02/14/2019-02544/maintaining-american-leadership-in-artificial-intelligence",
            "title": "Executive Order 13859 - Maintaining American Leadership in Artificial Intelligence",
            "date": "2019-02-14",
        },
        "EO13960": {
            "url": "https://www.federalregister.gov/documents/2020/12/08/2020-27065/promoting-the-use-of-trustworthy-artificial-intelligence-in-the-federal-government",
            "title": "Executive Order 13960 - Promoting the Use of Trustworthy Artificial Intelligence in the Federal Government",
            "date": "2020-12-08",
        },
        "AIGA": {
            "url": "https://www.govinfo.gov/app/details/COMPS-16716",
            "title": "AI in Government Act of 2020",
            "date": "2020-12-27",
        },
        "NAI_RD_2019_PLAN": {
            "url": "https://www.nitrd.gov/pubs/National-AI-RD-Strategy-2019.pdf",
            "title": "The National Artificial Intelligence Research and Development Strategic Plan: 2019 Update",
            "date": "2019-06-21",
        },
        "YEAR_ONE_REPORT": {
            "url": "https://www.nitrd.gov/nitrdgroups/images/c/c1/American-AI-Initiative-One-Year-Annual-Report.pdf",
            "title": "American Artificial Intelligence Initiative: Year One Annual Report",
            "date": "2020-02",
        },
        "FR_DATA_RFI": {
            "url": "https://www.federalregister.gov/documents/2019/07/10/2019-14618/identifying-priority-access-or-quality-improvements-for-federal-data-and-models-for-artificial",
            "title": "Identifying Priority Access or Quality Improvements for Federal Data and Models for Artificial Intelligence Research and Development and Testing",
            "date": "2019-07-10",
        },
        "FED_DATA_2020_ACTION_PLAN": {
            "url": "https://strategy.data.gov/assets/docs/2020-federal-data-strategy-action-plan.pdf",
            "title": "Federal Data Strategy 2020 Action Plan",
            "date": "2019-12-23",
        },
        "CLOUD_REPORT": {
            "url": "https://www.nitrd.gov/pubs/Recommendations-Cloud-AI-RD-Nov2020.pdf",
            "title": "Recommendations for Leveraging Cloud Computing Resources for Federally Funded Artificial Intelligence Research and Development",
            "date": "2020-11-17",
        },
        "M21_06": {
            "url": "https://www.whitehouse.gov/wp-content/uploads/2020/11/M-21-06.pdf",
            "title": "OMB Memorandum M-21-06: Guidance for Regulation of Artificial Intelligence Applications",
            "date": "2020-11-17",
        },
        "NIST_STANDARDS_PLAN": {
            "url": "https://www.nist.gov/artificial-intelligence/plan-federal-engagement-developing-ai-technical-standards-and-related-tools",
            "title": "A Plan for Federal Engagement in Developing AI Technical Standards and Related Tools in response to Executive Order (EO 13859)",
            "date": "2022-04-05",
        },
        "HHS_AI_INVENTORY_FY22": {
            "url": "https://www.hhs.gov/sites/default/files/hhs-ai-use-cases-inventory.pdf",
            "title": "Department of Health and Human Services Artificial Intelligence Use Cases - FY2022",
            "date": "FY2022 inventory (public by November 2022)",
        },
        "PIF_2021": {
            "url": "https://www.gsa.gov/blog/2020/10/19/passion-and-purpose-meet-the-2021-presidential-innovation-fellows",
            "title": "Passion and Purpose: Meet the 2021 Presidential Innovation Fellows",
            "date": "2020-10-19",
        },
        "PIF_10_YEARS": {
            "url": "https://www.gsa.gov/blog/2022/09/23/10-years-of-the-presidential-innovation-fellows-program",
            "title": "10 Years of the Presidential Innovation Fellows Program",
            "date": "2022-09-23",
        },
        "GSA_AI_COE": {
            "url": "https://coe.gsa.gov/2020/03/17/ai-update-1.html",
            "title": "How to Avoid the Red Queen Effect",
            "date": "2020-03-17",
        },
        "GSA_AI_COE_PAGE": {
            "url": "https://coe.gsa.gov/coe/artificial-intelligence.html",
            "title": "Artificial Intelligence | GSA - IT Modernization Centers of Excellence",
            "date": "2022-04-20",
        },
        "LESSONS_LEARNED_HPC": {
            "url": "https://www.nitrd.gov/pubs/Lessons-Learned-Cloud-for-AI-July2022.pdf",
            "title": "Lessons Learned from Federal Use of Cloud Computing To Support Artificial Intelligence Research and Development",
            "date": "2022-07",
        },
    }


def build_second_pass_decisions() -> dict[str, dict[str, str]]:
    """Return independent second-pass coding decisions keyed by requirement id."""
    decisions: dict[str, dict[str, str]] = {}
    sources = build_source_registry()

    def add(
        requirement_ids: list[str],
        *,
        status: str,
        source_key: str,
        notes: str,
    ) -> None:
        source = sources[source_key]
        for requirement_id in requirement_ids:
            decisions[requirement_id] = {
                "replication_status": status,
                "replication_evidence_url": source["url"],
                "replication_evidence_date": source["date"],
                "replication_notes": notes,
            }

    add(
        [
            "EO13859_4a",
            "EO13859_4b_i",
            "EO13859_4b_ii",
        ],
        status="Implemented",
        source_key="NAI_RD_2019_PLAN",
        notes=(
            "Public planning and investment documents available before the study cutoff show "
            "that AI R&D had been elevated as a budget and planning priority and was being "
            "tracked through the NITRD process."
        ),
    )
    add(
        ["EO13859_5a_i_rfi"],
        status="Implemented",
        source_key="FR_DATA_RFI",
        notes=(
            "The required Federal Register request for information was publicly issued within "
            "the required time window."
        ),
    )
    add(
        ["EO13859_5a_i_barriers"],
        status="Implemented",
        source_key="FED_DATA_2020_ACTION_PLAN",
        notes=(
            "The Federal Data Strategy action-plan materials publicly tracked the AI data "
            "and model access workstream, which supports a conservative implementation call "
            "for the barrier-investigation step."
        ),
    )
    add(
        ["EO13859_5c"],
        status="Implemented",
        source_key="CLOUD_REPORT",
        notes=(
            "The required NSTC report on enabling cloud resources for federally funded AI "
            "R&D was publicly issued in November 2020."
        ),
    )
    add(
        ["EO13859_6a_b"],
        status="Implemented",
        source_key="M21_06",
        notes=(
            "The original study window included both the public-comment step and the final "
            "OMB memorandum on AI regulatory approaches."
        ),
    )
    add(
        ["EO13859_6d"],
        status="Implemented",
        source_key="NIST_STANDARDS_PLAN",
        notes=(
            "NIST publicly released the required plan for federal engagement in AI technical "
            "standards and related tools before the original study cutoff."
        ),
    )
    add(
        ["EO13960_5a"],
        status="Implemented",
        source_key="HHS_AI_INVENTORY_FY22",
        notes=(
            "A public FY2022 agency AI inventory was available during the study period, which "
            "supports the inference that the CIO Council had issued publicly usable inventory "
            "criteria, format, and mechanisms."
        ),
    )
    add(
        ["EO13960_7a"],
        status="Implemented",
        source_key="PIF_2021",
        notes=(
            "GSA publicly described an AI-emphasis track within the Presidential Innovation "
            "Fellows program and identified AI-focused fellows and projects."
        ),
    )
    add(
        ["AIGA_103_create_coe"],
        status="Implemented",
        source_key="GSA_AI_COE",
        notes=(
            "GSA publicly operated an Artificial Intelligence Center of Excellence during the "
            "study period, satisfying the center-creation requirement."
        ),
    )
    add(
        ["EO13960_4b", "EO13960_6_cio_list", "AIGA_104_abd"],
        status="Not implemented",
        source_key="EO13960",
        notes=(
            "This row required a concrete public posting or guidance deliverable. The second-pass "
            "recode did not locate a matching public artifact by the study cutoff."
        ),
    )
    add(
        ["AIGA_104_abd"],
        status="Not implemented",
        source_key="AIGA",
        notes=(
            "The AI in Government Act required draft and final OMB guidance on acquisition "
            "and use of AI, but no such public memo was located by the study cutoff."
        ),
    )
    add(
        ["AIGA_104c"],
        status="Excluded because deadline had not passed",
        source_key="AIGA",
        notes=(
            "This follow-on agency posting requirement depended on issuance of the OMB memo "
            "required in section 104(a), and the second-pass recoding did not treat that triggering "
            "memo as completed by the study cutoff."
        ),
    )
    add(
        [
            "EO13859_2a_e",
            "EO13859_4c",
            "EO13859_5a",
            "EO13859_5a_ii",
            "EO13859_5a_iii",
            "EO13859_5a_iv",
            "EO13859_5a_v",
            "EO13859_5d",
            "EO13859_6c",
            "EO13859_7a_i_ii",
            "EO13859_7b",
            "EO13859_7c",
            "EO13859_8a_b",
            "EO13859_8c",
        ],
        status="Unknown / Unable to verify",
        source_key="EO13859",
        notes=(
            "The second-pass recoding treated this as an ongoing, internal, or multi-part obligation "
            "for which public evidence before the study cutoff was not specific enough to "
            "verify completion conservatively."
        ),
    )
    add(
        [
            "EO13960_2b",
            "EO13960_4a",
            "EO13960_4c",
            "EO13960_6_participation",
            "EO13960_7b",
            "EO13960_7c",
            "EO13960_8c",
        ],
        status="Unknown / Unable to verify",
        source_key="EO13960",
        notes=(
            "The second-pass recoding treated this as an ongoing, internal, or multi-part obligation "
            "for which public evidence before the study cutoff was not specific enough to "
            "verify completion conservatively."
        ),
    )
    add(
        [
            "EO13960_5c",
            "EO13960_5c_i",
            "EO13960_5d",
        ],
        status="Unknown / Unable to verify",
        source_key="HHS_AI_INVENTORY_FY22",
        notes=(
            "A public FY2022 AI inventory showed that some agencies were publishing use-case "
            "materials, but the second-pass recoding did not infer full completion of the related "
            "follow-on review, sharing, and planning obligations for every responsible agency."
        ),
    )
    add(
        ["EO13859_5b"],
        status="Unknown / Unable to verify",
        source_key="LESSONS_LEARNED_HPC",
        notes=(
            "Public materials showed progress on AI-related computing access, but the second-pass "
            "recode did not find requirement-specific public proof that each named agency had "
            "prioritized high-performance computing allocations as directed."
        ),
    )
    add(
        ["EO13960_5b", "EO13960_5e"],
        status="Unknown / Unable to verify",
        source_key="HHS_AI_INVENTORY_FY22",
        notes=(
            "At least one public FY2022 AI inventory was available, but the second-pass recoding did "
            "not infer whole-of-government completion for every responsible agency from a "
            "single published inventory example."
        ),
    )
    add(
        ["AIGA_103_duties", "AIGA_105a", "AIGA_105b"],
        status="Unknown / Unable to verify",
        source_key="AIGA",
        notes=(
            "The statute describes concrete duties, but the second-pass recoding did not locate enough "
            "requirement-specific public evidence by the study cutoff to verify the full bundle "
            "conservatively."
        ),
    )

    return decisions


def validate_decisions(
    counted_requirements: pd.DataFrame,
    decisions: dict[str, dict[str, str]],
) -> None:
    """Raise if any counted requirement is missing a second-pass decision."""
    requirement_ids = counted_requirements["requirement_id"].tolist()
    missing = sorted(set(requirement_ids) - set(decisions))
    extra = sorted(set(decisions) - set(requirement_ids))
    if missing or extra:
        raise ValueError(
            f"Second-pass recoding decisions mismatch. Missing: {missing}; Extra: {extra}"
        )


def normalize_paper_status(status: str) -> str:
    """Map paper appendix labels onto the second-pass label space."""
    return PAPER_TO_SECOND_PASS_STATUS.get(str(status), str(status))


def build_discrepancy_reason(row: pd.Series) -> str:
    """Explain why a second-pass decision disagrees with the appendix status."""
    if row["agreement_with_paper"] == "Agree":
        return ""

    requirement_id = row["requirement_id"]
    second_pass_status = row["replication_status"]
    paper_status = row["paper_normalized_status"]

    overrides = {
        "EO13859_5b": (
            "The second-pass recoding found public evidence of progress on computing access but not "
            "clear proof that each named agency had prioritized high-performance computing "
            "allocation as the order required."
        ),
        "EO13960_5a": (
            "The second-pass recoding treated the existence of a public FY2022 agency AI inventory as "
            "sufficient evidence that public inventory guidance and a workable mechanism had "
            "been issued."
        ),
        "AIGA_104c": (
            "The second-pass recoding treated this as a follow-on requirement whose deadline had not "
            "yet been triggered because the prerequisite OMB memorandum was not publicly in place."
        ),
    }
    if requirement_id in overrides:
        return overrides[requirement_id]

    if second_pass_status == "Unknown / Unable to verify" and paper_status == "Implemented":
        return (
            "The second-pass recoding required requirement-specific public proof of completion and did "
            "not upgrade the row from broader or indirect evidence."
        )
    if second_pass_status == "Unknown / Unable to verify" and paper_status == "Not implemented":
        return (
            "The second-pass recoding treated the absence of a public artifact as insufficient to prove "
            "nonimplementation where the work could have occurred internally."
        )
    if second_pass_status == "Not implemented":
        return (
            "The second-pass recoding treated this as a missed public deliverable because no matching "
            "public roadmap, list, or memo was located by the study cutoff."
        )
    if second_pass_status == "Excluded because deadline had not passed":
        return (
            "The second-pass recoding treated the requirement as not yet triggered by the cutoff date."
        )
    if second_pass_status == "Implemented":
        return (
            "The second-pass recoding treated the located public artifact as direct enough to support "
            "implementation."
        )
    return "The second-pass recoding applied a more conservative public-evidence interpretation."


def build_status_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Aggregate second-pass recoding status counts and percentages."""
    total = len(dataframe)
    summary = (
        dataframe["replication_status"]
        .value_counts()
        .reindex(SECOND_PASS_STATUS_ORDER, fill_value=0)
        .rename_axis("replication_status")
        .reset_index(name="count")
    )
    summary["percentage"] = (summary["count"] / total * 100).round(1)
    summary["cutoff_date"] = CUTOFF_DATE
    summary["total_requirements"] = total
    return summary


def compute_cohens_kappa(dataframe: pd.DataFrame) -> float:
    """Compute Cohen's kappa for second-pass agreement against the paper appendix."""
    labels = SECOND_PASS_STATUS_ORDER
    total = len(dataframe)
    paper_normalized = dataframe["paper_appendix_status"].map(normalize_paper_status)
    observed = (dataframe["replication_status"] == paper_normalized).mean()
    second_pass_share = (
        dataframe["replication_status"].value_counts().reindex(labels, fill_value=0) / total
    )
    paper_share = paper_normalized.value_counts().reindex(labels, fill_value=0) / total
    expected = float((second_pass_share * paper_share).sum())
    return (observed - expected) / (1 - expected)


def build_agreement_note(dataframe: pd.DataFrame) -> str:
    """Return a short Markdown agreement summary."""
    total = len(dataframe)
    agreed = int((dataframe["agreement_with_paper"] == "Agree").sum())
    disagreement_counts = (
        dataframe.loc[dataframe["agreement_with_paper"] == "Disagree", "discrepancy_reason"]
        .value_counts()
        .tolist()
    )
    disagreement_rows = int((dataframe["agreement_with_paper"] == "Disagree").sum())
    kappa = compute_cohens_kappa(dataframe)

    lines = [
        "# My Second Check vs the Paper",
        "",
        f"- Date used for the second check: `{CUTOFF_LABEL}`",
        f"- Rows reviewed: `{total}`",
        f"- Rows where my answer matched the paper: `{agreed}`",
        f"- Rows where my answer differed: `{disagreement_rows}`",
        f"- Agreement rate: `{round(agreed / total * 100, 1)}%`",
        f"- Cohen's kappa: `{round(kappa, 2)}`",
    ]
    if disagreement_counts:
        lines.extend(
            [
                "",
                "## What this means",
                "",
                "A simple way to think about this is two people grading the same checklist and then comparing answers.",
                "Most differences came from using a stricter evidence rule. If a requirement was broad, internal, or only partly supported by public records, I treated it as `Unknown / Unable to verify` instead of making a stronger claim.",
            ]
        )
    return "\n".join(lines) + "\n"


def plot_comparison_heatmap(crosstab: pd.DataFrame, output_path: Path) -> None:
    """Render a heatmap comparing second-pass recoding to paper appendix statuses."""
    plt.style.use("seaborn-v0_8-whitegrid")
    figure, axis = plt.subplots(figsize=(11.5, 5.3))
    sns.heatmap(
        crosstab,
        annot=True,
        fmt="d",
        cmap="Blues",
        linewidths=0.5,
        cbar=False,
        ax=axis,
    )
    axis.set_title("My Second Check vs the Paper\n45 Requirements")
    axis.set_xlabel("Paper's answer")
    axis.set_ylabel("My answer")
    axis.set_xticklabels(
        [SECOND_PASS_DISPLAY_LABELS.get(label, label) for label in crosstab.columns],
        rotation=0,
        ha="center",
    )
    axis.set_yticklabels(
        [SECOND_PASS_DISPLAY_LABELS.get(label, label) for label in crosstab.index],
        rotation=0,
        va="center",
    )
    axis.tick_params(axis="x", pad=6)
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    """Build second-pass recoding outputs from the original requirement list."""
    raw_path = project_path("data", "raw", "original_requirements.csv")
    requirements = load_csv(raw_path)

    counted_requirements = (
        requirements.loc[requirements["aggregate_count_included"] == "Yes"]
        .copy()
        .reset_index(drop=True)
    )
    second_pass_input = counted_requirements[
        [
            "requirement_id",
            "source_policy",
            "requirement_text",
            "responsible_entity",
            "deadline",
        ]
    ].copy()

    decisions = build_second_pass_decisions()
    validate_decisions(counted_requirements, decisions)

    second_pass_rows = pd.DataFrame.from_dict(decisions, orient="index").reset_index()
    second_pass_rows = second_pass_rows.rename(columns={"index": "requirement_id"})

    second_pass_recoding = second_pass_input.merge(second_pass_rows, on="requirement_id", how="left")

    paper_columns = counted_requirements[
        ["requirement_id", "appendix_status"]
    ].rename(columns={"appendix_status": "paper_appendix_status"})
    second_pass_recoding = second_pass_recoding.merge(paper_columns, on="requirement_id", how="left")
    second_pass_recoding["paper_normalized_status"] = second_pass_recoding["paper_appendix_status"].map(
        normalize_paper_status
    )
    second_pass_recoding["agreement_with_paper"] = second_pass_recoding.apply(
        lambda row: "Agree"
        if row["replication_status"] == row["paper_normalized_status"]
        else "Disagree",
        axis=1,
    )
    second_pass_recoding["discrepancy_reason"] = second_pass_recoding.apply(
        build_discrepancy_reason,
        axis=1,
    )

    output_second_pass = second_pass_recoding[
        [
            "requirement_id",
            "source_policy",
            "requirement_text",
            "responsible_entity",
            "deadline",
            "replication_status",
            "replication_evidence_url",
            "replication_evidence_date",
            "replication_notes",
            "paper_appendix_status",
            "agreement_with_paper",
            "discrepancy_reason",
        ]
    ].copy()

    summary = build_status_summary(output_second_pass)
    crosstab = pd.crosstab(
        output_second_pass["replication_status"],
        second_pass_recoding["paper_normalized_status"],
    ).reindex(index=SECOND_PASS_STATUS_ORDER, columns=SECOND_PASS_STATUS_ORDER, fill_value=0)
    crosstab.index.name = "second_pass_recoding_status"
    crosstab.columns.name = "paper_appendix_status"

    processed_dir = project_path("data", "processed")
    figures_dir = project_path("outputs", "figures")

    save_csv(output_second_pass, processed_dir / "original_second_pass_recoding.csv")
    save_csv(summary, processed_dir / "second_pass_recoding_status_summary.csv")
    save_csv(crosstab.reset_index(), processed_dir / "second_pass_recoding_vs_paper_comparison.csv")
    (processed_dir / "second_pass_recoding_agreement_rate.md").write_text(
        build_agreement_note(output_second_pass),
        encoding="utf-8",
    )
    plot_comparison_heatmap(
        crosstab,
        figures_dir / "second_pass_recoding_vs_paper_appendix.png",
    )


if __name__ == "__main__":
    main()
