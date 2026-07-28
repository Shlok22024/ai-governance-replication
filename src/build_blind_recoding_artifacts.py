"""Build Phase 1B blind-recoding artifacts for the original 45-row baseline.

This script intentionally treats `data/raw/original_requirements.csv` as a requirement
list only during the initial coding pass. It does not use `appendix_status` or
`aggregate_status` when assigning the independent `replication_status` values.
Those paper-era fields are joined back only after the blind decisions are complete.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from data_cleaning import load_csv, project_path, save_csv


BLIND_STATUS_ORDER = [
    "Implemented",
    "Not implemented",
    "Unknown / Unable to verify",
    "Excluded because deadline had not passed",
]

PAPER_TO_BLIND_STATUS = {
    "Implemented": "Implemented",
    "Not implemented": "Not implemented",
    "Unknown": "Unknown / Unable to verify",
    "Excluded": "Excluded because deadline had not passed",
}

CUTOFF_DATE = "2022-11-15"
CUTOFF_LABEL = "November 15, 2022"


def build_source_registry() -> dict[str, dict[str, str]]:
    """Return official public sources used for the blind recoding pass."""
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


def build_blind_decisions() -> dict[str, dict[str, str]]:
    """Return independent blind-coding decisions keyed by requirement id."""
    decisions: dict[str, dict[str, str]] = {}
    sources = build_source_registry()

    def add(
        requirement_ids: list[str],
        *,
        status: str,
        source_key: str,
        confidence: str,
        notes: str,
    ) -> None:
        source = sources[source_key]
        for requirement_id in requirement_ids:
            decisions[requirement_id] = {
                "replication_status": status,
                "replication_evidence_url": source["url"],
                "replication_evidence_date": source["date"],
                "replication_notes": notes,
                "replication_confidence": confidence,
            }

    add(
        [
            "EO13859_4a",
            "EO13859_4b_i",
            "EO13859_4b_ii",
        ],
        status="Implemented",
        source_key="NAI_RD_2019_PLAN",
        confidence="High",
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
        confidence="High",
        notes=(
            "The required Federal Register request for information was publicly issued within "
            "the required time window."
        ),
    )
    add(
        ["EO13859_5a_i_barriers"],
        status="Implemented",
        source_key="FED_DATA_2020_ACTION_PLAN",
        confidence="Medium",
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
        confidence="High",
        notes=(
            "The required NSTC report on enabling cloud resources for federally funded AI "
            "R&D was publicly issued in November 2020."
        ),
    )
    add(
        ["EO13859_6a_b"],
        status="Implemented",
        source_key="M21_06",
        confidence="High",
        notes=(
            "The original study window included both the public-comment step and the final "
            "OMB memorandum on AI regulatory approaches."
        ),
    )
    add(
        ["EO13859_6d"],
        status="Implemented",
        source_key="NIST_STANDARDS_PLAN",
        confidence="High",
        notes=(
            "NIST publicly released the required plan for federal engagement in AI technical "
            "standards and related tools before the original study cutoff."
        ),
    )
    add(
        ["EO13960_5a"],
        status="Implemented",
        source_key="HHS_AI_INVENTORY_FY22",
        confidence="Medium",
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
        confidence="High",
        notes=(
            "GSA publicly described an AI-emphasis track within the Presidential Innovation "
            "Fellows program and identified AI-focused fellows and projects."
        ),
    )
    add(
        ["AIGA_103_create_coe"],
        status="Implemented",
        source_key="GSA_AI_COE",
        confidence="High",
        notes=(
            "GSA publicly operated an Artificial Intelligence Center of Excellence during the "
            "study period, satisfying the center-creation requirement."
        ),
    )
    add(
        ["EO13960_4b", "EO13960_6_cio_list", "AIGA_104_abd"],
        status="Not implemented",
        source_key="EO13960",
        confidence="Medium",
        notes=(
            "This row required a concrete public posting or guidance deliverable. The blind "
            "recode did not locate a matching public artifact by the study cutoff."
        ),
    )
    add(
        ["AIGA_104_abd"],
        status="Not implemented",
        source_key="AIGA",
        confidence="High",
        notes=(
            "The AI in Government Act required draft and final OMB guidance on acquisition "
            "and use of AI, but no such public memo was located by the study cutoff."
        ),
    )
    add(
        ["AIGA_104c"],
        status="Excluded because deadline had not passed",
        source_key="AIGA",
        confidence="High",
        notes=(
            "This follow-on agency posting requirement depended on issuance of the OMB memo "
            "required in section 104(a), and the blind recode did not treat that triggering "
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
        confidence="Medium",
        notes=(
            "The blind recode treated this as an ongoing, internal, or multi-part obligation "
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
        confidence="Medium",
        notes=(
            "The blind recode treated this as an ongoing, internal, or multi-part obligation "
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
        confidence="Medium",
        notes=(
            "A public FY2022 AI inventory showed that some agencies were publishing use-case "
            "materials, but the blind recode did not infer full completion of the related "
            "follow-on review, sharing, and planning obligations for every responsible agency."
        ),
    )
    add(
        ["EO13859_5b"],
        status="Unknown / Unable to verify",
        source_key="LESSONS_LEARNED_HPC",
        confidence="Medium",
        notes=(
            "Public materials showed progress on AI-related computing access, but the blind "
            "recode did not find requirement-specific public proof that each named agency had "
            "prioritized high-performance computing allocations as directed."
        ),
    )
    add(
        ["EO13960_5b", "EO13960_5e"],
        status="Unknown / Unable to verify",
        source_key="HHS_AI_INVENTORY_FY22",
        confidence="Medium",
        notes=(
            "At least one public FY2022 AI inventory was available, but the blind recode did "
            "not infer whole-of-government completion for every responsible agency from a "
            "single published inventory example."
        ),
    )
    add(
        ["AIGA_103_duties", "AIGA_105a", "AIGA_105b"],
        status="Unknown / Unable to verify",
        source_key="AIGA",
        confidence="Medium",
        notes=(
            "The statute describes concrete duties, but the blind recode did not locate enough "
            "requirement-specific public evidence by the study cutoff to verify the full bundle "
            "conservatively."
        ),
    )

    return decisions


def validate_decisions(
    counted_requirements: pd.DataFrame,
    decisions: dict[str, dict[str, str]],
) -> None:
    """Raise if any counted requirement is missing a blind decision."""
    requirement_ids = counted_requirements["requirement_id"].tolist()
    missing = sorted(set(requirement_ids) - set(decisions))
    extra = sorted(set(decisions) - set(requirement_ids))
    if missing or extra:
        raise ValueError(
            f"Blind recoding decisions mismatch. Missing: {missing}; Extra: {extra}"
        )


def normalize_paper_status(status: str) -> str:
    """Map paper appendix labels onto the blind-recoding label space."""
    return PAPER_TO_BLIND_STATUS.get(str(status), str(status))


def build_discrepancy_reason(row: pd.Series) -> str:
    """Explain why a blind decision disagrees with the appendix status."""
    if row["agreement_with_paper"] == "Agree":
        return ""

    requirement_id = row["requirement_id"]
    blind_status = row["replication_status"]
    paper_status = row["paper_normalized_status"]

    overrides = {
        "EO13859_5b": (
            "The blind recode found public evidence of progress on computing access but not "
            "clear proof that each named agency had prioritized high-performance computing "
            "allocation as the order required."
        ),
        "EO13960_5a": (
            "The blind recode treated the existence of a public FY2022 agency AI inventory as "
            "sufficient evidence that public inventory guidance and a workable mechanism had "
            "been issued."
        ),
        "AIGA_104c": (
            "The blind recode treated this as a follow-on requirement whose deadline had not "
            "yet been triggered because the prerequisite OMB memorandum was not publicly in place."
        ),
    }
    if requirement_id in overrides:
        return overrides[requirement_id]

    if blind_status == "Unknown / Unable to verify" and paper_status == "Implemented":
        return (
            "The blind recode required requirement-specific public proof of completion and did "
            "not upgrade the row from broader or indirect evidence."
        )
    if blind_status == "Unknown / Unable to verify" and paper_status == "Not implemented":
        return (
            "The blind recode treated the absence of a public artifact as insufficient to prove "
            "nonimplementation where the work could have occurred internally."
        )
    if blind_status == "Not implemented":
        return (
            "The blind recode treated this as a missed public deliverable because no matching "
            "public roadmap, list, or memo was located by the study cutoff."
        )
    if blind_status == "Excluded because deadline had not passed":
        return (
            "The blind recode treated the requirement as not yet triggered by the cutoff date."
        )
    if blind_status == "Implemented":
        return (
            "The blind recode treated the located public artifact as direct enough to support "
            "implementation."
        )
    return "The blind recode applied a more conservative public-evidence interpretation."


def build_status_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Aggregate blind-recoding status counts and percentages."""
    total = len(dataframe)
    summary = (
        dataframe["replication_status"]
        .value_counts()
        .reindex(BLIND_STATUS_ORDER, fill_value=0)
        .rename_axis("replication_status")
        .reset_index(name="count")
    )
    summary["percentage"] = (summary["count"] / total * 100).round(1)
    summary["cutoff_date"] = CUTOFF_DATE
    summary["total_requirements"] = total
    return summary


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

    lines = [
        "# Blind Recoding Agreement Rate",
        "",
        f"- Independent blind recoding cutoff: `{CUTOFF_LABEL}`",
        f"- Counted baseline rows reviewed: `{total}`",
        f"- Rows agreeing with paper appendix status: `{agreed}`",
        f"- Rows disagreeing with paper appendix status: `{disagreement_rows}`",
        f"- Agreement rate: `{round(agreed / total * 100, 1)}%`",
    ]
    if disagreement_counts:
        lines.extend(
            [
                "",
                "## Interpretation",
                "",
                "Most disagreements come from the blind pass using a stricter public-evidence rule:",
                "if a requirement was broad, internal, or only partially evidenced, the recode held it at `Unknown / Unable to verify` instead of inferring stronger completion or noncompletion.",
            ]
        )
    return "\n".join(lines) + "\n"


