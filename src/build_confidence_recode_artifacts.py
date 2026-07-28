"""Build the evidence-quality confidence redesign artifacts for the 2026 update layer."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from confidence_rules import (
    apply_confidence_index,
    check_collinearity,
    sources_checked_from_log,
    validate_values,
)
from data_cleaning import project_path, save_csv


CHECK_DATE = "2026-07-28"
SEARCH_RESULTS = [
    "Supports",
    "Partial support",
    "Context only",
    "No evidence",
    "Dead link",
    "Not relevant",
]
STATUS_ORDER = [
    "Implemented",
    "Partially implemented",
    "Unable to verify",
    "Not implemented",
    "Superseded or replaced",
    "No longer applicable",
]
SCOPE_ORDER = ["Exhaustive", "Targeted", "Cursory", "Not searched", "Not recorded"]
CONFIDENCE_ORDER = ["High", "Medium", "Low"]
SEARCH_SCOPE_COLORS = {
    "Exhaustive": "#1b9e77",
    "Targeted": "#7570b3",
    "Cursory": "#d95f02",
    "Not searched": "#e6ab02",
    "Not recorded": "#666666",
}
CONFIDENCE_COLORS = {
    "High": "#1b9e77",
    "Medium": "#7570b3",
    "Low": "#d95f02",
}


def build_search_source_registry() -> dict[str, dict[str, str]]:
    """Return the curated official source registry used in the confidence pass."""
    return {
        "AI_GOV": {
            "url": "https://www.ai.gov/",
            "source_title": "AI.Gov | President Trump's AI Strategy and Action Plan",
        },
        "AI_GOV_INVENTORIES_DEAD": {
            "url": "https://www.ai.gov/ai-use-case-inventories/",
            "source_title": "AI Use Case Inventories | AI.Gov",
        },
        "RESOURCES_HOME": {
            "url": "https://resources.data.gov/",
            "source_title": "Home | resources.data.gov",
        },
        "DCAT_PRIORITIES": {
            "url": "https://resources.data.gov/resources/dcat-us-priorities/",
            "source_title": "Improving Discoverability, Usability and Governance of Priority Data and Models in AI Research and Development",
        },
        "NITRD_AI": {
            "url": "https://www.nitrd.gov/coordination-areas/ai/",
            "source_title": "Artificial Intelligence Research and Development - NITRD.gov",
        },
        "NITRD_PROGRESS_PDF": {
            "url": "https://www.nitrd.gov/pubs/AI-Research-and-Development-Progress-Report-2020-2024.pdf",
            "source_title": "2020-2024 Progress Report: Advancing Trustworthy Artificial Intelligence Research and Development",
        },
        "NITRD_CLOUD_REPORT": {
            "url": "https://www.nitrd.gov/recommendations-for-leveraging-cloud-computing-resources-for-federally-funded-artificial-intelligence-research-and-development/",
            "source_title": "Recommendations for Leveraging Cloud Computing Resources for Federally Funded Artificial Intelligence Research and Development",
        },
        "FR_DATA_RFI": {
            "url": "https://www.federalregister.gov/documents/2019/07/10/2019-14618/identifying-priority-access-or-quality-improvements-for-federal-data-and-models-for-artificial",
            "source_title": "Identifying Priority Access or Quality Improvements for Federal Data and Models for Artificial Intelligence Research and Development and Testing",
        },
        "FED_DATA_ACTION_PLAN": {
            "url": "https://strategy.data.gov/assets/docs/2020-federal-data-strategy-action-plan.pdf",
            "source_title": "Federal Data Strategy 2020 Action Plan",
        },
        "M21_06": {
            "url": "https://www.whitehouse.gov/wp-content/uploads/2020/11/M-21-06.pdf",
            "source_title": "OMB Memorandum M-21-06: Guidance for Regulation of Artificial Intelligence Applications",
        },
        "FR_AI_REG_DRAFT": {
            "url": "https://www.federalregister.gov/documents/2020/01/13/2020-00261/request-for-comments-on-a-draft-memorandum-to-the-heads-of-executive-departments-and-agencies",
            "source_title": "Request for Comments on a Draft Memorandum to the Heads of Executive Departments and Agencies, Guidance for Regulation of Artificial Intelligence Applications",
        },
        "NIST_PLAN_PAGE": {
            "url": "https://www.nist.gov/artificial-intelligence/plan-federal-engagement-developing-ai-technical-standards-and-related-tools",
            "source_title": "A Plan for Federal Engagement in Developing AI Technical Standards and Related Tools in response to Executive Order (EO 13859)",
        },
        "NIST_PLAN_PDF": {
            "url": "https://www.nist.gov/document/report-plan-federal-engagement-developing-technical-standards-and-related-tools",
            "source_title": "A Plan for Federal Engagement in Developing AI Technical Standards and Related Tools (PDF)",
        },
        "GSA_AI": {
            "url": "https://www.gsa.gov/artificial-intelligence",
            "source_title": "Artificial intelligence - GSA",
        },
        "GSA_AI_RESOURCES": {
            "url": "https://www.gsa.gov/artificial-intelligence/resources",
            "source_title": "Resources - GSA",
        },
        "GSA_AI_COP": {
            "url": "https://www.gsa.gov/artificial-intelligence/ai-community-of-practice",
            "source_title": "AI Community of Practice | GSA",
        },
        "GSA_AI_GOVERNANCE": {
            "url": "https://www.gsa.gov/artificial-intelligence/resources/ai-governance",
            "source_title": "AI governance - GSA",
        },
        "GSA_AI_COMPLIANCE": {
            "url": "https://www.gsa.gov/artificial-intelligence/resources/ai-strategies-and-compliance-plan",
            "source_title": "AI strategies and compliance plan - GSA",
        },
        "GSA_AI_USE_CASES": {
            "url": "https://www.gsa.gov/artificial-intelligence/2025-gsa-ai-use-cases",
            "source_title": "2025 GSA AI use cases",
        },
        "GSA_PIF_2026": {
            "url": "https://www.gsa.gov/about-gsa/newsroom/news-releases/gsa-advances-tech-talent-strategy-with-new-presidential-innovation-fellows-class-04232026",
            "source_title": "GSA Advances Tech Talent Strategy with New Presidential Innovation Fellows Class",
        },
        "GSA_AI_TRAINING": {
            "url": "https://coe.gsa.gov/communities/AITraining.html",
            "source_title": "AI Training Series for Government Employees | GSA",
        },
        "M25_21": {
            "url": "https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-21-Accelerating-Federal-Use-of-AI-through-Innovation-Governance-and-Public-Trust.pdf",
            "source_title": "OMB Memorandum M-25-21: Accelerating Federal Use of AI through Innovation, Governance, and Public Trust",
        },
        "M25_22": {
            "url": "https://www.whitehouse.gov/wp-content/uploads/2025/02/M-25-22-Driving-Efficient-Acquisition-of-Artificial-Intelligence-in-Government.pdf",
            "source_title": "OMB Memorandum M-25-22: Driving Efficient Acquisition of Artificial Intelligence in Government",
        },
        "EO14179": {
            "url": "https://www.govinfo.gov/app/details/DCPD-202500170",
            "source_title": "Executive Order 14179 - Removing Barriers to American Leadership in Artificial Intelligence",
        },
        "WHITEHOUSE_NS_DIR": {
            "url": "https://www.whitehouse.gov/fact-sheets/2026/06/fact-sheet-president-donald-j-trump-signs-historic-directive-on-ai-in-the-national-security-enterprise/",
            "source_title": "Fact Sheet: President Donald J. Trump Signs Historic Directive on AI in the National Security Enterprise",
        },
        "DOJ_AI": {
            "url": "https://www.justice.gov/ai",
            "source_title": "Artificial Intelligence | United States Department of Justice",
        },
        "DOJ_AI_INVENTORY": {
            "url": "https://www.justice.gov/ai/ai-inventory",
            "source_title": "AI Inventory - Department of Justice",
        },
        "DOJ_M24_PLAN": {
            "url": "https://www.justice.gov/media/1373026/dl",
            "source_title": "Compliance Plan for OMB Memorandum M-24-10",
        },
        "DOJ_IT_PLAN": {
            "url": "https://www.justice.gov/d9/fieldable-panel-panes/basic-panes/attachments/2022/06/09/doj_it_strategic_plan_2022-2024.pdf",
            "source_title": "DOJ IT Strategic Plan 2022-2024",
        },
        "EPA_AI_INVENTORY": {
            "url": "https://www.epa.gov/data/ai-use-case-inventory",
            "source_title": "AI Use Case Inventory | US EPA",
        },
        "EPA_AI_COMPLIANCE": {
            "url": "https://www.epa.gov/data/ai-compliance-plan",
            "source_title": "AI Compliance Plan | US EPA",
        },
        "HHS_AI_USE_CASES": {
            "url": "https://www.hhs.gov/programs/topic-sites/ai/use-cases/index.html",
            "source_title": "Artificial intelligence use cases | HHS",
        },
        "CIO_HOME": {
            "url": "https://www.cio.gov/",
            "source_title": "About CIOC - Councils.gov",
        },
        "CIO_INVENTORY_REFERENCE_DEAD": {
            "url": "https://www.cio.gov/policies-and-priorities/Executive-Order-13960-AI-Use-Case-Inventories-Reference/",
            "source_title": "Executive Order 13960 AI Use Case Inventories Reference",
        },
        "CIO_INVENTORY_GUIDANCE_DEAD": {
            "url": "https://www.cio.gov/assets/resources/2021%20Guidance%20for%20Creating%20Agency%20Inventories%20of%20AI%20Use%20Cases%2010.06.2021.docx",
            "source_title": "2021 Guidance for Creating Agency Inventories of AI Use Cases",
        },
        "OPM_AI_GUIDANCE": {
            "url": "https://www.opm.gov/chcoc/transmittals/2024/The%20Artificial%20Intelligence%20Classification%20Policy%20and%20Talent%20Acquisition%20Guidance%20-%20The%20AI%20in%20Government%20Act%20of%202020.pdf",
            "source_title": "The Artificial Intelligence Classification Policy and Talent Acquisition Guidance - The AI in Government Act of 2020",
        },
        "OPM_AI_REVIEW": {
            "url": "https://www.opm.gov/policy-data-oversight/oversight-and-effectiveness/human-capital-reviews/fy-2024-human-capital-reviews/artificial-intelligence/",
            "source_title": "Artificial Intelligence - FY 2024 Human Capital Reviews - OPM",
        },
        "OPM_AI_WORKFORCE_FUTURE": {
            "url": "https://www.opm.gov/chcoc/latest-memos/building-the-ai-workforce-of-the-future.pdf",
            "source_title": "Building the AI Workforce of the Future - OPM",
        },
        "OPM_PUBLISHED_MEMOS": {
            "url": "https://www.opm.gov/chcoc/published-memos/",
            "source_title": "OPM Published Memos",
        },
        "OPM_SKILLS_GUIDANCE": {
            "url": "https://www.opm.gov/chcoc/transmittals/2024/Skills-Based%20Hiring%20Guidance%20and%20Competency%20Model%20for%20Artificial%20Intelligence%20Work.pdf",
            "source_title": "Skills-Based Hiring Guidance and Competency Model for Artificial Intelligence Work",
        },
        "RESOURCES_DATA_SKILLS": {
            "url": "https://resources.data.gov/assets/documents/fds-data-skills-catalog.pdf",
            "source_title": "Curated Data Skills Catalog",
        },
    }


def load_current_coded() -> pd.DataFrame:
    """Load the committed 2026 coded dataset as the base for the redesign."""
    path = project_path("data", "processed", "requirements_coded_2026.csv")
    return pd.read_csv(path)


def build_search_log(coded: pd.DataFrame) -> pd.DataFrame:
    """Build an auditable search log for the 2026 update layer."""
    source_registry = build_search_source_registry()
    rows: list[dict[str, str]] = []

    def add_log(
        requirement_ids: list[str],
        source_key: str,
        result: str,
        notes: str,
    ) -> None:
        source = source_registry[source_key]
        for requirement_id in requirement_ids:
            rows.append(
                {
                    "requirement_id": requirement_id,
                    "url": source["url"],
                    "source_title": source["source_title"],
                    "date_checked": CHECK_DATE,
                    "result": result,
                    "notes": notes,
                }
            )

    base_result_map = {
        "Implemented": "Supports",
        "Partially implemented": "Partial support",
        "Superseded or replaced": "Supports",
        "Unable to verify": "Context only",
        "Not implemented": "No evidence",
        "No longer applicable": "Not relevant",
    }
    for row in coded.to_dict(orient="records"):
        rows.append(
            {
                "requirement_id": row["requirement_id"],
                "url": row["evidence_url"],
                "source_title": row["evidence_title"],
                "date_checked": CHECK_DATE,
                "result": base_result_map[row["updated_2026_status"]],
                "notes": (
                    "Cited source from the committed July 24, 2026 update; re-reviewed during "
                    "the evidence-quality confidence pass."
                ),
            }
        )

    add_log(
        ["EO13859_4a", "EO13859_4b_i", "EO13859_4b_ii"],
        "NITRD_PROGRESS_PDF",
        "Context only",
        "Supports the broader NITRD investment and coordination context behind the ongoing AI R&D priority rows.",
    )
    add_log(
        ["EO13859_5a_i_rfi", "EO13859_5a_i_barriers"],
        "FED_DATA_ACTION_PLAN",
        "Context only",
        "Tracking and action-plan materials reinforce the completion context around the RFI and barrier-investigation workflow.",
    )
    add_log(
        ["EO13859_5c"],
        "NITRD_AI",
        "Context only",
        "NITRD program materials provide contextual confirmation that the cloud-computing recommendations report sits within the federal AI R&D coordination workflow.",
    )
    add_log(
        ["EO13859_6a_b"],
        "FR_AI_REG_DRAFT",
        "Context only",
        "The draft-for-comment notice provides direct context for the issuance path that ended in M-21-06.",
    )
    add_log(
        ["EO13859_6d"],
        "NIST_PLAN_PDF",
        "Supports",
        "The direct PDF artifact supports the NIST standards-plan completion judgment.",
    )
    add_log(
        ["EO13960_2b", "EO13960_4a"],
        "AI_GOV",
        "Context only",
        "Current federal AI strategy materials provide contextual support for continuing governance and public-trust expectations.",
    )
    add_log(
        ["EO13960_5b", "EO13960_5c", "EO13960_5e"],
        "EPA_AI_INVENTORY",
        "Partial support",
        "A second agency inventory page supports the partial government-wide inventory judgment without proving universal coverage.",
    )
    add_log(
        ["EO13960_6_participation"],
        "GSA_AI_COP",
        "Supports",
        "The Chief AI Officer and community-of-practice ecosystem directly supports the interagency participation judgment.",
    )
    add_log(
        ["EO13960_7a"],
        "GSA_AI",
        "Context only",
        "The broader GSA AI program page provides context for the continuing PIF and federal AI talent ecosystem.",
    )
    add_log(
        ["EO13960_8c"],
        "GSA_AI_COMPLIANCE",
        "Context only",
        "Agency compliance-structure materials provide additional context for the newer accountable-official model.",
    )
    add_log(
        ["AIGA_103_create_coe"],
        "GSA_AI_RESOURCES",
        "Context only",
        "The GSA AI resources hub provides contextual support for the continued operation of the AI Center of Excellence function.",
    )
    add_log(
        ["AIGA_103_duties"],
        "GSA_AI_COP",
        "Partial support",
        "The cross-agency community of practice supports the partial-duty judgment for the AI Center of Excellence.",
    )
    add_log(
        ["AIGA_103_duties"],
        "GSA_AI_USE_CASES",
        "Partial support",
        "Public use-case publication is one direct piece of the statutory AI Center of Excellence duties bundle.",
    )
    add_log(
        ["AIGA_104_abd"],
        "M25_22",
        "Supports",
        "The acquisition memo is a major co-equal guidance artifact already referenced in the original 2026 coding rationale.",
    )
    add_log(
        ["AIGA_104c"],
        "DOJ_M24_PLAN",
        "Partial support",
        "A second public agency compliance artifact supports the partial implementation judgment for public plans.",
    )
    add_log(
        ["AIGA_104c"],
        "EPA_AI_COMPLIANCE",
        "Partial support",
        "A third public agency compliance artifact supports the partial implementation judgment for public plans.",
    )
    add_log(
        ["AIGA_105a"],
        "OPM_AI_REVIEW",
        "Context only",
        "OPM oversight materials reinforce the continuing workforce-implementation context around the AI in Government Act skills guidance.",
    )

    add_log(
        ["EO13859_2a_e"],
        "NITRD_AI",
        "Context only",
        "Federal AI R&D coordination exists, but the page does not verify completion of the full strategic-objectives bundle.",
    )
    add_log(
        ["EO13859_2a_e"],
        "GSA_AI",
        "Context only",
        "The agency AI hub shows active federal AI work but does not verify the government-wide strategic-objectives clause.",
    )
    add_log(
        ["EO13859_2a_e"],
        "OPM_AI_WORKFORCE_FUTURE",
        "Context only",
        "Workforce activity is relevant context but not direct evidence that agencies satisfied the full strategic-objectives requirement.",
    )
    add_log(
        ["EO13859_4c"],
        "NITRD_AI",
        "Context only",
        "Current interagency coordination does not directly verify the required non-federal collaboration exploration by covered agencies.",
    )
    add_log(
        ["EO13859_4c"],
        "GSA_AI_COP",
        "Context only",
        "Cross-sector participation exists, but this page does not directly document the collaboration obligation in the requirement text.",
    )
    add_log(
        ["EO13859_5a", "EO13859_5a_ii", "EO13859_5a_iii", "EO13859_5a_iv", "EO13859_5a_v"],
        "DCAT_PRIORITIES",
        "Context only",
        "Metadata and inventory guidance is relevant context, but it does not directly verify completion of the specific agency review obligations in these rows.",
    )
    add_log(
        ["EO13859_5a", "EO13859_5a_ii", "EO13859_5a_iii", "EO13859_5a_iv", "EO13859_5a_v"],
        "NITRD_AI",
        "Context only",
        "Federal AI R&D coordination is relevant context, but it does not directly verify these agency-by-agency data-and-model access actions.",
    )
    add_log(
        ["EO13859_5a", "EO13859_5a_ii", "EO13859_5a_iii", "EO13859_5a_iv", "EO13859_5a_v"],
        "AI_GOV",
        "Context only",
        "Current national AI strategy language is relevant context, but it does not directly verify the original data-and-model access implementation tasks.",
    )
    add_log(
        ["EO13859_5b"],
        "NITRD_CLOUD_REPORT",
        "Context only",
        "The report shows progress on computing access, but it does not directly verify that every named agency prioritized high-performance computing allocations for AI.",
    )
    add_log(
        ["EO13859_5b"],
        "NITRD_PROGRESS_PDF",
        "Context only",
        "Federal AI R&D investment reporting provides related context but not requirement-specific proof of high-performance computing allocation decisions.",
    )
    add_log(
        ["EO13859_5d"],
        "NITRD_AI",
        "Context only",
        "Interagency AI coordination exists, but the page does not directly verify the specific technical-expertise support obligation to the American Technology Council.",
    )
    add_log(
        ["EO13859_5d"],
        "GSA_AI_COP",
        "Context only",
        "Cross-agency coordination infrastructure is relevant context but not direct proof of the specific advisory obligation in this row.",
    )
    add_log(
        ["EO13859_6c"],
        "M21_06",
        "Context only",
        "The underlying regulatory memo exists, but this artifact does not prove agencies submitted the required review-and-plan materials to OMB.",
    )
    add_log(
        ["EO13859_6c"],
        "FR_AI_REG_DRAFT",
        "Context only",
        "The draft memo notice confirms the rulemaking path but does not prove the downstream agency submission requirement was completed.",
    )
    add_log(
        ["EO13859_6c"],
        "AI_GOV",
        "No evidence",
        "Current White House AI strategy materials do not surface a public record of the row-specific regulatory-authority submissions.",
    )
    add_log(
        ["EO13859_7a_i_ii"],
        "OPM_AI_WORKFORCE_FUTURE",
        "Context only",
        "Current federal AI workforce activity is relevant context but does not directly verify the required annual communications from covered grantmaking agencies.",
    )
    add_log(
        ["EO13859_7a_i_ii"],
        "GSA_AI_TRAINING",
        "Context only",
        "Training initiatives show education activity, not the row-specific annual reporting obligation.",
    )
    add_log(
        ["EO13859_7b", "EO13859_7c"],
        "OPM_AI_WORKFORCE_FUTURE",
        "Context only",
        "Current AI workforce activity is relevant context but does not directly verify the specific NSTC recommendation and advisory obligations in these rows.",
    )
    add_log(
        ["EO13859_7b", "EO13859_7c"],
        "RESOURCES_DATA_SKILLS",
        "Context only",
        "Federal data-skills materials provide related context but not direct verification of the row-specific NSTC actions.",
    )
    add_log(
        ["EO13859_8a_b", "EO13859_8c"],
        "AI_GOV",
        "Context only",
        "Current national AI strategy materials do not reveal the historical status of the original national-security action-plan requirement.",
    )
    add_log(
        ["EO13859_8a_b", "EO13859_8c"],
        "EO14179",
        "Context only",
        "A newer AI executive order exists, but it does not by itself verify whether the earlier national-security action plan was completed or formally absorbed.",
    )
    add_log(
        ["EO13960_4b"],
        "CIO_INVENTORY_REFERENCE_DEAD",
        "Dead link",
        "The likely historical CIO Council reference location now resolves to a 404 and does not provide the roadmap artifact required by the row.",
    )
    add_log(
        ["EO13960_4b"],
        "AI_GOV_INVENTORIES_DEAD",
        "Dead link",
        "The likely current AI.Gov inventory landing page now resolves to a 404 and does not supply a public roadmap artifact.",
    )
    add_log(
        ["EO13960_4b"],
        "CIO_HOME",
        "No evidence",
        "The CIO Council home page does not surface the specific roadmap deliverable required by this row.",
    )
    add_log(
        ["EO13960_4c"],
        "GSA_AI_GOVERNANCE",
        "Context only",
        "Current agency governance guidance references AI oversight, but it does not directly verify government-wide use of voluntary consensus standards in the specific EO 13960 sense.",
    )
    add_log(
        ["EO13960_4c"],
        "NIST_PLAN_PAGE",
        "Context only",
        "Technical standards work remains visible, but the page does not directly verify the government-wide practice required in this EO 13960 row.",
    )
    add_log(
        ["EO13960_5a"],
        "CIO_INVENTORY_REFERENCE_DEAD",
        "Dead link",
        "The likely historical CIO Council inventory reference page is no longer publicly available.",
    )
    add_log(
        ["EO13960_5a"],
        "CIO_INVENTORY_GUIDANCE_DEAD",
        "Dead link",
        "The likely historical inventory guidance document now resolves to a 404 and cannot be reviewed as a current public artifact.",
    )
    add_log(
        ["EO13960_5a"],
        "AI_GOV_INVENTORIES_DEAD",
        "Dead link",
        "The likely current AI.Gov inventory landing page resolves to a 404 and does not expose the older guidance artifact.",
    )
    add_log(
        ["EO13960_5c_i", "EO13960_5c_ii", "EO13960_5d"],
        "DOJ_AI_INVENTORY",
        "Context only",
        "The public inventory confirms governance activity but does not directly verify completion of the specific plan, implementation, or sharing obligations in these rows.",
    )
    add_log(
        ["EO13960_5c_i", "EO13960_5c_ii", "EO13960_5d"],
        "DOJ_IT_PLAN",
        "Context only",
        "The DOJ strategic plan confirms inventory work exists, but it does not directly prove government-wide completion of the row-specific deliverables.",
    )
    add_log(
        ["EO13960_6_cio_list"],
        "CIO_HOME",
        "No evidence",
        "The CIO Council home page does not surface the specific published list of recommended interagency bodies required by this row.",
    )
    add_log(
        ["EO13960_6_cio_list"],
        "CIO_INVENTORY_REFERENCE_DEAD",
        "Dead link",
        "The likely historical reference page now resolves to a 404 and does not provide the required list.",
    )
    add_log(
        ["EO13960_6_cio_list"],
        "CIO_INVENTORY_GUIDANCE_DEAD",
        "Dead link",
        "The likely historical inventory-guidance document now resolves to a 404 and does not expose the required list.",
    )
    add_log(
        ["EO13960_7b"],
        "OPM_AI_GUIDANCE",
        "Context only",
        "Current OPM AI workforce guidance is relevant but does not directly verify a rotational-program inventory.",
    )
    add_log(
        ["EO13960_7b"],
        "OPM_AI_WORKFORCE_FUTURE",
        "Context only",
        "Current AI workforce planning materials do not directly expose the rotational-program inventory required by this row.",
    )
    add_log(
        ["EO13960_7c"],
        "OPM_AI_GUIDANCE",
        "Context only",
        "Current OPM AI workforce guidance is relevant but does not directly provide the required recommendations report on rotational programs.",
    )
    add_log(
        ["EO13960_7c"],
        "OPM_AI_WORKFORCE_FUTURE",
        "Context only",
        "Current AI workforce planning materials do not directly provide the row-specific recommendations report.",
    )
    add_log(
        ["EO13960_7c"],
        "OPM_PUBLISHED_MEMOS",
        "No evidence",
        "The published memos index did not surface a clear public copy of the specific recommendations report required by this row.",
    )
    add_log(
        ["AIGA_105b"],
        "OPM_AI_WORKFORCE_FUTURE",
        "Context only",
        "Current workforce planning materials show active implementation work but do not directly expose the specific comprehensive plan to Congress required by section 105(b).",
    )
    add_log(
        ["AIGA_105b"],
        "OPM_PUBLISHED_MEMOS",
        "No evidence",
        "The current published-memos index does not surface a public copy of the specific comprehensive plan to Congress required by section 105(b).",
    )
    add_log(
        ["AIGA_105b"],
        "OPM_AI_REVIEW",
        "Context only",
        "OPM AI oversight materials confirm ongoing workforce implementation activity but not the specific congressional plan artifact.",
    )

    search_log = pd.DataFrame(rows)
    duplicates = search_log.duplicated(subset=["requirement_id", "url"], keep="first")
    search_log = search_log.loc[~duplicates].copy()
    invalid_results = set(search_log["result"]) - set(SEARCH_RESULTS)
    if invalid_results:
        raise ValueError(f"Unexpected search-log results: {sorted(invalid_results)}")
    return search_log.sort_values(["requirement_id", "url"]).reset_index(drop=True)


def derive_search_scope(sources_checked: int) -> str:
    """Map logged source counts to a search-scope label."""
    if sources_checked >= 4:
        return "Exhaustive"
    if sources_checked >= 2:
        return "Targeted"
    if sources_checked == 1:
        return "Cursory"
    return "Not recorded"


def build_quality_fields() -> dict[str, dict[str, str | None]]:
    """Return requirement-level evidence-quality metadata for the 2026 layer."""
    values: dict[str, dict[str, str | None]] = {}

    def add(
        requirement_ids: list[str],
        *,
        evidence_found: str,
        evidence_specificity: str | None,
        evidence_temporal_fit: str,
    ) -> None:
        for requirement_id in requirement_ids:
            values[requirement_id] = {
                "evidence_found": evidence_found,
                "evidence_specificity": evidence_specificity,
                "evidence_temporal_fit": evidence_temporal_fit,
            }

    add(
        ["EO13859_4a", "EO13859_4b_i", "EO13859_4b_ii"],
        evidence_found="Yes",
        evidence_specificity="Program-level",
        evidence_temporal_fit="Current and directly applicable",
    )
    add(
        ["EO13859_5a_i_rfi", "EO13859_5a_i_barriers", "EO13859_5c", "EO13859_6a_b", "EO13859_6d"],
        evidence_found="Yes",
        evidence_specificity="Requirement-specific",
        evidence_temporal_fit="Historical but applicable",
    )
    add(
        ["EO13960_7a"],
        evidence_found="Yes",
        evidence_specificity="Program-level",
        evidence_temporal_fit="Current and directly applicable",
    )
    add(
        ["AIGA_103_create_coe", "AIGA_105a"],
        evidence_found="Yes",
        evidence_specificity="Requirement-specific",
        evidence_temporal_fit="Current and directly applicable",
    )
    add(
        ["AIGA_104_abd"],
        evidence_found="Yes",
        evidence_specificity="Requirement-specific",
        evidence_temporal_fit="Current but policy context changed",
    )
    add(
        ["EO13960_2b", "EO13960_4a"],
        evidence_found="Yes",
        evidence_specificity="Program-level",
        evidence_temporal_fit="Current but policy context changed",
    )
    add(
        ["EO13960_5b", "EO13960_5c", "AIGA_104c"],
        evidence_found="Yes",
        evidence_specificity="Agency-level",
        evidence_temporal_fit="Current and directly applicable",
    )
    add(
        ["EO13960_5e", "EO13960_6_participation", "AIGA_103_duties"],
        evidence_found="Yes",
        evidence_specificity="Requirement-specific",
        evidence_temporal_fit="Current and directly applicable",
    )
    add(
        ["EO13960_8c"],
        evidence_found="Yes",
        evidence_specificity="Requirement-specific",
        evidence_temporal_fit="Current but policy context changed",
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
            "EO13859_5b",
            "EO13859_5d",
            "EO13859_6c",
            "EO13859_7a_i_ii",
            "EO13859_7b",
            "EO13859_7c",
            "EO13859_8a_b",
            "EO13859_8c",
            "EO13960_4b",
            "EO13960_4c",
            "EO13960_5a",
            "EO13960_5c_i",
            "EO13960_5c_ii",
            "EO13960_5d",
            "EO13960_6_cio_list",
            "EO13960_7b",
            "EO13960_7c",
            "AIGA_105b",
        ],
        evidence_found="No",
        evidence_specificity=None,
        evidence_temporal_fit="Not applicable",
    )

    return values


def apply_quality_framework(
    coded: pd.DataFrame,
    search_log: pd.DataFrame,
) -> pd.DataFrame:
    """Attach search-derived counts and evidence-quality metadata to the 2026 dataset."""
    output = coded.copy()
    output["previous_verification_confidence"] = output["verification_confidence"]

    source_counts = sources_checked_from_log(search_log).rename("sources_checked")
    output = output.merge(source_counts, on="requirement_id", how="left")
    output["sources_checked"] = output["sources_checked"].fillna(0).astype(int)
    output["search_scope"] = output["sources_checked"].map(derive_search_scope)

    quality_fields = build_quality_fields()
    quality_frame = (
        pd.DataFrame.from_dict(quality_fields, orient="index")
        .reset_index()
        .rename(columns={"index": "requirement_id"})
    )
    output = output.merge(quality_frame, on="requirement_id", how="left")

    missing_quality = output.loc[
        output["evidence_found"].isna(),
        "requirement_id",
    ].tolist()
    if missing_quality:
        raise KeyError(f"Missing quality metadata for rows: {missing_quality}")

    output = apply_confidence_index(output)
    problems = validate_values(output)
    if problems:
        raise ValueError("Confidence-value validation failed: " + " | ".join(problems))

    ordered_columns = [
        "requirement_id",
        "source_policy",
        "requirement_text",
        "responsible_entity",
        "deadline",
        "appendix_status",
        "aggregate_status",
        "aggregate_count_included",
        "updated_2026_status",
        "status_change",
        "evidence_url",
        "evidence_title",
        "evidence_date",
        "evidence_source_type",
        "verification_confidence",
        "previous_verification_confidence",
        "evidence_found",
        "evidence_specificity",
        "evidence_temporal_fit",
        "search_scope",
        "sources_checked",
        "confidence_index",
        "confidence_changed",
        "update_notes",
        "superseded_or_replaced",
        "replacement_policy_source",
    ]
    return output[ordered_columns].copy()


def build_confidence_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create a compact multi-view summary for the confidence redesign."""
    rows: list[dict[str, object]] = []

    rows.append(
        {
            "summary_type": "overview",
            "group": "all_rows",
            "label": "total_rows",
            "count": int(len(df)),
        }
    )
    rows.append(
        {
            "summary_type": "overview",
            "group": "all_rows",
            "label": "confidence_changed_yes",
            "count": int((df["confidence_changed"] == "Yes").sum()),
        }
    )
    rows.append(
        {
            "summary_type": "overview",
            "group": "all_rows",
            "label": "unable_to_verify_rows",
            "count": int((df["updated_2026_status"] == "Unable to verify").sum()),
        }
    )

    for column, summary_type in [
        ("previous_verification_confidence", "previous_confidence"),
        ("confidence_index", "confidence_index"),
        ("confidence_changed", "confidence_changed"),
    ]:
        counts = df[column].value_counts().to_dict()
        for label, count in counts.items():
            rows.append(
                {
                    "summary_type": summary_type,
                    "group": "all_rows",
                    "label": label,
                    "count": int(count),
                }
            )

    for status in STATUS_ORDER:
        subset = df.loc[df["updated_2026_status"] == status]
        if subset.empty:
            continue
        for scope in SCOPE_ORDER:
            count = int((subset["search_scope"] == scope).sum())
            if count:
                rows.append(
                    {
                        "summary_type": "search_scope_by_status",
                        "group": status,
                        "label": scope,
                        "count": count,
                    }
                )
        for confidence in CONFIDENCE_ORDER:
            count = int((subset["confidence_index"] == confidence).sum())
            if count:
                rows.append(
                    {
                        "summary_type": "confidence_index_by_status",
                        "group": status,
                        "label": confidence,
                        "count": count,
                    }
                )

    return pd.DataFrame(rows)


