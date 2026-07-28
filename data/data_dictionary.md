# Data Dictionary

## Raw Data

### `raw/original_requirements.csv`

Requirement-level reconstruction of the paper's appendix tracker and counted-baseline logic.

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
- `aggregate_status`: Counted-baseline status used for the baseline summary.
- `validation_note`: Reconciliation note for appendix versus aggregate handling.

Notes:

- The appendix tracker contains `46` rows.
- The counted baseline contains `45` included requirements because `EO13960 section 5(c)(ii)` is explicitly excluded by the paper's footnote 8.

### `raw/source_documents_log.csv`

Log of public legal, policy, and agency sources used in the appendix reconstruction, the independent second-pass recoding, and the 2026 update.

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

### `processed/original_second_pass_recoding.csv`

Independent second-pass recoding table for the 45 counted baseline requirements.

Fields:

- `requirement_id`: Stable requirement identifier.
- `source_policy`: Original source policy tracked by the paper.
- `requirement_text`: Requirement text used during second-pass coding.
- `responsible_entity`: Agency, office, or actor responsible for the requirement.
- `deadline`: Original requirement deadline or cadence.
- `replication_status`: Independent second-pass status using the November 15, 2022 public-evidence cutoff.
- `replication_evidence_url`: Public source URL used in the second pass.
- `replication_evidence_date`: Publication or timing label for the cited second-pass source.
- `replication_notes`: Short justification for the second-pass coding decision.
- `paper_appendix_status`: Appendix-era status joined back only after second-pass coding was complete.
- `agreement_with_paper`: `Agree` or `Disagree` after normalizing label names across the second-pass and appendix status schemes.
- `discrepancy_reason`: Short explanation for disagreements between the second pass and the paper appendix status.

### `processed/second_pass_recoding_status_summary.csv`

Summary table for the independent second-pass recoding.

Fields:

- `replication_status`: Second-pass status category.
- `count`: Number of rows in that category.
- `percentage`: Percentage of the 45 counted rows in that category.
- `cutoff_date`: Public-evidence cutoff date used for the second pass.
- `total_requirements`: Total number of counted baseline rows reviewed in the second pass.

### `processed/second_pass_recoding_vs_paper_comparison.csv`

Cross-tabulation comparing second-pass statuses against the paper appendix statuses after label normalization.

Fields:

- `second_pass_recoding_status`: Row-axis second-pass status.
- `Implemented`: Count of rows whose paper appendix status normalizes to `Implemented`.
- `Not implemented`: Count of rows whose paper appendix status normalizes to `Not implemented`.
- `Unknown / Unable to verify`: Count of rows whose paper appendix status normalizes to `Unknown / Unable to verify`.
- `Excluded because deadline had not passed`: Count of rows whose paper appendix status normalizes to `Excluded because deadline had not passed`.

### `processed/second_pass_recoding_agreement_rate.md`

Short Markdown summary of agreement between the independent second-pass recoding and the paper appendix.

### `processed/implementation_status_summary.csv`

Original-baseline summary generated from `raw/original_requirements.csv`.

### `processed/requirements_coded_2026.csv`

Main July 24, 2026 update dataset, preserving the original baseline fields and adding the 2026 coding layer.

Fields:

- `requirement_id`: Stable requirement identifier.
- `source_policy`: Original source policy tracked by the paper.
- `requirement_text`: Requirement text used in the coding workflow.
- `responsible_entity`: Agency, office, or actor responsible for the requirement.
- `deadline`: Original requirement deadline or cadence.
- `appendix_status`: Appendix-facing baseline status.
- `aggregate_status`: Counted-baseline status used for comparison against the paper.
- `aggregate_count_included`: Whether the row is included in the comparable 45-row baseline.
- `updated_2026_status`: July 24, 2026 status using public evidence.
- `status_change`: Human-readable comparison label between the baseline and the 2026 status.
- `evidence_url`: Public source URL used for the 2026 status.
- `evidence_title`: Public title of the cited 2026 source.
- `evidence_date`: Publication or access date for the cited source.
- `evidence_source_type`: Short label describing the type of public evidence.
- `verification_confidence`: Coding confidence from the July 24, 2026 update pass.
- `update_notes`: Short justification for the 2026 coding decision.
- `superseded_or_replaced`: `Yes` if the requirement is coded as clearly superseded or replaced, otherwise `No`.
- `replacement_policy_source`: Later policy source that replaced or absorbed the original requirement, if applicable.

### `processed/implementation_status_summary_2026.csv`

Summary table for the July 24, 2026 update, including both the comparable counted baseline and the full 46-row tracker view.

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
- `updated_2026_status`: Status from the July 24, 2026 coded dataset.
- `evidence_url`: Public evidence URL reviewed during the audit.
- `evidence_title`: Public title of the audited evidence source.
- `evidence_date`: Publication or access date for the audited evidence source.
- `verification_confidence`: Confidence label carried from the July 24, 2026 coding pass.
- `audit_decision`: Audit action taken or recommended.
- `audit_reason`: Short explanation for the audit decision.
- `recommended_status`: Final recommended status after audit review.
- `requires_manual_review`: Whether the row still needs manual review.

### `processed/summary_stats.md`

Generated Markdown summary of the current authoritative project counts.

Contents:

- Appendix-derived baseline counts
- Independent second-pass recoding counts
- Agreement rate and Cohen's kappa
- July 24, 2026 update counts
- July 27, 2026 row-audit counts

### `processed/agency_inventory_status.csv`

Reserved dataset from earlier exploration. It is not used in the core reproduction workflow described in the README.