def plot_comparison_heatmap(crosstab: pd.DataFrame, output_path: Path) -> None:
    """Render a heatmap comparing blind recoding to paper appendix statuses."""
    plt.style.use("seaborn-v0_8-whitegrid")
    figure, axis = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        crosstab,
        annot=True,
        fmt="d",
        cmap="Blues",
        linewidths=0.5,
        cbar=False,
        ax=axis,
    )
    axis.set_title(
        "Independent Blind Recode vs Paper Appendix Status\n45 Counted Requirements"
    )
    axis.set_xlabel("Paper appendix status")
    axis.set_ylabel("Blind recoding status")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    """Build blind-recoding outputs from the original requirement list."""
    raw_path = project_path("data", "raw", "original_requirements.csv")
    requirements = load_csv(raw_path)

    counted_requirements = (
        requirements.loc[requirements["aggregate_count_included"] == "Yes"]
        .copy()
        .reset_index(drop=True)
    )
    blind_input = counted_requirements[
        [
            "requirement_id",
            "source_policy",
            "requirement_text",
            "responsible_entity",
            "deadline",
        ]
    ].copy()

    decisions = build_blind_decisions()
    validate_decisions(counted_requirements, decisions)

    blind_rows = pd.DataFrame.from_dict(decisions, orient="index").reset_index()
    blind_rows = blind_rows.rename(columns={"index": "requirement_id"})

    blind_recoding = blind_input.merge(blind_rows, on="requirement_id", how="left")

    paper_columns = counted_requirements[
        ["requirement_id", "appendix_status"]
    ].rename(columns={"appendix_status": "paper_appendix_status"})
    blind_recoding = blind_recoding.merge(paper_columns, on="requirement_id", how="left")
    blind_recoding["paper_normalized_status"] = blind_recoding["paper_appendix_status"].map(
        normalize_paper_status
    )
    blind_recoding["agreement_with_paper"] = blind_recoding.apply(
        lambda row: "Agree"
        if row["replication_status"] == row["paper_normalized_status"]
        else "Disagree",
        axis=1,
    )
    blind_recoding["discrepancy_reason"] = blind_recoding.apply(
        build_discrepancy_reason,
        axis=1,
    )

    output_blind = blind_recoding[
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
            "replication_confidence",
            "paper_appendix_status",
            "agreement_with_paper",
            "discrepancy_reason",
        ]
    ].copy()

    summary = build_status_summary(output_blind)
    crosstab = pd.crosstab(
        output_blind["replication_status"],
        blind_recoding["paper_normalized_status"],
    ).reindex(index=BLIND_STATUS_ORDER, columns=BLIND_STATUS_ORDER, fill_value=0)
    crosstab.index.name = "blind_recoding_status"
    crosstab.columns.name = "paper_appendix_status"

    processed_dir = project_path("data", "processed")
    figures_dir = project_path("outputs", "figures")

    save_csv(output_blind, processed_dir / "original_blind_recoding.csv")
    save_csv(summary, processed_dir / "blind_recoding_status_summary.csv")
    save_csv(crosstab.reset_index(), processed_dir / "blind_recoding_vs_paper_comparison.csv")
    (processed_dir / "blind_recoding_agreement_rate.md").write_text(
        build_agreement_note(output_blind),
        encoding="utf-8",
    )
    plot_comparison_heatmap(
        crosstab,
        figures_dir / "blind_recoding_vs_paper_appendix.png",
    )


if __name__ == "__main__":
    main()
