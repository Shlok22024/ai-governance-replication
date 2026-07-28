# Data Dictionary

This file explains the main project files in plain language.

A simple way to think about the project is this:

- the paper is a checklist
- the datasets are spreadsheet versions of that checklist
- each row is one requirement
- each column answers a question about that requirement

## Raw data

### `raw/original_requirements.csv`

This is the rebuilt checklist from the original paper.

Each row is one requirement from a law, executive order, or memo.

Main columns:

- `requirement_id`: a short ID for the row
- `source_policy`: which law, executive order, or memo the row comes from
- `requirement_text`: the requirement written in plain text
- `responsible_entity`: who was supposed to do it
- `deadline`: when it was supposed to happen, if the rule gave a date
- `appendix_status`: the status shown by the paper's appendix logic
- `aggregate_status`: the status used in the paper's counted baseline
- `aggregate_count_included`: whether the row is part of the paper's 45 counted rows
- `validation_note`: notes about how the row was handled during the rebuild

Helpful note:

- The full tracker has `46` rows.
- The paper's counted baseline uses `45` rows because one row was excluded by the paper's own footnote.

### `raw/source_documents_log.csv`

This is the source list for the project.

It works like a reading log. It records the public documents, web pages, PDFs, and government sources used during the project.

Main columns:

- `document_id`: source ID
- `document_title`: title of the document or page
- `document_type`: what kind of source it is
- `issuing_body`: who published it
- `publication_date`: when it was published
- `url`: where it can be found
- `relevance_to_project`: why it matters for this project
- `notes`: extra notes

### `raw/agency_ai_inventory_links.csv`

This is a simple reference list of agency AI inventory pages and related links.

## Processed data

### `processed/original_second_pass_recoding.csv`

This file contains my own second check of the 45 counted requirements.

Think of it like grading the same checklist a second time and then comparing answers.

Main columns:

- `requirement_id`: row ID
- `source_policy`: which law, executive order, or memo it comes from
- `requirement_text`: the requirement itself
- `responsible_entity`: who was supposed to do it
- `deadline`: timing for the requirement
- `replication_status`: my answer for that row
- `replication_evidence_url`: the main public source I used
- `replication_evidence_date`: date of that source
- `replication_notes`: short explanation of my decision
- `paper_appendix_status`: the paper's appendix answer for the same row
- `agreement_with_paper`: whether my answer matched the paper
- `discrepancy_reason`: short explanation when the answers did not match

### `processed/second_pass_recoding_status_summary.csv`

This is the simple count table for my second check.

It tells you how many rows ended up as:

- implemented
- not implemented
- unknown or unable to verify
- excluded because the deadline had not passed

### `processed/second_pass_recoding_vs_paper_comparison.csv`

This file compares my second check with the paper's appendix.

You can think of it like a score table showing where two graders matched and where they did not.

### `processed/second_pass_recoding_agreement_rate.md`

This is a short plain-English summary of the agreement result, including:

- how many rows matched
- the percent agreement
- Cohen's kappa

### `processed/implementation_status_summary.csv`

This is the baseline count table rebuilt from the paper's checklist.

It is the file that supports the finding that the appendix-based count is `12` implemented even though the paper's prose says `11`.

### `processed/requirements_coded_2026.csv`

This is the July 24, 2026 update file.

It keeps the original baseline columns and adds a newer check based on later public records.

Main columns:

- `requirement_id`: row ID
- `source_policy`: which law, executive order, or memo it comes from
- `requirement_text`: the requirement itself
- `responsible_entity`: who was supposed to do it
- `deadline`: timing for the requirement
- `appendix_status`: paper appendix answer
- `aggregate_status`: baseline counted answer
- `aggregate_count_included`: whether the row is in the 45 counted baseline
- `updated_2026_status`: what the row looked like when I checked newer public records
- `status_change`: how the 2026 result compares with the baseline
- `evidence_url`: main public source used for the 2026 check
- `evidence_title`: title of that source
- `evidence_date`: date of that source
- `evidence_source_type`: what kind of source it is
- `verification_confidence`: confidence label from the 2026 coding pass
- `update_notes`: short explanation of the 2026 decision
- `superseded_or_replaced`: whether a newer rule clearly replaced the older one
- `replacement_policy_source`: the newer rule, if there is one

Important note:

- `Unable to verify` means I could not confirm it from public records.
- It does **not** automatically mean the work was not done.

### `processed/implementation_status_summary_2026.csv`

This is the count table for the July 24, 2026 update.

It summarizes how many rows looked:

- implemented
- partly implemented
- unclear from public records
- not implemented
- replaced by a newer rule

### `processed/row_audit_2026.csv`

This is the follow-up review of the hardest 2026 rows.

Think of it like checking the toughest answers one more time before finalizing the spreadsheet.

Main columns:

- `requirement_id`: row ID
- `updated_2026_status`: the earlier 2026 answer
- `audit_decision`: what the audit decided to do
- `audit_reason`: why
- `recommended_status`: the final suggested answer after the audit

### `processed/summary_stats.md`

This is the short summary file for the whole project.

It gives the main numbers used in the README and report, including:

- the paper's appendix-based counts
- my second-check counts
- the agreement result
- the 2026 counts
- the row-audit counts

### `processed/agency_inventory_status.csv`

This is a leftover exploration file from earlier work.

It is not part of the main story of the project.
