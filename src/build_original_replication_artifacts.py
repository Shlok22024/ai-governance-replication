"""Build the original requirement-level replication dataset and summary artifacts.

This script encodes the paper's original requirement-level tracker as a structured
45-row dataset for the replication baseline. It intentionally stops at the
original-status phase and does not perform any 2026 update coding.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import pandas as pd

from data_cleaning import project_path, save_csv
from visualization_helpers import plot_policy_status_breakdown, save_figure


STATUS_ORDER = ["Implemented", "Unknown", "Not implemented"]
POLICY_ORDER = ["EO 13859", "EO 13960", "AI in Government Act"]


def round_half_up(value: float) -> int:
    """Round a percentage using half-up semantics instead of banker's rounding."""
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def build_original_requirements() -> pd.DataFrame:
    """Return the structured 45-row original replication dataset."""
    rows = [
        {
            "requirement_id": "EO13859_2a_e",
            "source_policy": "EO 13859",
            "requirement_text": (
                "Implementing agencies shall pursue six strategic objectives to promote "
                "and protect American advances in AI, including sustained AI R&D, "
                "access to Federal data and computing resources, reduced barriers to AI "
                "use, technical standards, and AI workforce development."
            ),
            "responsible_entity": "Implementing agencies",
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper classifies this as an ongoing requirement without mandated "
                "outcomes to assess, so implementation was not publicly verifiable."
            ),
        },
        {
            "requirement_id": "EO13859_4a",
            "source_policy": "EO 13859",
            "requirement_text": (
                "Heads of AI R&D agencies shall consider AI as an agency R&D priority "
                "and take that priority into account when developing budget proposals "
                "and planning for the use of funds."
            ),
            "responsible_entity": "Heads of AI R&D agencies",
            "deadline": "None",
            "original_status": "Implemented",
            "original_evidence_notes": (
                "The paper cites the National Artificial Intelligence Research and "
                "Development Strategic Plan: 2019 Update and subsequent progress "
                "reports as indications of sustained implementation."
            ),
        },
        {
            "requirement_id": "EO13859_4b_i",
            "source_policy": "EO 13859",
            "requirement_text": (
                "Heads of AI R&D agencies shall budget an amount of AI R&D appropriate "
                "for this prioritization and communicate plans for achieving it each "
                "fiscal year through the NITRD Program."
            ),
            "responsible_entity": "Heads of AI R&D agencies",
            "deadline": "None",
            "original_status": "Implemented",
            "original_evidence_notes": (
                "The paper treats this as an ongoing requirement with indications of "
                "sustained implementation through NITRD budget and planning materials."
            ),
        },
        {
            "requirement_id": "EO13859_4b_ii",
            "source_policy": "EO 13859",
            "requirement_text": (
                "Heads of AI R&D agencies shall identify each year the programs to "
                "which the AI R&D priority will apply and estimate the total amount "
                "of funds to be spent on each program."
            ),
            "responsible_entity": "Heads of AI R&D agencies",
            "deadline": "Annually within 90 days of enactment of appropriations for an agency",
            "original_status": "Implemented",
            "original_evidence_notes": (
                "The paper points to NITRD supplements and the AI R&D dashboard as "
                "evidence that these annual reporting expectations were being carried out."
            ),
        },
        {
            "requirement_id": "EO13859_4c",
            "source_policy": "EO 13859",
            "requirement_text": (
                "Heads of AI R&D agencies shall explore opportunities for collaboration "
                "with non-Federal entities, including the private sector, academia, "
                "nonprofits, subnational governments, and foreign partners and allies."
            ),
            "responsible_entity": "Heads of AI R&D agencies",
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper classifies this as an ongoing requirement without mandated "
                "outcomes to assess."
            ),
        },
        {
            "requirement_id": "EO13859_5a",
            "source_policy": "EO 13859",
            "requirement_text": (
                "Heads of all agencies shall review Federal data and models to identify "
                "opportunities to increase access and use by the non-Federal AI research "
                "community, including improvements to inventory documentation and the "
                "prioritization of quality and access improvements."
            ),
            "responsible_entity": "Head of all agencies",
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper treats this as open-ended and not publicly verifiable, while "
                "noting partial supporting infrastructure such as the AI Researchers Portal."
            ),
        },
        {
            "requirement_id": "EO13859_5a_i_rfi",
            "source_policy": "EO 13859",
            "requirement_text": (
                "The OMB Director shall publish a Federal Register notice inviting the "
                "public to identify requests for access or quality improvements for "
                "Federal data and models that would improve AI R&D and testing."
            ),
            "responsible_entity": "OMB Director",
            "deadline": "Within 90 days of EO",
            "original_status": "Implemented",
            "original_evidence_notes": (
                "The paper cites the July 10, 2019 Federal Register request for "
                "information on priority access or quality improvements for Federal "
                "data and models for AI research and testing."
            ),
        },
        {
            "requirement_id": "EO13859_5a_i_barriers",
            "source_policy": "EO 13859",
            "requirement_text": (
                "The OMB Director, with the NSTC Select Committee on AI, shall "
                "investigate barriers to access or quality limitations of Federal "
                "data and models that impede AI R&D and testing."
            ),
            "responsible_entity": "OMB Director with NSTC Select Committee on AI",
            "deadline": "Within 90 days of EO",
            "original_status": "Implemented",
            "original_evidence_notes": (
                "The paper treats the Federal Data Strategy 2020 Action Plan and its "
                "tracking of the RFI milestone as evidence that this directive was implemented."
            ),
        },
        {
            "requirement_id": "EO13859_5a_ii",
            "source_policy": "EO 13859",
            "requirement_text": (
                "OMB, with interagency councils and the NSTC Select Committee on AI, "
                "shall update implementation guidance for Enterprise Data Inventories "
                "and Source Code Inventories to support discovery and usability in AI R&D."
            ),
            "responsible_entity": "OMB with interagency councils and NSTC Select Committee on AI",
            "deadline": "Within 120 days of EO",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper found references to a non-final guidance document but no "
                "clear public confirmation that final updated guidance had been issued."
            ),
        },
        {
            "requirement_id": "EO13859_5a_iii",
            "source_policy": "EO 13859",
            "requirement_text": (
                "Agencies shall consider methods to improve the quality, usability, and "
                "appropriate access to priority data by the AI research community and "
                "identify associated resource implications."
            ),
            "responsible_entity": "Agencies",
            "deadline": "Within 180 days of EO",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper notes references in agency open data planning materials but "
                "found no mandated public reporting that would verify implementation."
            ),
        },
        {
            "requirement_id": "EO13859_5a_iv",
            "source_policy": "EO 13859",
            "requirement_text": (
                "Agencies, coordinating with privacy officials, statistical entities, "
                "data managers, and other relevant personnel, shall identify barriers "
                "or requirements associated with increased access to and use of data "
                "and models, including privacy, safety, security, documentation, "
                "governance, and related considerations."
            ),
            "responsible_entity": (
                "Agencies in coordination with privacy officials, statistical entities, "
                "data managers, and relevant personnel"
            ),
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper treats this as open-ended and not publicly verifiable."
            ),
        },
        {
            "requirement_id": "EO13859_5a_v",
            "source_policy": "EO 13859",
            "requirement_text": (
                "Agencies shall identify opportunities to use new technologies and best "
                "practices to increase access to and usability of open data and models, "
                "while exploring appropriate controls on access to sensitive or restricted "
                "data and models."
            ),
            "responsible_entity": "Agencies",
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper classifies this as an ongoing requirement without mandated "
                "public reporting or a concrete outcome to assess."
            ),
        },
        {
            "requirement_id": "EO13859_5b",
            "source_policy": "EO 13859",
            "requirement_text": (
                "The Secretaries of Defense, Commerce, Health and Human Services, and "
                "Energy, the NASA Administrator, and the NSF Director shall prioritize "
                "the allocation of high-performance computing resources for AI-related "
                "applications through discretionary reserves or other mechanisms."
            ),
            "responsible_entity": (
                "Secretaries of Defense, Commerce, Health and Human Services, and Energy; "
                "Administrator of NASA; Director of NSF"
            ),
            "deadline": "None",
            "original_status": "Implemented",
            "original_evidence_notes": (
                "The paper cites the National AI Initiative Office's AI Researchers Portal "
                "and its federally supported computing infrastructure resources overview."
            ),
        },
        {
            "requirement_id": "EO13859_5c",
            "source_policy": "EO 13859",
            "requirement_text": (
                "The NSTC Select Committee on AI, in coordination with GSA, shall submit "
                "a report to the President making recommendations on better enabling the "
                "use of cloud computing resources for federally funded AI R&D."
            ),
            "responsible_entity": "NSTC Select Committee on AI in coordination with GSA",
            "deadline": "Within 180 days of EO",
            "original_status": "Implemented",
            "original_evidence_notes": (
                "The paper cites the November 17, 2020 recommendations report and a July "
                "2022 lessons-learned report, noting that the original deadline was missed "
                "but the required report was ultimately produced."
            ),
        },
        {
            "requirement_id": "EO13859_5d",
            "source_policy": "EO 13859",
            "requirement_text": (
                "The NSTC Select Committee on AI shall provide technical expertise to the "
                "American Technology Council on AI and the modernization of Federal "
                "technology, data, and digital service delivery."
            ),
            "responsible_entity": "NSTC Select Committee on AI",
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper treats this as an ongoing requirement without a mandated outcome."
            ),
        },
        {
            "requirement_id": "EO13859_6a_b",
            "source_policy": "EO 13859",
            "requirement_text": (
                "OMB, coordinating with OSTP, the Domestic Policy Council, the NEC, and "
                "other relevant agencies and stakeholders, shall issue a memorandum to guide "
                "regulatory and non-regulatory approaches to AI and shall release a draft "
                "for public comment before finalizing it."
            ),
            "responsible_entity": (
                "OMB Director in coordination with OSTP, Domestic Policy Council, NEC, "
                "and relevant agencies and stakeholders"
            ),
            "deadline": "Within 180 days of EO",
            "original_status": "Implemented",
            "original_evidence_notes": (
                "The paper cites the January 2020 draft request for comments and the "
                "final OMB M-21-06 memorandum issued on November 17, 2020."
            ),
        },
        {
            "requirement_id": "EO13859_6c",
            "source_policy": "EO 13859",
            "requirement_text": (
                "Implementing agencies that also have regulatory authorities shall review "
                "their authorities and submit plans to OMB to achieve consistency with the "
                "OMB memorandum issued under section 6(a)."
            ),
            "responsible_entity": "Implementing agencies with regulatory authorities",
            "deadline": "Within 180 days of OMB memorandum",
            "original_status": "Not implemented",
            "original_evidence_notes": (
                "The paper marks this as not implemented and points to the poor publication "
                "rate of Agency AI Plans discussed in Section 6 and Appendix B."
            ),
        },
        {
            "requirement_id": "EO13859_6d",
            "source_policy": "EO 13859",
            "requirement_text": (
                "The Secretary of Commerce, through the NIST Director and with relevant "
                "agency participation, shall issue a plan for Federal engagement in the "
                "development of AI technical standards and related tools."
            ),
            "responsible_entity": "Secretary of Commerce through the NIST Director",
            "deadline": "Within 180 days of EO",
            "original_status": "Implemented",
            "original_evidence_notes": (
                "The paper cites NIST's August 2019 report, A Plan for Federal Engagement "
                "in Developing AI Technical Standards and Related Tools."
            ),
        },
        {
            "requirement_id": "EO13859_7a_i_ii",
            "source_policy": "EO 13859",
            "requirement_text": (
                "Implementing agencies that provide educational grants shall consider AI as "
                "a priority area within existing Federal fellowship and service programs and "
                "shall annually communicate plans for doing so to the NSTC Select Committee on AI."
            ),
            "responsible_entity": "Implementing agencies that provide educational grants",
            "deadline": "Annually",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper found no mandated public reporting that would verify the status "
                "of this ongoing annual requirement."
            ),
        },
        {
            "requirement_id": "EO13859_7b",
            "source_policy": "EO 13859",
            "requirement_text": (
                "The NSTC Select Committee on AI shall provide recommendations to the NSTC "
                "Committee on STEM Education regarding AI-related educational and workforce "
                "development considerations that focus on American citizens."
            ),
            "responsible_entity": "NSTC Select Committee on AI",
            "deadline": "Within 90 days of EO",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper found no mandated public reporting that would verify whether the "
                "recommendations had been delivered."
            ),
        },
        {
            "requirement_id": "EO13859_7c",
            "source_policy": "EO 13859",
            "requirement_text": (
                "The NSTC Select Committee on AI shall provide technical expertise to the "
                "National Council for the American Worker on AI and the American workforce."
            ),
            "responsible_entity": "NSTC Select Committee on AI",
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper treats this as an ongoing requirement without mandated public reporting."
            ),
        },
        {
            "requirement_id": "EO13859_8a_b",
            "source_policy": "EO 13859",
            "requirement_text": (
                "The Assistant to the President for National Security Affairs, coordinating "
                "with OSTP and relevant agencies, shall organize and submit to the President "
                "an action plan to protect the United States advantage in AI and related "
                "critical technologies against strategic competitors and adversarial nations."
            ),
            "responsible_entity": (
                "Assistant to the President for National Security Affairs in coordination "
                "with OSTP and recipients of the NSPM"
            ),
            "deadline": "Within 120 days of EO",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper found no public confirmation of the action plan and notes that "
                "the associated national security memorandum may itself not have been issued publicly."
            ),
        },
        {
            "requirement_id": "EO13859_8c",
            "source_policy": "EO 13859",
            "requirement_text": (
                "Agencies that are recipients of the action plan described in section 8(a)-(b) "
                "shall implement that action plan."
            ),
            "responsible_entity": "Agencies that are recipients of the action plan",
            "deadline": "Within 120 days of EO",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper found no mandated public reporting that would verify implementation."
            ),
        },
        {
            "requirement_id": "EO13960_2b",
            "source_policy": "EO 13960",
            "requirement_text": (
                "Responsible agencies shall, when considering the design, development, "
                "acquisition, and use of AI in Government, be guided by the order's "
                "principles in order to foster public trust and remain consistent with law."
            ),
            "responsible_entity": "Responsible agencies as defined in section 8",
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper notes example agency documents that suggest implementation, but "
                "classifies the overall ongoing requirement as not publicly verifiable."
            ),
        },
        {
            "requirement_id": "EO13960_4a",
            "source_policy": "EO 13960",
            "requirement_text": (
                "To the extent existing OMB policies that address information and information "
                "technology design, development, acquisition, and use are consistent with the "
                "order's principles and applicable law, those policies shall continue to apply."
            ),
            "responsible_entity": "OMB and agencies",
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper treats this as an ongoing requirement without a mandated public outcome."
            ),
        },
        {
            "requirement_id": "EO13960_4b",
            "source_policy": "EO 13960",
            "requirement_text": (
                "OMB shall publicly post a roadmap for policy guidance that it intends to "
                "create or revise to better support the use of AI in Government, including "
                "a schedule for public engagement and finalization where appropriate."
            ),
            "responsible_entity": "OMB Director in coordination with key stakeholders",
            "deadline": "Within 180 days of EO",
            "original_status": "Not implemented",
            "original_evidence_notes": (
                "The paper found no public roadmap that matched this requirement, despite "
                "related milestones in the 2021 Federal Data Strategy Action Plan."
            ),
        },
        {
            "requirement_id": "EO13960_4c",
            "source_policy": "EO 13960",
            "requirement_text": (
                "Agencies shall continue to use voluntary consensus standards developed "
                "with industry participation where available and appropriate, and OMB shall "
                "take such standards into account when revising or developing AI guidance."
            ),
            "responsible_entity": "Agencies and OMB",
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper classifies this as an ongoing requirement without mandated public reporting."
            ),
        },
        {
            "requirement_id": "EO13960_5a",
            "source_policy": "EO 13960",
            "requirement_text": (
                "The CIO Council, coordinating with relevant interagency bodies, shall "
                "identify, provide guidance on, and make publicly available the criteria, "
                "format, and mechanisms for agency inventories of non-classified and "
                "non-sensitive AI use cases."
            ),
            "responsible_entity": "Federal CIO Council in coordination with interagency bodies",
            "deadline": "Within 60 days of EO",
            "original_status": "Implemented",
            "original_evidence_notes": (
                "The paper cites the CIO Council's 2021 guidance, FAQ materials, example "
                "scenarios, and template for agency AI use case inventories."
            ),
        },
        {
            "requirement_id": "EO13960_5b",
            "source_policy": "EO 13960",
            "requirement_text": (
                "Responsible agencies shall prepare an inventory of non-classified and "
                "non-sensitive AI use cases, including current and planned uses, and "
                "update that inventory annually."
            ),
            "responsible_entity": "Responsible agencies",
            "deadline": "Within 180 days of CIO Council guidance; annually thereafter",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper treats this requirement as separate from the public disclosure "
                "requirement in section 5(e) and finds no mandated public reporting on status."
            ),
        },
        {
            "requirement_id": "EO13960_5c",
            "source_policy": "EO 13960",
            "requirement_text": (
                "As part of their inventories, agencies shall identify, review, and assess "
                "existing AI deployed and operating in support of agency missions for any "
                "inconsistencies with the order."
            ),
            "responsible_entity": "Responsible agencies",
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper classifies this as open-ended and not publicly verifiable apart "
                "from the more specific follow-on requirements in sections 5(c)(i) and 5(c)(ii)."
            ),
        },
        {
            "requirement_id": "EO13960_5c_i",
            "source_policy": "EO 13960",
            "requirement_text": (
                "Agencies shall develop plans either to achieve consistency with the order "
                "for each AI application or to retire applications found not to be consistent "
                "with the order, and those plans must be approved by the responsible officials."
            ),
            "responsible_entity": "Responsible agencies",
            "deadline": "Within 120 days of completing AI inventory",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper found no mandated public reporting that would verify completion "
                "of these plans."
            ),
        },
        {
            "requirement_id": "EO13960_5d",
            "source_policy": "EO 13960",
            "requirement_text": (
                "Agencies shall share their AI inventories with other agencies, to the extent "
                "practicable and consistent with applicable law and policy, through coordination "
                "by the CIO and Chief Data Officer Councils."
            ),
            "responsible_entity": "Responsible agencies; CIO Council; Chief Data Officer Council",
            "deadline": "Within 60 days of completing AI inventory",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper found no mandated public reporting that would verify whether "
                "interagency sharing had taken place."
            ),
        },
        {
            "requirement_id": "EO13960_5e",
            "source_policy": "EO 13960",
            "requirement_text": (
                "Agencies shall make their AI inventories available to the public, to the "
                "extent practicable and consistent with applicable law and policy."
            ),
            "responsible_entity": "Responsible agencies",
            "deadline": "Within 120 days of completing AI inventory",
            "original_status": "Not implemented",
            "original_evidence_notes": (
                "The paper marks this as not implemented overall and notes that only a "
                "minority of inventories had been publicly posted at the time of assessment."
            ),
        },
        {
            "requirement_id": "EO13960_6_participation",
            "source_policy": "EO 13960",
            "requirement_text": (
                "Agencies are expected to participate in interagency bodies for the purpose "
                "of advancing implementation of the principles and the use of AI consistent "
                "with the order."
            ),
            "responsible_entity": "Responsible agencies",
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper treats this as an ongoing requirement without a mandated outcome to assess."
            ),
        },
        {
            "requirement_id": "EO13960_6_cio_list",
            "source_policy": "EO 13960",
            "requirement_text": (
                "The CIO Council shall publish a list of recommended interagency bodies and "
                "forums in which agencies may elect to participate to advance the AI principles."
            ),
            "responsible_entity": "Federal CIO Council",
            "deadline": "Within 45 days of EO",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper found no mandated public reporting that would verify publication "
                "of the required list."
            ),
        },
        {
            "requirement_id": "EO13960_7a",
            "source_policy": "EO 13960",
            "requirement_text": (
                "The Presidential Innovation Fellows program, administered by GSA in "
                "collaboration with agencies, shall identify priority areas of expertise "
                "and establish an AI track to attract experts from industry and academia."
            ),
            "responsible_entity": "Presidential Innovation Fellows program (GSA)",
            "deadline": "Within 90 days of EO",
            "original_status": "Implemented",
            "original_evidence_notes": (
                "The paper notes that the 2022 Presidential Innovation Fellows application "
                "included a Data Strategy and AI track, treating the requirement as implemented."
            ),
        },
        {
            "requirement_id": "EO13960_7b",
            "source_policy": "EO 13960",
            "requirement_text": (
                "OPM, coordinating with GSA and other relevant agencies, shall create an "
                "inventory of Federal Government rotational programs and determine how they "
                "can be used to expand the number of employees with AI expertise."
            ),
            "responsible_entity": "OPM in coordination with GSA and relevant agencies",
            "deadline": "Within 45 days of EO",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper found no mandated public reporting that would verify completion "
                "of the inventory."
            ),
        },
        {
            "requirement_id": "EO13960_7c",
            "source_policy": "EO 13960",
            "requirement_text": (
                "OPM shall issue a report with recommendations on how rotational programs "
                "can best be used to expand the number of employees with AI expertise at agencies."
            ),
            "responsible_entity": "OPM",
            "deadline": "Within 180 days of creating inventory under section 7(b)",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper found no public report matching the EO's specific recommendation "
                "requirement, even though broader workforce priority materials existed."
            ),
        },
        {
            "requirement_id": "EO13960_8c",
            "source_policy": "EO 13960",
            "requirement_text": (
                "Agencies shall specify the responsible official or officials who will "
                "coordinate implementation of the order's principles with the agency data "
                "governance body and relevant officials and collaborate with the interagency bodies."
            ),
            "responsible_entity": "Responsible agencies",
            "deadline": "Within 30 days of EO",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper found no mandated public reporting that would verify designation "
                "of the responsible officials."
            ),
        },
        {
            "requirement_id": "AIGA_103_create_coe",
            "source_policy": "AI in Government Act",
            "requirement_text": (
                "GSA shall create an AI Center of Excellence to facilitate the adoption of "
                "AI technologies in the Federal Government, improve cohesion and competency "
                "in AI adoption and use, and benefit the public by enhancing productivity "
                "and efficiency of Federal operations."
            ),
            "responsible_entity": "GSA",
            "deadline": "None",
            "original_status": "Implemented",
            "original_evidence_notes": (
                "The paper cites the Artificial Intelligence Center of Excellence, its "
                "services catalog, and the published AI Guide for Government."
            ),
        },
        {
            "requirement_id": "AIGA_103_duties",
            "source_policy": "AI in Government Act",
            "requirement_text": (
                "The duties of the AI Center of Excellence shall include convening relevant "
                "stakeholders, publishing information on AI programs and initiatives, advising "
                "GSA, OMB, agencies, and OSTP, assisting agencies in applying Federal policies, "
                "and consulting with agencies that operate or support AI-related programs."
            ),
            "responsible_entity": "GSA AI Center of Excellence",
            "deadline": "None",
            "original_status": "Unknown",
            "original_evidence_notes": (
                "The paper classifies most of these duties as ongoing requirements without "
                "mandated outcomes to assess, while noting partial examples of activity."
            ),
        },
        {
            "requirement_id": "AIGA_104_abd",
            "source_policy": "AI in Government Act",
            "requirement_text": (
                "OMB, coordinating with OSTP, GSA, and other relevant agencies and stakeholders, "
                "shall issue draft and final memorandum guidance on Federal acquisition and use "
                "of AI, barriers to agency AI use, discriminatory impact and bias mitigation, "
                "and the template for agency compliance plans, and shall update that memorandum "
                "every two years for ten years."
            ),
            "responsible_entity": "OMB in coordination with OSTP, GSA, and relevant agencies and stakeholders",
            "deadline": (
                "Draft for public comment not later than 180 days after enactment; final not later "
                "than 270 days after enactment"
            ),
            "original_status": "Not implemented",
            "original_evidence_notes": (
                "The paper marks both the draft and final memorandum requirement as not implemented "
                "as of the 2022 assessment window."
            ),
        },
        {
            "requirement_id": "AIGA_104c",
            "source_policy": "AI in Government Act",
            "requirement_text": (
                "Heads of agencies shall submit to OMB and post publicly either a plan to "
                "achieve consistency with the OMB memorandum or a written determination that "
                "the agency does not use and does not anticipate using AI."
            ),
            "responsible_entity": "Heads of agencies",
            "deadline": "No later than 180 days after OMB issues memorandum",
            "original_status": "Not implemented",
            "original_evidence_notes": (
                "The paper marks this as not implemented because the required OMB memorandum "
                "had not been issued and corresponding agency plans had not been posted."
            ),
        },
        {
            "requirement_id": "AIGA_105a",
            "source_policy": "AI in Government Act",
            "requirement_text": (
                "The OPM Director shall identify AI-related skills and competencies, establish "
                "or update an AI occupational series, estimate the number of Federal employees "
                "in AI-related positions by agency, and prepare two-year and five-year workforce forecasts."
            ),
            "responsible_entity": "OPM Director",
            "deadline": "Not later than 18 months after enactment",
            "original_status": "Not implemented",
            "original_evidence_notes": (
                "The paper marks the workforce and occupational series requirement as not implemented."
            ),
        },
        {
            "requirement_id": "AIGA_105b",
            "source_policy": "AI in Government Act",
            "requirement_text": (
                "The OPM Director shall submit to the relevant congressional committees a "
                "comprehensive plan with a timeline to complete the requirements described in section 105(a)."
            ),
            "responsible_entity": "OPM Director",
            "deadline": "Not later than 120 days after enactment",
            "original_status": "Not implemented",
            "original_evidence_notes": (
                "The paper marks the required congressional plan as not implemented."
            ),
        },
    ]

    dataframe = pd.DataFrame(rows)
    dataframe["deadline"] = dataframe["deadline"].replace({"None": "No fixed deadline"})

    if len(dataframe) != 45:
        raise ValueError(f"Expected 45 requirements, found {len(dataframe)}")

    per_policy_counts = dataframe["source_policy"].value_counts().to_dict()
    expected_policy_counts = {
        "EO 13859": 23,
        "EO 13960": 16,
        "AI in Government Act": 6,
    }
    if per_policy_counts != expected_policy_counts:
        raise ValueError(f"Unexpected policy counts: {per_policy_counts}")

    invalid_statuses = set(dataframe["original_status"]) - set(STATUS_ORDER)
    if invalid_statuses:
        raise ValueError(f"Unexpected original statuses: {sorted(invalid_statuses)}")

    return dataframe


