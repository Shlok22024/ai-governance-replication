# Data Dictionary

## Raw Data

### `original_requirements.csv`

Requirement-level extraction from the original paper.

Expected fields:

- `requirement_id`
- `source_policy`
- `requirement_text`
- `responsible_entity`
- `requirement_type`
- `deadline`
- `original_status`
- `paper_evidence_notes`

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

This file currently stores the original paper's top-line implementation summary so that the first analysis notebook and initial figure can be reproduced before the full requirement dataset is completed.

### `agency_inventory_status.csv`

Optional extension dataset for agency inventory tracking.
