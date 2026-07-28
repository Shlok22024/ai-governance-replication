# Data Dictionary

## Raw Data

### `raw/original_requirements.csv`

Requirement-level extraction from the original paper and counted-baseline reconciliation.

Fields:

- `requirement_id`: Stable identifier for a requirement row.
- `source_policy`: Original legal or policy source tracked by the paper.
- `requirement_text`: Requirement text summarized from the original source and appendix.
- `responsible_entity`: Agency, office, or actor responsible for the requirement.
- `deadline`: Original requirement deadline or cadence.
- `original_status`: Earlier extraction-era status field preserved for project history.
- `aggregate_count_included`: `Yes` if the row belongs to the paper's 45-row counted baseline, `No` otherwise.
- `original_evidence_notes`: Notes from the original extraction pass.
- `appendix_status`: Status label reflected in the appendix-facing tracker logic.
- `aggregate_status`: Counted-baseline status used for the replication summary.
- `validation_note`: Reconciliation note for appendix versus aggregate handling.

Notes:

- The appendix tracker contains 46 rows.
- The counted baseline contains 45 included requirements because `EO13960 section 5(c)(ii)` is explicitly excluded by the paper's footnote 8.

### `raw/source_documents_log.csv`

Log of public legal, policy, and agency sources used in the original replication and the 2026 update.

Fields:

- `document_id`: Stable document identifier used in the project log.
- `document_title`: Public title of the document or page.
- `document_type`: Short document-type label.
- `issuing_body`: Issuing organization or office.
- `publication_date`: Publication or access date in `YYYY-MM-DD` format.
- `url`: Canonical public URL used in the project.
- `relevance_to_project`: How the source is used in the project.
- `notes`: Additional source-handling notes.

### `raw/agency_ai_inventory_links.csv`

Reference list for agency AI inventory pages and related public sources.

## Processed Data

### `processed/requirements_coded_2026.csv`

Main audited July 24, 2026 update dataset, preserving the original baseline fields and adding the 2026 coding layer.

Fields:

- `requirement_id`: Stable requirement identifier.
- `source_policy`: Original source policy tracked by the paper.
- `requirement_text`: Requirement text used in the coding workflow.
- `responsible_entity`: Agency, office, or actor responsible for the requirement.
- `deadline`: Original requirement deadline or cadence.
- `appendix_status`: Appendix-facing baseline status.
- `aggregate_status`: Counted-baseline status used for comparison against the paper.
- `aggregate_count_included`: Whether the row is included in the comparable 45-row baseline.
- `updated_2026_status`: Audited 2026 status using public evidence.
- `status_change`: Human-readable comparison label between the baseline and the 2026 status.
- `evidence_url`: Public source URL used for the 2026 status.
- `evidence_title`: Public title of the cited 2026 source.
- `evidence_date`: Publication or access date for the cited source.
- `evidence_source_type`: Short label describing the type of public evidence.
- `verification_confidence`: Confidence rating for the 2026 coding decision.
- `update_notes`: Short justification for the 2026 coding decision.
- `superseded_or_replaced`: `Yes` if the requirement is coded as clearly superseded or replaced, otherwise `No`.
- `replacement_policy_source`: Later policy source that replaced or absorbed the original requirement, if applicable.

### `processed/implementation_status_summary_2026.csv`

Summary table for the audited 2026 update, including both the comparable counted baseline and the full 46-row tracker view.

Fields:

- `summary_basis`: Summary slice identifier, such as `comparable_baseline_45` or `full_tracker_46`.
- `instrument`: Policy-source grouping or `Total`.
- `tracker_rows`: Number of tracker rows associated with the instrument in the full dataset.
- `excluded_count`: Number of rows excluded from the counted baseline for that instrument.
- `total_requirements`: Number of rows included in the summary slice for that instrument.
- `notes`: Explanation of how the summary slice should be interpreted.
- `implemented_count`: Count of rows coded `Implemented`.
- `implemented_pct`: Percentage of rows coded `Implemented`.
- `partially_implemented_count`: Count of rows coded `Partially implemented`.
- `partially_implemented_pct`: Percentage of rows coded `Partially implemented`.
- `unable_to_verify_count`: Count of rows coded `Unable to verify`.
- `unable_to_verify_pct`: Percentage of rows coded `Unable to verify`.
- `not_implemented_count`: Count of rows coded `Not implemented`.
- `not_implemented_pct`: Percentage of rows coded `Not implemented`.
- `superseded_or_replaced_count`: Count of rows coded `Superseded or replaced`.
- `superseded_or_replaced_pct`: Percentage of rows coded `Superseded or replaced`.
- `no_longer_applicable_count`: Count of rows coded `No longer applicable`.
- `no_longer_applicable_pct`: Percentage of rows coded `No longer applicable`.

### `processed/row_audit_2026.csv`

Focused audit table for the highest-risk July 24, 2026 row-level decisions reviewed on Monday, July 27, 2026.

Fields:

- `requirement_id`: Stable requirement identifier.
- `source_policy`: Original source policy tracked by the paper.
- `requirement_text`: Requirement text used during audit review.
- `updated_2026_status`: Pre-audit status from the committed July 24, 2026 coded dataset.
- `evidence_url`: Public evidence URL reviewed during the audit.
- `evidence_title`: Public title of the audited evidence source.
- `evidence_date`: Publication or access date for the audited evidence source.
- `verification_confidence`: Pre-audit confidence label.
- `audit_decision`: Audit action taken or recommended.
- `audit_reason`: Short explanation for the audit decision.
- `recommended_status`: Final recommended status after audit review.
- `requires_manual_review`: Whether the row still needs manual review.

### `processed/implementation_status_summary.csv`

Original-baseline replication summary generated from `raw/original_requirements.csv`.

### `processed/agency_inventory_status.csv`

Optional extension dataset reserved for future agency-level inventory tracking.