def build_summary(requirements: pd.DataFrame) -> pd.DataFrame:
    """Aggregate policy-level status counts and percentages from the requirement dataset."""
    summary_rows = []

    for policy in POLICY_ORDER:
        subset = requirements.loc[requirements["source_policy"] == policy]
        counts = subset["original_status"].value_counts().to_dict()
        total = len(subset)
        summary_rows.append(
            {
                "instrument": policy,
                "total_requirements": total,
                "implemented_count": counts.get("Implemented", 0),
                "unknown_count": counts.get("Unknown", 0),
                "not_implemented_count": counts.get("Not implemented", 0),
                "implemented_pct": round_half_up(counts.get("Implemented", 0) / total * 100),
                "unknown_pct": round_half_up(counts.get("Unknown", 0) / total * 100),
                "not_implemented_pct": round_half_up(
                    counts.get("Not implemented", 0) / total * 100
                ),
                "notes": "Generated from original_requirements.csv",
            }
        )

    counts = requirements["original_status"].value_counts().to_dict()
    total = len(requirements)
    summary_rows.append(
        {
            "instrument": "Total",
            "total_requirements": total,
            "implemented_count": counts.get("Implemented", 0),
            "unknown_count": counts.get("Unknown", 0),
            "not_implemented_count": counts.get("Not implemented", 0),
            "implemented_pct": round_half_up(counts.get("Implemented", 0) / total * 100),
            "unknown_pct": round_half_up(counts.get("Unknown", 0) / total * 100),
            "not_implemented_pct": round_half_up(
                counts.get("Not implemented", 0) / total * 100
            ),
            "notes": (
                "Generated from the 45-row original replication dataset. This appendix-derived "
                "count yields 12 implemented requirements, which differs from one sentence in "
                "Section 5 of the paper that states 11 implemented."
            ),
        }
    )

    return pd.DataFrame(summary_rows)


def main() -> None:
    """Generate the original dataset, summary files, and status chart."""
    requirements = build_original_requirements()
    summary = build_summary(requirements)

    raw_output = project_path("data", "raw", "original_requirements.csv")
    processed_output = project_path(
        "data",
        "processed",
        "implementation_status_summary.csv",
    )
    table_output = project_path("outputs", "tables", "summary_table.csv")
    requirement_table_output = project_path(
        "outputs",
        "tables",
        "requirement_status_table.csv",
    )
    figure_output = project_path(
        "outputs",
        "figures",
        "implementation_status_original.png",
    )

    save_csv(requirements, raw_output)
    save_csv(summary, processed_output)
    save_csv(summary, table_output)
    save_csv(requirements, requirement_table_output)

    figure = plot_policy_status_breakdown(
        summary[["instrument", "implemented_pct", "unknown_pct", "not_implemented_pct"]],
        "Original Paper Summary of Federal AI Governance Implementation",
    )
    save_figure(figure, figure_output)

    print(f"Wrote {raw_output}")
    print(f"Wrote {processed_output}")
    print(f"Wrote {table_output}")
    print(f"Wrote {requirement_table_output}")
    print(f"Wrote {figure_output}")


if __name__ == "__main__":
    main()
