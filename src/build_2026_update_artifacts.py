"""Build the July 2026 update dataset and derived summary artifacts."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from data_cleaning import project_path, save_csv


UPDATE_STATUS_ORDER = [
    "Implemented",
    "Partially implemented",
    "Unable to verify",
    "Not implemented",
    "Superseded or replaced",
    "No longer applicable",
]

CONFIDENCE_ORDER = ["High", "Medium", "Low"]

STATUS_COLORS = {
    "Implemented": "#1b9e77",
    "Partially implemented": "#66a61e",
    "Unable to verify": "#7570b3",
    "Not implemented": "#d95f02",
    "Superseded or replaced": "#e6ab02",
    "No longer applicable": "#a6761d",
}

CONFIDENCE_COLORS = {
    "High": "#1b9e77",
    "Medium": "#7570b3",
    "Low": "#d95f02",
}

ACCESS_DATE = "2026-07-24"
ACCESS_DATE_LABEL = "July 24, 2026"


def build_source_registry() -> dict[str, dict[str, str]]:
    """Return official public sources used in the 2026 coding pass."""
    return {
        "WHITEHOUSE_AI_GOV": {
            "evidence_url": "https://www.ai.gov/",
            "evidence_title": "AI.Gov | President Trump's AI Strategy and Action Plan",
            "evidence_date": ACCESS_DATE,
            "evidence_source_type": "White House AI portal",
        },
        "M25_21": {
            "evidence_url": "https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-21-Accelerating-Federal-Use-of-AI-through-Innovation-Governance-and-Public-Trust.pdf",
            "evidence_title": "OMB Memorandum M-25-21: Accelerating Federal Use of AI through Innovation, Governance, and Public Trust",
            "evidence_date": "2025-04-03",
            "evidence_source_type": "OMB memorandum PDF",
        },
        "M25_22": {
            "evidence_url": "https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-22-Driving-Efficient-Acquisition-of-Artificial-Intelligence-in-Government.pdf",
            "evidence_title": "OMB Memorandum M-25-22: Driving Efficient Acquisition of Artificial Intelligence in Government",
            "evidence_date": "2025-04-03",
            "evidence_source_type": "OMB memorandum PDF",
        },
        "EO14179": {
            "evidence_url": "https://www.govinfo.gov/app/details/DCPD-202500170",
            "evidence_title": "Executive Order 14179—Removing Barriers to American Leadership in Artificial Intelligence",
            "evidence_date": "2025-01-23",
            "evidence_source_type": "GovInfo executive order",
        },
        "NITRD_AI": {
            "evidence_url": "https://www.nitrd.gov/coordination-areas/ai/",
            "evidence_title": "Artificial Intelligence Research and Development - NITRD Program",
            "evidence_date": ACCESS_DATE,
            "evidence_source_type": "NITRD program page",
        },
        "NITRD_CLOUD_REPORT": {
            "evidence_url": "https://www.nitrd.gov/recommendations-for-leveraging-cloud-computing-resources-for-federally-funded-artificial-intelligence-research-and-development/",
            "evidence_title": "Recommendations for Leveraging Cloud Computing Resources for Federally Funded Artificial Intelligence Research and Development",
            "evidence_date": "2020-11-17",
            "evidence_source_type": "NITRD report page",
        },
        "NIST_STANDARDS_PLAN": {
            "evidence_url": "https://www.nist.gov/artificial-intelligence/plan-federal-engagement-developing-ai-technical-standards-and-related-tools",
            "evidence_title": "A Plan for Federal Engagement in Developing AI Technical Standards and Related Tools in response to Executive Order (EO 13859)",
            "evidence_date": "2022-04-05",
            "evidence_source_type": "NIST standards page",
        },
        "RESOURCES_DATA_GOV": {
            "evidence_url": "https://resources.data.gov",
            "evidence_title": "resources.data.gov",
            "evidence_date": ACCESS_DATE,
            "evidence_source_type": "Federal data guidance portal",
        },
        "FR_DATA_RFI": {
            "evidence_url": "https://www.federalregister.gov/documents/2019/07/10/2019-14618/identifying-priority-access-or-quality-improvements-for-federal-data-and-models-for-artificial",
            "evidence_title": "Identifying Priority Access or Quality Improvements for Federal Data and Models for Artificial Intelligence Research and Development and Testing",
            "evidence_date": "2019-07-10",
            "evidence_source_type": "Federal Register notice",
        },
        "FR_AI_REG_DRAFT": {
            "evidence_url": "https://www.federalregister.gov/documents/2020/01/13/2020-00261/request-for-comments-on-a-draft-memorandum-to-the-heads-of-executive-departments-and-agencies",
            "evidence_title": "Request for Comments on a Draft Memorandum to the Heads of Executive Departments and Agencies, Guidance for Regulation of Artificial Intelligence Applications",
            "evidence_date": "2020-01-13",
            "evidence_source_type": "Federal Register notice",
        },
        "M21_06": {
            "evidence_url": "https://www.whitehouse.gov/wp-content/uploads/2020/11/M-21-06.pdf",
            "evidence_title": "OMB Memorandum M-21-06: Guidance for Regulation of Artificial Intelligence Applications",
            "evidence_date": "2020-11-17",
            "evidence_source_type": "OMB memorandum PDF",
        },
        "GSA_AI": {
            "evidence_url": "https://www.gsa.gov/artificial-intelligence",
            "evidence_title": "Artificial intelligence | GSA",
            "evidence_date": "2026-07-10",
            "evidence_source_type": "Agency AI hub page",
        },
        "GSA_AI_COMPLIANCE": {
            "evidence_url": "https://www.gsa.gov/artificial-intelligence/resources/ai-strategies-and-compliance-plan",
            "evidence_title": "AI strategies and compliance plan | GSA",
            "evidence_date": "2025-09-30",
            "evidence_source_type": "Agency strategy and compliance page",
        },
        "GSA_AI_USE_CASES": {
            "evidence_url": "https://www.gsa.gov/artificial-intelligence/2025-gsa-ai-use-cases",
            "evidence_title": "2025 GSA AI use cases",
            "evidence_date": ACCESS_DATE,
            "evidence_source_type": "Agency AI inventory page",
        },
        "GSA_AI_COP": {
            "evidence_url": "https://www.gsa.gov/artificial-intelligence/ai-community-of-practice",
            "evidence_title": "AI Community of Practice | GSA",
            "evidence_date": "2026-07-20",
            "evidence_source_type": "Cross-agency community page",
        },
        "GSA_PIF_2026": {
            "evidence_url": "https://www.gsa.gov/about-gsa/newsroom/news-releases/gsa-advances-tech-talent-strategy-with-new-presidential-innovation-fellows-class-04232026",
            "evidence_title": "GSA Advances Tech Talent Strategy with New Presidential Innovation Fellows Class",
            "evidence_date": "2026-04-23",
            "evidence_source_type": "GSA news release",
        },
        "DOJ_AI_INVENTORY": {
            "evidence_url": "https://www.justice.gov/ai/ai-inventory",
            "evidence_title": "Department of Justice | AI Inventory",
            "evidence_date": ACCESS_DATE,
            "evidence_source_type": "Agency AI inventory page",
        },
        "DOJ_M24_PLAN": {
            "evidence_url": "https://www.justice.gov/media/1373026/dl",
            "evidence_title": "Department of Justice Compliance Plan for OMB Memorandum M-24-10",
            "evidence_date": "2024-10-01",
            "evidence_source_type": "Agency compliance plan PDF",
        },
        "EPA_AI_INVENTORY": {
            "evidence_url": "https://www.epa.gov/data/ai-use-case-inventory",
            "evidence_title": "AI Use Case Inventory | US EPA",
            "evidence_date": "2026-05-04",
            "evidence_source_type": "Agency AI inventory page",
        },
        "EPA_AI_COMPLIANCE": {
            "evidence_url": "https://www.epa.gov/data/ai-compliance-plan",
            "evidence_title": "AI Compliance Plan | US EPA",
            "evidence_date": "2025-10-30",
            "evidence_source_type": "Agency strategy and compliance page",
        },
        "OPM_AI_GUIDANCE": {
            "evidence_url": "https://www.opm.gov/chcoc/transmittals/2024/The%20Artificial%20Intelligence%20Classification%20Policy%20and%20Talent%20Acquisition%20Guidance%20-%20The%20AI%20in%20Government%20Act%20of%202020.pdf",
            "evidence_title": "The Artificial Intelligence Classification Policy and Talent Acquisition Guidance - The AI in Government Act of 2020",
            "evidence_date": "2024-04-29",
            "evidence_source_type": "OPM guidance PDF",
        },
        "OPM_AI_REVIEW": {
            "evidence_url": "https://www.opm.gov/policy-data-oversight/oversight-and-effectiveness/human-capital-reviews/fy-2024-human-capital-reviews/artificial-intelligence/",
            "evidence_title": "Artificial Intelligence - FY 2024 Human Capital Reviews - OPM",
            "evidence_date": ACCESS_DATE,
            "evidence_source_type": "OPM oversight page",
        },
        "NSPM_AI_NSE": {
            "evidence_url": "https://www.whitehouse.gov/fact-sheets/2026/06/fact-sheet-president-donald-j-trump-signs-historic-directive-on-ai-in-the-national-security-enterprise/",
            "evidence_title": "Fact Sheet: President Donald J. Trump Signs Historic Directive on AI in the National Security Enterprise",
            "evidence_date": "2026-06-05",
            "evidence_source_type": "White House fact sheet",
        },
        "VA_AI": {
            "evidence_url": "https://department.va.gov/ai/",
            "evidence_title": "VA Artificial Intelligence - U.S. Department of Veterans Affairs",
            "evidence_date": ACCESS_DATE,
            "evidence_source_type": "Agency AI hub page",
        },
        "STATE_AI": {
            "evidence_url": "https://www.state.gov/artificial-intelligence",
            "evidence_title": "Artificial Intelligence (AI) - United States Department of State",
            "evidence_date": ACCESS_DATE,
            "evidence_source_type": "Agency AI hub page",
        },
    }


def build_updates() -> dict[str, dict[str, str]]:
    """Return row-level 2026 coding decisions."""
    updates: dict[str, dict[str, str]] = {}
    sources = build_source_registry()

    def add(
        requirement_ids: list[str],
        *,
        updated_2026_status: str,
        source_key: str,
        verification_confidence: str,
        update_notes: str,
        superseded_or_replaced: str = "No",
        replacement_policy_source: str = "",
    ) -> None:
        source = sources[source_key]
        for requirement_id in requirement_ids:
            updates[requirement_id] = {
                "updated_2026_status": updated_2026_status,
                "evidence_url": source["evidence_url"],
                "evidence_title": source["evidence_title"],
                "evidence_date": source["evidence_date"],
                "evidence_source_type": source["evidence_source_type"],
                "verification_confidence": verification_confidence,
                "update_notes": update_notes,
                "superseded_or_replaced": superseded_or_replaced,
                "replacement_policy_source": replacement_policy_source,
            }

    add(
        ["EO13859_4a", "EO13859_4b_i", "EO13859_4b_ii"],
        updated_2026_status="Implemented",
        source_key="NITRD_AI",
        verification_confidence="Medium",
        update_notes=(
            "NITRD continues to publish the Federal AI R&D investments dashboard and ongoing "
            "coordination materials. That is strong public evidence that AI R&D prioritization "
            "and related budget visibility remained in place through July 24, 2026."
        ),
    )
    add(
        ["EO13859_5a_i_rfi"],
        updated_2026_status="Implemented",
        source_key="FR_DATA_RFI",
        verification_confidence="High",
        update_notes=(
            "This time-boxed requirement was completed when OMB published the Federal Register "
            "request for information in July 2019."
        ),
    )
    add(
        ["EO13859_5a_i_barriers"],
        updated_2026_status="Implemented",
        source_key="FR_DATA_RFI",
        verification_confidence="Medium",
        update_notes=(
            "The public RFI and its framing around access and quality barriers remain direct public "
            "evidence that the investigation requirement was carried out."
        ),
    )
    add(
        ["EO13859_5c"],
        updated_2026_status="Implemented",
        source_key="NITRD_CLOUD_REPORT",
        verification_confidence="High",
        update_notes=(
            "The required cloud-computing recommendations report was publicly released. The "
            "requirement is complete."
        ),
    )
    add(
        ["EO13859_6a_b"],
        updated_2026_status="Implemented",
        source_key="M21_06",
        verification_confidence="High",
        update_notes=(
            "OMB issued the required memorandum, and it remains publicly available."
        ),
    )
    add(
        ["EO13859_6d"],
        updated_2026_status="Implemented",
        source_key="NIST_STANDARDS_PLAN",
        verification_confidence="High",
        update_notes=(
            "NIST released the required technical-standards engagement plan. The requirement is complete."
        ),
    )
    add(
        ["EO13960_5a"],
        updated_2026_status="Partially implemented",
        source_key="EPA_AI_INVENTORY",
        verification_confidence="Medium",
        update_notes=(
            "By 2026, agencies are clearly using common inventory/reporting structures and posting "
            "public AI inventory data. That strongly suggests the underlying criteria/format/mechanism "
            "requirement was operationalized, but this pass did not recover a direct public copy of the "
            "original CIO Council artifact itself."
        ),
    )
    add(
        ["EO13960_7a"],
        updated_2026_status="Implemented",
        source_key="GSA_PIF_2026",
        verification_confidence="High",
        update_notes=(
            "The Presidential Innovation Fellows program remains active in 2026 and is publicly "
            "supporting AI-related agency projects."
        ),
    )
    add(
        ["AIGA_103_create_coe"],
        updated_2026_status="Implemented",
        source_key="GSA_AI",
        verification_confidence="High",
        update_notes=(
            "GSA continues to operate a public federal AI hub with USAi, AI use cases, governance, "
            "and acquisition resources, indicating the AI Center of Excellence function remains active."
        ),
    )
    add(
        ["AIGA_104_abd"],
        updated_2026_status="Implemented",
        source_key="M25_21",
        verification_confidence="High",
        update_notes=(
            "By April 3, 2025, OMB issued current government-wide memoranda on Federal AI use and "
            "AI acquisition. Together with M-25-22, this closes the earlier guidance gap identified "
            "in the paper."
        ),
    )
    add(
        ["AIGA_105a"],
        updated_2026_status="Implemented",
        source_key="OPM_AI_GUIDANCE",
        verification_confidence="Medium",
        update_notes=(
            "OPM publicly states that it identified AI competencies, issued classification guidance, "
            "and completed the estimate and workforce forecast components of the AI in Government Act "
            "requirements, although not every downstream artifact is published on the same page."
        ),
    )
    add(
        ["EO13859_2a_e"],
        updated_2026_status="Partially implemented",
        source_key="WHITEHOUSE_AI_GOV",
        verification_confidence="Low",
        update_notes=(
            "The strategic objectives remain visibly active across the federal AI policy ecosystem, "
            "including R&D, education, procurement, and infrastructure initiatives. But this broad, "
            "multi-objective requirement still does not have a single public government-wide outcome "
            "record that would justify coding it as fully implemented."
        ),
    )
    add(
        ["EO13859_5b"],
        updated_2026_status="Partially implemented",
        source_key="NITRD_AI",
        verification_confidence="Medium",
        update_notes=(
            "Public evidence shows continued federal coordination around AI R&D and computing resources, "
            "but this pass does not verify named-agency prioritization decisions one by one."
        ),
    )
    add(
        ["EO13859_7a_i_ii"],
        updated_2026_status="Partially implemented",
        source_key="WHITEHOUSE_AI_GOV",
        verification_confidence="Low",
        update_notes=(
            "Public federal AI education initiatives remain active, but this pass does not verify the "
            "annual communications from each covered grantmaking agency to the NSTC Select Committee."
        ),
    )
    add(
        ["EO13960_2b", "EO13960_4a"],
        updated_2026_status="Partially implemented",
        source_key="M25_21",
        verification_confidence="Medium",
        update_notes=(
            "The current government-wide AI governance memo explicitly operates in concert with "
            "Executive Order 13960 and requires agencies to maintain governance, public trust, "
            "and reporting structures. That is strong evidence that the EO 13960 principles continue "
            "to shape agency practice, but not enough to classify every covered agency as fully compliant."
        ),
    )
    add(
        ["EO13960_5b", "EO13960_5e"],
        updated_2026_status="Partially implemented",
        source_key="DOJ_AI_INVENTORY",
        verification_confidence="Medium",
        update_notes=(
            "By 2026, agencies are clearly conducting and publishing annual AI inventories, but this "
            "pass did not verify every covered agency individually. The coding therefore remains "
            "conservative at partially implemented."
        ),
    )
    add(
        ["EO13960_5c"],
        updated_2026_status="Partially implemented",
        source_key="DOJ_AI_INVENTORY",
        verification_confidence="Medium",
        update_notes=(
            "Public inventory methodology shows agencies are using AI governance review processes to "
            "consolidate and scrutinize use cases, but this pass does not establish full government-wide "
            "completion of review-and-assessment activity."
        ),
    )
    add(
        ["EO13960_6_participation"],
        updated_2026_status="Partially implemented",
        source_key="M25_21",
        verification_confidence="Medium",
        update_notes=(
            "The 2025 memo creates an interagency Chief AI Officer Council to coordinate development "
            "and use of AI across agencies and explicitly advance implementation of the AI principles "
            "from EO 13960."
        ),
    )
    add(
        ["AIGA_103_duties"],
        updated_2026_status="Partially implemented",
        source_key="GSA_AI",
        verification_confidence="Medium",
        update_notes=(
            "GSA publicly operates AI coordination, use-case publication, procurement support, USAi, "
            "and related cross-agency resources. But several statutory duties remain ongoing and are "
            "not fully auditable from public evidence alone."
        ),
    )
    add(
        ["AIGA_104c"],
        updated_2026_status="Partially implemented",
        source_key="GSA_AI_COMPLIANCE",
        verification_confidence="Medium",
        update_notes=(
            "Public agency compliance plans now exist, but this pass did not confirm every covered "
            "agency's public plan or written determination. The conservative coding is partially implemented."
        ),
    )
    add(
        ["EO13859_6c"],
        updated_2026_status="Superseded or replaced",
        source_key="M25_21",
        verification_confidence="Medium",
        update_notes=(
            "The original M-21-06-specific agency planning obligation is no longer the operative public "
            "framework. M-25-21 now requires agencies to submit and publicly post updated compliance plans."
        ),
        superseded_or_replaced="Yes",
        replacement_policy_source="OMB Memorandum M-25-21",
    )
    add(
        ["EO13859_8a_b", "EO13859_8c"],
        updated_2026_status="Superseded or replaced",
        source_key="NSPM_AI_NSE",
        verification_confidence="Medium",
        update_notes=(
            "The original national-security planning framework referenced by EO 13859 has been overtaken "
            "by the June 5, 2026 National Security Presidential Memorandum on AI in the National Security Enterprise."
        ),
        superseded_or_replaced="Yes",
        replacement_policy_source="National Security Presidential Memorandum on AI in the National Security Enterprise (2026-06-05)",
    )
    add(
        ["EO13960_4b"],
        updated_2026_status="Superseded or replaced",
        source_key="M25_21",
        verification_confidence="Medium",
        update_notes=(
            "OMB moved beyond the earlier unfulfilled roadmap requirement and issued current AI use "
            "and acquisition directives with public implementation tables."
        ),
        superseded_or_replaced="Yes",
        replacement_policy_source="OMB Memoranda M-25-21 and M-25-22",
    )
    add(
        ["EO13960_6_cio_list", "EO13960_8c"],
        updated_2026_status="Superseded or replaced",
        source_key="M25_21",
        verification_confidence="Medium",
        update_notes=(
            "The current governance structure centers on designated Chief AI Officers, agency governance "
            "boards, and the OMB-led Chief AI Officer Council rather than the earlier CIO Council structure."
        ),
        superseded_or_replaced="Yes",
        replacement_policy_source="OMB Memorandum M-25-21",
    )

    add(
        [
            "EO13859_4c",
            "EO13859_5a",
            "EO13859_5a_ii",
            "EO13859_5a_iii",
            "EO13859_5a_iv",
            "EO13859_5a_v",
            "EO13859_5d",
            "EO13859_7b",
            "EO13859_7c",
        ],
        updated_2026_status="Unable to verify",
        source_key="RESOURCES_DATA_GOV",
        verification_confidence="Low",
        update_notes=(
            "Public evidence shows some relevant infrastructure and guidance, but this pass did not "
            "find sufficient government-wide documentation to verify completion conservatively."
        ),
    )
    add(
        ["EO13960_4c"],
        updated_2026_status="Unable to verify",
        source_key="M25_21",
        verification_confidence="Low",
        update_notes=(
            "The current federal AI framework references standards and governance, but this pass did not "
            "find enough public evidence to verify government-wide continued use of voluntary consensus "
            "standards in the precise sense required by the original EO 13960 provision."
        ),
    )
    add(
        ["EO13960_5c_i", "EO13960_5c_ii", "EO13960_5d", "EO13960_7b", "EO13960_7c"],
        updated_2026_status="Unable to verify",
        source_key="DOJ_M24_PLAN",
        verification_confidence="Low",
        update_notes=(
            "Agency governance processes clearly exist, but this pass does not verify full government-wide "
            "completion of the specific planning, implementation, sharing, or workforce deliverables tied "
            "to these rows."
        ),
    )
    add(
        ["AIGA_105b"],
        updated_2026_status="Unable to verify",
        source_key="OPM_AI_GUIDANCE",
        verification_confidence="Low",
        update_notes=(
            "Public OPM materials show substantial progress on the broader AI workforce mandate, but this "
            "pass did not locate a public copy of the specific comprehensive plan to Congress required by section 105(b)."
        ),
    )

    return updates


def compute_status_change(original_status: str, updated_status: str) -> str:
    """Compute a readable status-change label."""
    baseline_map = {
        "Implemented": "Implemented",
        "Unknown": "Unable to verify",
        "Not implemented": "Not implemented",
        "Excluded": "Excluded",
    }

    original_mapped = baseline_map.get(original_status, original_status)

    if original_mapped == "Excluded":
        return "Originally excluded; coded in 2026"
    if updated_status == "Superseded or replaced":
        return "Superseded or replaced"
    if updated_status == "No longer applicable":
        return "No longer applicable"
    if updated_status == original_mapped:
        return "No material change"
    if original_mapped == "Unable to verify" and updated_status in {
        "Implemented",
        "Partially implemented",
        "Not implemented",
    }:
        return "Clarified in 2026"
    if original_mapped == "Not implemented" and updated_status in {
        "Implemented",
        "Partially implemented",
    }:
        return "Improved"
    if original_mapped == "Implemented" and updated_status in {
        "Partially implemented",
        "Unable to verify",
        "Not implemented",
    }:
        return "Evidence weaker in 2026"
    return "Changed"


def build_coded_dataframe() -> pd.DataFrame:
    """Merge the preserved baseline with 2026 coding decisions."""
    original_path = project_path("data", "raw", "original_requirements.csv")
    original = pd.read_csv(original_path)
    updates = build_updates()

    rows = []
    for record in original.to_dict(orient="records"):
        requirement_id = record["requirement_id"]
        if requirement_id not in updates:
            raise KeyError(f"Missing 2026 update mapping for {requirement_id}")

        update = updates[requirement_id]
        row = {
            "requirement_id": record["requirement_id"],
            "source_policy": record["source_policy"],
            "requirement_text": record["requirement_text"],
            "responsible_entity": record["responsible_entity"],
            "deadline": record["deadline"],
            "appendix_status": record["appendix_status"],
            "aggregate_status": record["aggregate_status"],
            "aggregate_count_included": record["aggregate_count_included"],
            "updated_2026_status": update["updated_2026_status"],
            "status_change": compute_status_change(
                str(record["aggregate_status"]),
                str(update["updated_2026_status"]),
            ),
            "evidence_url": update["evidence_url"],
            "evidence_title": update["evidence_title"],
            "evidence_date": update["evidence_date"],
            "evidence_source_type": update["evidence_source_type"],
            "verification_confidence": update["verification_confidence"],
            "update_notes": update["update_notes"],
            "superseded_or_replaced": update["superseded_or_replaced"],
            "replacement_policy_source": update["replacement_policy_source"],
        }
        rows.append(row)

    coded = pd.DataFrame(rows)
    invalid_statuses = set(coded["updated_2026_status"]) - set(UPDATE_STATUS_ORDER)
    if invalid_statuses:
        raise ValueError(f"Unexpected 2026 statuses: {sorted(invalid_statuses)}")

    invalid_confidence = set(coded["verification_confidence"]) - set(CONFIDENCE_ORDER)
    if invalid_confidence:
        raise ValueError(f"Unexpected confidence values: {sorted(invalid_confidence)}")

    return coded


def build_2026_summary(coded: pd.DataFrame) -> pd.DataFrame:
    """Build summary tables for the 2026 update."""
    summary_rows: list[dict[str, object]] = []
    policy_order = ["EO 13859", "EO 13960", "AI in Government Act"]

    def add_summary(summary_basis: str, frame: pd.DataFrame, notes: str) -> None:
        for instrument in policy_order:
            subset = frame.loc[frame["source_policy"] == instrument]
            tracker_rows = int((coded["source_policy"] == instrument).sum())
            excluded_count = int(
                (
                    coded.loc[coded["source_policy"] == instrument, "aggregate_count_included"]
                    == "No"
                ).sum()
            )
            counts = subset["updated_2026_status"].value_counts().to_dict()
            total = len(subset)
            row = {
                "summary_basis": summary_basis,
                "instrument": instrument,
                "tracker_rows": tracker_rows,
                "excluded_count": excluded_count,
                "total_requirements": total,
                "notes": notes,
            }
            for status in UPDATE_STATUS_ORDER:
                label = status.lower().replace(" ", "_")
                row[f"{label}_count"] = counts.get(status, 0)
                row[f"{label}_pct"] = round(counts.get(status, 0) / total * 100, 1) if total else 0.0
            summary_rows.append(row)

        tracker_rows = len(coded)
        excluded_count = int((coded["aggregate_count_included"] == "No").sum())
        counts = frame["updated_2026_status"].value_counts().to_dict()
        total = len(frame)
        total_row = {
            "summary_basis": summary_basis,
            "instrument": "Total",
            "tracker_rows": tracker_rows,
            "excluded_count": excluded_count,
            "total_requirements": total,
            "notes": notes,
        }
        for status in UPDATE_STATUS_ORDER:
            label = status.lower().replace(" ", "_")
            total_row[f"{label}_count"] = counts.get(status, 0)
            total_row[f"{label}_pct"] = round(counts.get(status, 0) / total * 100, 1) if total else 0.0
        summary_rows.append(total_row)

    comparable = coded.loc[coded["aggregate_count_included"] == "Yes"].copy()
    add_summary(
        "comparable_baseline_45",
        comparable,
        (
            f"Comparable status summary as of {ACCESS_DATE_LABEL} using the same 45 counted "
            "requirements as the original baseline. The explicitly excluded EO13960 section "
            "5(c)(ii) tracker row is omitted here."
        ),
    )
    add_summary(
        "full_tracker_46",
        coded.copy(),
        f"Full status summary as of {ACCESS_DATE_LABEL} across all 46 appendix tracker rows, including the originally excluded row.",
    )

    return pd.DataFrame(summary_rows)


def set_plot_style() -> None:
    """Apply a clean plotting style."""
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams["figure.figsize"] = (12, 6)
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 11


def save_figure(output_path: Path, figure: plt.Figure) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def plot_2026_status_summary(summary: pd.DataFrame) -> plt.Figure:
    """Plot the 2026 status summary by instrument."""
    set_plot_style()
    figure, axis = plt.subplots()
    plot_frame = summary.loc[
        (summary["summary_basis"] == "comparable_baseline_45")
        & (summary["instrument"] != "Total")
    ].copy()
    instruments = plot_frame["instrument"]
    cumulative = pd.Series(0, index=plot_frame.index, dtype=float)

    for status in UPDATE_STATUS_ORDER:
        col = f"{status.lower().replace(' ', '_')}_pct"
        values = plot_frame[col]
        axis.barh(
            instruments,
            values,
            left=cumulative,
            color=STATUS_COLORS[status],
            label=status,
        )
        cumulative += values

    axis.set_title(f"Status Summary on {ACCESS_DATE_LABEL} by Policy Source")
    axis.set_xlabel("Percent of counted baseline requirements")
    axis.set_xlim(0, 100)
    axis.legend(frameon=False, ncol=3, bbox_to_anchor=(0.5, 1.02), loc="lower center")
    figure.tight_layout()
    return figure


def plot_original_vs_2026_comparison(
    original_summary: pd.DataFrame,
    summary_2026: pd.DataFrame,
) -> plt.Figure:
    """Compare the original counted baseline against the July 2026 counted baseline."""
    set_plot_style()
    figure, axis = plt.subplots()

    original_total = original_summary.loc[
        (original_summary["summary_basis"] == "aggregate_included_rows")
        & (original_summary["instrument"] == "Total")
    ].iloc[0]
    updated_total = summary_2026.loc[
        (summary_2026["summary_basis"] == "comparable_baseline_45")
        & (summary_2026["instrument"] == "Total")
    ].iloc[0]

    comparison = pd.DataFrame(
        [
            {
                "label": "Original baseline (Nov 2022 logic)",
                "Implemented": float(original_total["implemented_pct"]),
                "Partially implemented": 0.0,
                "Unable to verify": float(original_total["unknown_pct"]),
                "Not implemented": float(original_total["not_implemented_pct"]),
                "Superseded or replaced": 0.0,
                "No longer applicable": 0.0,
            },
            {
                "label": "July 24, 2026 update",
                "Implemented": float(updated_total["implemented_pct"]),
                "Partially implemented": float(updated_total["partially_implemented_pct"]),
                "Unable to verify": float(updated_total["unable_to_verify_pct"]),
                "Not implemented": float(updated_total["not_implemented_pct"]),
                "Superseded or replaced": float(updated_total["superseded_or_replaced_pct"]),
                "No longer applicable": float(updated_total["no_longer_applicable_pct"]),
            },
        ]
    )

    cumulative = pd.Series(0, index=comparison.index, dtype=float)
    for status in UPDATE_STATUS_ORDER:
        axis.barh(
            comparison["label"],
            comparison[status],
            left=cumulative,
            color=STATUS_COLORS[status],
            label=status,
        )
        cumulative += comparison[status]

    axis.set_title(f"Original Baseline vs {ACCESS_DATE_LABEL} Update")
    axis.set_xlabel("Percent of counted baseline requirements")
    axis.set_xlim(0, 100)
    axis.legend(frameon=False, ncol=3, bbox_to_anchor=(0.5, 1.02), loc="lower center")
    figure.tight_layout()
    return figure


def plot_status_change_matrix(coded: pd.DataFrame) -> plt.Figure:
    """Plot a matrix of baseline aggregate status versus July 2026 status."""
    set_plot_style()
    comparable = coded.copy()
    baseline_order = ["Implemented", "Unknown", "Not implemented", "Excluded"]
    matrix = pd.crosstab(
        comparable["aggregate_status"],
        comparable["updated_2026_status"],
    ).reindex(index=baseline_order, columns=UPDATE_STATUS_ORDER, fill_value=0)

    figure, axis = plt.subplots(figsize=(11, 6))
    image = axis.imshow(matrix.values, cmap="YlGnBu")
    axis.set_xticks(range(len(matrix.columns)))
    axis.set_xticklabels(matrix.columns, rotation=30, ha="right")
    axis.set_yticks(range(len(matrix.index)))
    axis.set_yticklabels(matrix.index)
    axis.set_title("Status Change Matrix: Original Aggregate Status vs July 2026 Status")

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            axis.text(j, i, matrix.iloc[i, j], ha="center", va="center", color="black")

    figure.colorbar(image, ax=axis, shrink=0.8)
    figure.tight_layout()
    return figure


def plot_verification_confidence(coded: pd.DataFrame) -> plt.Figure:
    """Plot counts by verification confidence."""
    set_plot_style()
    counts = (
        coded["verification_confidence"]
        .value_counts()
        .reindex(CONFIDENCE_ORDER, fill_value=0)
    )
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.bar(
        counts.index,
        counts.values,
        color=[CONFIDENCE_COLORS[level] for level in counts.index],
    )
    axis.set_title("Verification Confidence Across 2026 Coding Decisions")
    axis.set_ylabel("Requirement count")
    figure.tight_layout()
    return figure


def update_source_log() -> None:
    """Append 2026 update sources to the shared source document log if missing."""
    log_path = project_path("data", "raw", "source_documents_log.csv")
    log = pd.read_csv(log_path)

    new_rows = [
        {
            "document_id": "DOC013",
            "document_title": "resources.data.gov",
            "document_type": "guidance portal",
            "issuing_body": "OMB / GSA / OGIS",
            "publication_date": ACCESS_DATE,
            "url": "https://resources.data.gov",
            "relevance_to_project": "2026 update source",
            "notes": "Used conservatively as public evidence of current federal data inventory and guidance infrastructure.",
        },
        {
            "document_id": "DOC014",
            "document_title": "Artificial Intelligence Research and Development - NITRD Program",
            "document_type": "program page",
            "issuing_body": "NITRD",
            "publication_date": ACCESS_DATE,
            "url": "https://www.nitrd.gov/coordination-areas/ai/",
            "relevance_to_project": "2026 update source",
            "notes": "Used for ongoing public evidence of federal AI R&D coordination and investment tracking.",
        },
        {
            "document_id": "DOC015",
            "document_title": "A Plan for Federal Engagement in Developing AI Technical Standards and Related Tools in response to Executive Order (EO 13859)",
            "document_type": "standards plan page",
            "issuing_body": "NIST",
            "publication_date": "2022-04-05",
            "url": "https://www.nist.gov/artificial-intelligence/plan-federal-engagement-developing-ai-technical-standards-and-related-tools",
            "relevance_to_project": "2026 update source",
            "notes": "Used to confirm continued public availability of the technical standards engagement plan.",
        },
        {
            "document_id": "DOC016",
            "document_title": "Artificial intelligence | GSA",
            "document_type": "agency AI hub page",
            "issuing_body": "GSA",
            "publication_date": "2026-07-10",
            "url": "https://www.gsa.gov/artificial-intelligence",
            "relevance_to_project": "2026 update source",
            "notes": "Used for AI CoE continuity, USAi, use cases, and governance resources.",
        },
        {
            "document_id": "DOC017",
            "document_title": "AI strategies and compliance plan | GSA",
            "document_type": "agency strategy and compliance page",
            "issuing_body": "GSA",
            "publication_date": "2025-09-30",
            "url": "https://www.gsa.gov/artificial-intelligence/resources/ai-strategies-and-compliance-plan",
            "relevance_to_project": "2026 update source",
            "notes": "Used as public evidence of posted agency strategy and compliance planning under M-25-21.",
        },
        {
            "document_id": "DOC018",
            "document_title": "AI Community of Practice | GSA",
            "document_type": "community page",
            "issuing_body": "GSA",
            "publication_date": "2026-07-20",
            "url": "https://www.gsa.gov/artificial-intelligence/ai-community-of-practice",
            "relevance_to_project": "2026 update source",
            "notes": "Used as public evidence of cross-agency AI collaboration activity.",
        },
        {
            "document_id": "DOC019",
            "document_title": "GSA Advances Tech Talent Strategy with New Presidential Innovation Fellows Class",
            "document_type": "news release",
            "issuing_body": "GSA",
            "publication_date": "2026-04-23",
            "url": "https://www.gsa.gov/about-gsa/newsroom/news-releases/gsa-advances-tech-talent-strategy-with-new-presidential-innovation-fellows-class-04232026",
            "relevance_to_project": "2026 update source",
            "notes": "Used to confirm active AI-focused Presidential Innovation Fellows work in 2026.",
        },
        {
            "document_id": "DOC020",
            "document_title": "Department of Justice | AI Inventory",
            "document_type": "agency AI inventory page",
            "issuing_body": "Department of Justice",
            "publication_date": ACCESS_DATE,
            "url": "https://www.justice.gov/ai/ai-inventory",
            "relevance_to_project": "2026 update source",
            "notes": "Used as evidence of a current public agency AI inventory and supporting governance process.",
        },
        {
            "document_id": "DOC021",
            "document_title": "AI Use Case Inventory | US EPA",
            "document_type": "agency AI inventory page",
            "issuing_body": "Environmental Protection Agency",
            "publication_date": "2026-05-04",
            "url": "https://www.epa.gov/data/ai-use-case-inventory",
            "relevance_to_project": "2026 update source",
            "notes": "Used as evidence of a current public agency AI inventory and its update cadence.",
        },
        {
            "document_id": "DOC022",
            "document_title": "AI Compliance Plan | US EPA",
            "document_type": "agency compliance page",
            "issuing_body": "Environmental Protection Agency",
            "publication_date": "2025-10-30",
            "url": "https://www.epa.gov/data/ai-compliance-plan",
            "relevance_to_project": "2026 update source",
            "notes": "Used as evidence of public agency strategy and compliance planning.",
        },
        {
            "document_id": "DOC023",
            "document_title": "The Artificial Intelligence Classification Policy and Talent Acquisition Guidance - The AI in Government Act of 2020",
            "document_type": "guidance PDF",
            "issuing_body": "OPM",
            "publication_date": "2024-04-29",
            "url": "https://www.opm.gov/chcoc/transmittals/2024/The%20Artificial%20Intelligence%20Classification%20Policy%20and%20Talent%20Acquisition%20Guidance%20-%20The%20AI%20in%20Government%20Act%20of%202020.pdf",
            "relevance_to_project": "2026 update source",
            "notes": "Used for current public evidence of OPM implementation progress on AI workforce requirements.",
        },
        {
            "document_id": "DOC024",
            "document_title": "Artificial Intelligence - FY 2024 Human Capital Reviews - OPM",
            "document_type": "oversight page",
            "issuing_body": "OPM",
            "publication_date": ACCESS_DATE,
            "url": "https://www.opm.gov/policy-data-oversight/oversight-and-effectiveness/human-capital-reviews/fy-2024-human-capital-reviews/artificial-intelligence/",
            "relevance_to_project": "2026 update source",
            "notes": "Used for public evidence of OPM AI workforce support and follow-on implementation activity.",
        },
        {
            "document_id": "DOC025",
            "document_title": "Fact Sheet: President Donald J. Trump Signs Historic Directive on AI in the National Security Enterprise",
            "document_type": "fact sheet",
            "issuing_body": "The White House",
            "publication_date": "2026-06-05",
            "url": "https://www.whitehouse.gov/fact-sheets/2026/06/fact-sheet-president-donald-j-trump-signs-historic-directive-on-ai-in-the-national-security-enterprise/",
            "relevance_to_project": "2026 update source",
            "notes": "Used as update-context evidence for national-security AI policy replacement logic.",
        },
    ]

    existing_ids = set(log["document_id"].astype(str))
    additions = [row for row in new_rows if row["document_id"] not in existing_ids]
    if additions:
        log = pd.concat([log, pd.DataFrame(additions)], ignore_index=True)
        save_csv(log, log_path)


def main() -> None:
    """Build the 2026 coded dataset, summaries, charts, and source log updates."""
    coded = build_coded_dataframe()
    summary_2026 = build_2026_summary(coded)
    original_summary = pd.read_csv(project_path("data", "processed", "implementation_status_summary.csv"))

    coded_output = project_path("data", "processed", "requirements_coded_2026.csv")
    summary_output = project_path("data", "processed", "implementation_status_summary_2026.csv")
    table_output = project_path("outputs", "tables", "summary_table_2026.csv")
    comparable_output = project_path("outputs", "tables", "requirement_status_table_2026.csv")

    save_csv(coded, coded_output)
    save_csv(summary_2026, summary_output)
    save_csv(summary_2026, table_output)
    save_csv(coded, comparable_output)

    figure_2026 = plot_2026_status_summary(summary_2026)
    save_figure(project_path("outputs", "figures", "implementation_status_2026.png"), figure_2026)

    figure_compare = plot_original_vs_2026_comparison(original_summary, summary_2026)
    save_figure(project_path("outputs", "figures", "original_vs_2026_comparison.png"), figure_compare)

    figure_matrix = plot_status_change_matrix(coded)
    save_figure(project_path("outputs", "figures", "status_change_matrix.png"), figure_matrix)

    figure_confidence = plot_verification_confidence(coded)
    save_figure(project_path("outputs", "figures", "verification_confidence.png"), figure_confidence)

    update_source_log()

    print(f"Wrote {coded_output}")
    print(f"Wrote {summary_output}")
    print(f"Wrote {table_output}")
    print(f"Wrote {comparable_output}")


if __name__ == "__main__":
    main()