def plot_stacked_percent(
    crosstab: pd.DataFrame,
    order: list[str],
    color_map: dict[str, str],
    title: str,
    output_path: Path,
) -> None:
    """Render a horizontal stacked-percent bar chart."""
    plt.style.use("seaborn-v0_8-whitegrid")
    percentages = crosstab.div(crosstab.sum(axis=1), axis=0).fillna(0) * 100
    figure, axis = plt.subplots(figsize=(11, 6))
    left = pd.Series(0, index=percentages.index, dtype=float)
    for label in order:
        if label not in percentages.columns:
            continue
        values = percentages[label]
        axis.barh(
            percentages.index,
            values,
            left=left,
            color=color_map[label],
            label=label,
        )
        left = left + values

    axis.set_title(title)
    axis.set_xlabel("Percent of requirements")
    axis.set_xlim(0, 100)
    axis.legend(frameon=False, ncol=min(len(order), 3), bbox_to_anchor=(0.5, 1.02), loc="lower center")
    for spine in ("top", "right"):
        axis.spines[spine].set_visible(False)
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def plot_shift_heatmap(
    df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Render a heatmap showing confidence shifts from old to new labels."""
    shift = pd.crosstab(
        df["previous_verification_confidence"],
        df["confidence_index"],
    ).reindex(index=CONFIDENCE_ORDER, columns=CONFIDENCE_ORDER, fill_value=0)
    plt.style.use("seaborn-v0_8-whitegrid")
    figure, axis = plt.subplots(figsize=(7, 5))
    sns.heatmap(
        shift,
        annot=True,
        fmt="d",
        cmap="Blues",
        linewidths=0.5,
        cbar=False,
        ax=axis,
    )
    axis.set_title("Shift from Previous Verification Confidence to Confidence Index")
    axis.set_xlabel("confidence_index")
    axis.set_ylabel("previous_verification_confidence")
    figure.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    """Generate search-log and confidence-redesign artifacts."""
    coded = load_current_coded()
    search_log = build_search_log(coded)

    raw_dir = project_path("data", "raw")
    processed_dir = project_path("data", "processed")
    figures_dir = project_path("outputs", "figures")

    save_csv(search_log, raw_dir / "search_log.csv")

    updated = apply_quality_framework(coded, search_log)
    save_csv(updated, processed_dir / "requirements_coded_2026.csv")

    collinearity = check_collinearity(
        updated,
        status_col="updated_2026_status",
        index_col="confidence_index",
        threshold=0.70,
    ).reset_index().rename(columns={"updated_2026_status": "status"})
    save_csv(collinearity, processed_dir / "confidence_collinearity_report.csv")

    confidence_summary = build_confidence_summary(updated)
    save_csv(confidence_summary, processed_dir / "confidence_recode_summary.csv")

    scope_crosstab = pd.crosstab(
        updated["updated_2026_status"],
        updated["search_scope"],
    ).reindex(index=STATUS_ORDER, columns=SCOPE_ORDER, fill_value=0)
    confidence_crosstab = pd.crosstab(
        updated["updated_2026_status"],
        updated["confidence_index"],
    ).reindex(index=STATUS_ORDER, columns=CONFIDENCE_ORDER, fill_value=0)

    plot_stacked_percent(
        scope_crosstab,
        SCOPE_ORDER,
        SEARCH_SCOPE_COLORS,
        "Search Scope by 2026 Status",
        figures_dir / "search_scope_by_status_2026.png",
    )
    plot_stacked_percent(
        confidence_crosstab,
        CONFIDENCE_ORDER,
        CONFIDENCE_COLORS,
        "Confidence Index by 2026 Status",
        figures_dir / "confidence_index_by_status_2026.png",
    )
    plot_shift_heatmap(
        updated,
        figures_dir / "confidence_index_shift.png",
    )


if __name__ == "__main__":
    main()
