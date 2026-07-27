"""Create a focused audit table for high-risk July 2026 coding decisions."""

from __future__ import annotations

from io import StringIO
import subprocess

import pandas as pd

from data_cleaning import project_path, save_csv


AUDIT_DECISIONS: dict[str, dict[str, str]] = {
    "EO13859_2a_e": {
        "audit_decision": "Downgrade to Unable to verify",
        "audit_reason": "The cited AI.Gov page is broad, strategic context rather than direct public evidence that agencies pursued the full set of objectives in this requirement.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_4c": {
        "audit_decision": "Keep status",
        "audit_reason": "The row is already coded conservatively because the public evidence is broad and not requirement-specific.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_5a": {
        "audit_decision": "Keep status",
        "audit_reason": "The requirement is already held at Unable to verify because the available public evidence does not prove agency-by-agency review activity.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_5a_ii": {
        "audit_decision": "Keep status",
        "audit_reason": "The public guidance portal does not directly establish that the required inventory-guidance update was completed, so keeping Unable to verify is the safer choice.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_5a_iii": {
        "audit_decision": "Keep status",
        "audit_reason": "The evidence remains too general to verify agency consideration of data quality and access improvements across government.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_5a_iv": {
        "audit_decision": "Keep status",
        "audit_reason": "The available public materials do not document completion of the specific barrier-identification exercise described in the requirement.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_5a_v": {
        "audit_decision": "Keep status",
        "audit_reason": "The public record supports related open-data work but not the specific agency identification of new technologies and controls required here.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_5b": {
        "audit_decision": "Downgrade to Unable to verify",
        "audit_reason": "The cited NITRD evidence shows federal coordination, but it does not directly verify that the named agencies prioritized high-performance computing allocations for AI applications.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_5d": {
        "audit_decision": "Keep status",
        "audit_reason": "The public evidence is still too general to verify that agencies created or maintained the specific access pathways implied by this provision.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_6c": {
        "audit_decision": "Downgrade to Unable to verify",
        "audit_reason": "Later AI-use memoranda do not clearly replace the original M-21-06-specific plan submission obligation for agencies with regulatory authorities.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_7a_i_ii": {
        "audit_decision": "Downgrade to Unable to verify",
        "audit_reason": "Public AI education activity exists, but the evidence does not directly verify the required annual agency communications to the NSTC Select Committee.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_7b": {
        "audit_decision": "Keep status",
        "audit_reason": "The evidence remains too general to verify agency identification of AI-related workforce needs under this specific requirement.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_7c": {
        "audit_decision": "Keep status",
        "audit_reason": "No direct public evidence was found for the specific policy development obligation in this row, so keeping Unable to verify is appropriate.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_8a_b": {
        "audit_decision": "Downgrade to Unable to verify",
        "audit_reason": "A White House fact sheet shows a newer national-security AI directive, but it does not directly establish that this earlier action-plan requirement was formally replaced or completed.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13859_8c": {
        "audit_decision": "Downgrade to Unable to verify",
        "audit_reason": "The public record does not clearly show whether agencies implemented the original action plan or whether that obligation was formally replaced by the newer directive.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13960_2b": {
        "audit_decision": "Keep status",
        "audit_reason": "M-25-21 directly reaffirms governance and public-trust expectations tied to EO 13960, which is enough for a cautious Partially implemented judgment but not a full upgrade.",
        "recommended_status": "Partially implemented",
        "requires_manual_review": "No",
    },
    "EO13960_4a": {
        "audit_decision": "Keep status",
        "audit_reason": "The current OMB governance memorandum is direct evidence that relevant AI policies continue to operate, but not enough to prove full requirement-level completion across government.",
        "recommended_status": "Partially implemented",
        "requires_manual_review": "No",
    },
    "EO13960_4b": {
        "audit_decision": "Downgrade to Unable to verify",
        "audit_reason": "Later OMB AI memoranda exist, but the audit did not locate direct public evidence that the specific roadmap deliverable was posted or formally superseded.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13960_4c": {
        "audit_decision": "Keep status",
        "audit_reason": "The row is already conservatively coded because the cited evidence does not directly verify use of voluntary consensus standards in the specific sense required here.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13960_5a": {
        "audit_decision": "Downgrade to Unable to verify",
        "audit_reason": "Agency inventory pages suggest common practice, but the audit did not find direct public evidence of the CIO Council guidance artifact required by the row.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13960_5b": {
        "audit_decision": "Keep status",
        "audit_reason": "Multiple agency public inventory pages support a cautious Partially implemented judgment, even though the audit did not verify every covered agency individually.",
        "recommended_status": "Partially implemented",
        "requires_manual_review": "No",
    },
    "EO13960_5c": {
        "audit_decision": "Keep status",
        "audit_reason": "Public inventory methodology is indirect, but it still supports a limited conclusion that some review-and-assessment activity is occurring.",
        "recommended_status": "Partially implemented",
        "requires_manual_review": "No",
    },
    "EO13960_5c_i": {
        "audit_decision": "Keep status",
        "audit_reason": "The available public evidence does not directly verify completion of agency planning obligations tied to this row, so keeping Unable to verify is appropriate.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13960_5c_ii": {
        "audit_decision": "Keep status",
        "audit_reason": "This row was originally excluded from the paper's aggregate count, and the current public evidence still does not verify completion of the implementation step itself.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13960_5d": {
        "audit_decision": "Keep status",
        "audit_reason": "The public record does not clearly verify the cross-agency sharing obligation, so the conservative Unable to verify coding should stand.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13960_5e": {
        "audit_decision": "Keep status",
        "audit_reason": "Public agency inventory pages are direct evidence that some agencies are posting inventories, but the audit did not confirm universal coverage, so Partially implemented remains appropriate.",
        "recommended_status": "Partially implemented",
        "requires_manual_review": "No",
    },
    "EO13960_6_participation": {
        "audit_decision": "Keep status",
        "audit_reason": "M-25-21 directly establishes an interagency Chief AI Officer Council, which supports a cautious partial-implementation judgment for participation requirements.",
        "recommended_status": "Partially implemented",
        "requires_manual_review": "No",
    },
    "EO13960_6_cio_list": {
        "audit_decision": "Downgrade to Unable to verify",
        "audit_reason": "The newer governance structure does not directly verify that the required CIO Council list was published or formally replaced by a clearly equivalent deliverable.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13960_7b": {
        "audit_decision": "Keep status",
        "audit_reason": "The current public materials do not directly document the specific rotational-program inventory required here, so retaining Unable to verify is the safer choice.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13960_7c": {
        "audit_decision": "Keep status",
        "audit_reason": "No direct public copy of the required OPM recommendations report was identified in the audit, so the row should remain Unable to verify.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
    "EO13960_8c": {
        "audit_decision": "Keep status",
        "audit_reason": "M-25-21 directly requires agencies to designate Chief AI Officers and governance structures, which clearly absorbs the older responsible-official coordination role.",
        "recommended_status": "Superseded or replaced",
        "requires_manual_review": "No",
    },
    "AIGA_103_duties": {
        "audit_decision": "Keep status",
        "audit_reason": "The GSA AI hub provides direct evidence of several ongoing AI Center of Excellence functions, but not enough to verify every statutory duty in full.",
        "recommended_status": "Partially implemented",
        "requires_manual_review": "No",
    },
    "AIGA_104_abd": {
        "audit_decision": "Keep status",
        "audit_reason": "The public OMB memoranda are direct evidence that the high-level guidance deliverables were eventually issued.",
        "recommended_status": "Implemented",
        "requires_manual_review": "No",
    },
    "AIGA_104c": {
        "audit_decision": "Keep status",
        "audit_reason": "Public agency compliance-plan pages support a cautious Partially implemented coding because the audit did not verify every agency's posting or determination.",
        "recommended_status": "Partially implemented",
        "requires_manual_review": "No",
    },
    "AIGA_105a": {
        "audit_decision": "Keep status",
        "audit_reason": "OPM's published guidance is direct public evidence for the workforce-skills and classification work described in this row.",
        "recommended_status": "Implemented",
        "requires_manual_review": "No",
    },
    "AIGA_105b": {
        "audit_decision": "Keep status",
        "audit_reason": "The audit still did not locate a public copy of the specific plan to Congress required by section 105(b), so keeping Unable to verify is the conservative choice.",
        "recommended_status": "Unable to verify",
        "requires_manual_review": "No",
    },
}


def build_row_audit() -> pd.DataFrame:
    """Build the focused audit table for flagged rows."""
    snapshot = subprocess.run(
        ["git", "show", "HEAD:data/processed/requirements_coded_2026.csv"],
        check=True,
        capture_output=True,
        text=True,
        cwd=project_path(),
    )
    coded = pd.read_csv(StringIO(snapshot.stdout))

    # The user asked for rows whose status_change is not "No change".
    # This project uses "No material change" for that baseline-equivalent state.
    audit_subset = coded.loc[
        (coded["verification_confidence"] == "Low")
        | (coded["updated_2026_status"] == "Partially implemented")
        | (coded["updated_2026_status"] == "Superseded or replaced")
        | (coded["status_change"] != "No material change")
    ].copy()

    audited_ids = set(audit_subset["requirement_id"])
    mapped_ids = set(AUDIT_DECISIONS)
    if audited_ids != mapped_ids:
        missing = sorted(audited_ids - mapped_ids)
        extra = sorted(mapped_ids - audited_ids)
        raise ValueError(
            f"Audit decision map mismatch. Missing={missing} Extra={extra}"
        )

    records: list[dict[str, str]] = []
    for row in audit_subset.sort_values(["source_policy", "requirement_id"]).to_dict(orient="records"):
        decision = AUDIT_DECISIONS[row["requirement_id"]]
        records.append(
            {
                "requirement_id": row["requirement_id"],
                "source_policy": row["source_policy"],
                "requirement_text": row["requirement_text"],
                "updated_2026_status": row["updated_2026_status"],
                "evidence_url": row["evidence_url"],
                "evidence_title": row["evidence_title"],
                "evidence_date": row["evidence_date"],
                "verification_confidence": row["verification_confidence"],
                "audit_decision": decision["audit_decision"],
                "audit_reason": decision["audit_reason"],
                "recommended_status": decision["recommended_status"],
                "requires_manual_review": decision["requires_manual_review"],
            }
        )

    return pd.DataFrame(records)


def main() -> None:
    audit = build_row_audit()
    output_path = project_path("data", "processed", "row_audit_2026.csv")
    save_csv(audit, output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
