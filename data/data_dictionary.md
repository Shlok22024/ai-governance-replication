# Data Dictionary

## Raw Data

### `original_requirements.csv`

Requirement-level extraction from the original paper.

Expected fields:

- `requirement_id`
- `source_policy`
- `requirement_text`
- `responsible_entity`
- `deadline`
- `original_status`
- `aggregate_count_included`
- `original_evidence_notes`
- `appendix_status`
- `aggregate_status`
- `validation_note`

Notes:

- The appendix tracker contains 46 rows.
- The counted baseline contains 45 included requirements because `EO13960 §5(c)(ii)` is explicitly excluded by the paper's footnote 8.
- `appendix_status` preserves the tracker-facing label.
- `aggregate_count_included` and `aggregate_status` preserve the counted-baseline logic used for the summary.

### `source_documents_log.csv`

Log of legal, policy, and agency source documents used in the replication and 2026 update.

Expected fields:

- `document_id`
- `document_title`
- `document_type`
- `issuing_body`
- `publication_date`
- `url`
- `relevance_to_project`
- `notes`

### `agency_ai_inventory_links.csv`

Reference table for agency AI inventory pages and related public sources.

## Processed Data

### `requirements_coded_2026.csv`

Main coded dataset combining original statuses with July 2026 public-evidence updates.

Expected fields:

- `requirement_id`
- `source_policy`
- `requirement_text`
- `responsible_entity`
- `requirement_type`
- `deadline`
- `original_status`
- `updated_2026_status`
- `status_change`
- `evidence_url`
- `evidence_date`
- `verification_confidence`
- `notes`

### `implementation_status_summary.csv`

Summary metrics used for charts and reporting.

This file is now generated directly from `original_requirements.csv`.

Expected fields:

- `summary_basis`
- `instrument`
- `tracker_rows`
- `excluded_count`
- `total_requirements`
- `implemented_count`
- `unknown_count`
- `not_implemented_count`
- `implemented_pct`
- `unknown_pct`
- `not_implemented_pct`
- `notes`

Notes:

- `appendix_all_rows` shows the appendix tracker with the excluded row explicitly tracked.
- `aggregate_included_rows` shows the 45-requirement counted baseline used for replication.
- `paper_published_narrative` stores the paper's prose claim of `11 implemented, 26 unknown, 7 not implemented`, which does not match the appendix-derived counted baseline.

### `agency_inventory_status.csv`

Optional extension dataset for agency inventory tracking.
