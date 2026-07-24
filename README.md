# Replication and July 24, 2026 Update of U.S. Federal AI Governance Implementation

## Overview

This repository contains a replication-focused portfolio project based on:

**Lawrence, Cui, and Ho (2023). _The Bureaucratic Challenge to AI Governance: An Empirical Assessment of Implementation at U.S. Federal Agencies_.**

The project has two linked goals:

1. Reproduce the paper's original implementation-status baseline as transparently as possible.
2. Extend that baseline with a conservative requirement-level update coded on Friday, July 24, 2026, using only public evidence.

## Research Questions

1. Can the original paper's main implementation-status results be reproduced from a requirement-level dataset?
2. What changed by July 24, 2026, when the same baseline is re-evaluated using public evidence?
3. Which federal AI governance requirements still remain difficult to verify publicly?

## Original Study

The original paper assessed implementation across three major U.S. federal AI governance pillars:

- Executive Order 13859, **Maintaining American Leadership in Artificial Intelligence**
- Executive Order 13960, **Promoting the Use of Trustworthy Artificial Intelligence in the Federal Government**
- The **AI in Government Act of 2020**

The authors used public materials gathered in late October through mid-November 2022 and concluded that fewer than 40 percent of the 45 counted legal requirements could be publicly verified as implemented.

## Current Project Scope

This repository is structured in two layers:

- A **weekend MVP** that reproduces the original baseline and completes a traceable July 24, 2026 coding pass
- An **optional full replication extension** that can later expand into deeper agency-level tracking and validation

## Data

The repository currently includes:

- `data/raw/source_documents_log.csv` for the paper, original policy texts, and official update-period sources
- `data/raw/original_requirements.csv` with the full appendix tracker plus counted-baseline flags
- `data/processed/implementation_status_summary.csv` generated from the original counted baseline
- `data/processed/requirements_coded_2026.csv` with preserved baseline fields plus the July 24, 2026 coding layer
- `data/processed/implementation_status_summary_2026.csv` with both the comparable 45-row summary and the full 46-row tracker summary
- `outputs/tables/requirement_status_table_2026.csv` and `outputs/tables/summary_table_2026.csv` for export-ready tables

## Methodology

The project follows the paper's basic logic:

1. Identify requirement-level legal or policy obligations.
2. Categorize them by source policy and responsible entity.
3. Preserve the original appendix-derived and aggregate-baseline fields.
4. Add a separate July 24, 2026 coding layer using only official public evidence.
5. Compare the original baseline against the 2026 update without overwriting the paper-era fields.

The 2026 pass uses six update categories:

- `Implemented`
- `Partially implemented`
- `Not implemented`
- `Unable to verify`
- `Superseded or replaced`
- `No longer applicable`

Two guardrails shape the update:

- The original paper baseline is preserved and never silently rewritten.
- If public evidence is weak or indirect, the row is coded as `Unable to verify` or assigned lower confidence instead of being pushed into `Implemented`.

## Policy Context for the 2026 Update

The update does not treat the policy environment as static.

- Executive Order 14110 added a major new federal AI governance layer in 2023.
- OMB Memorandum M-24-10 added agency-use guidance in 2024.
- Executive Order 14110 was revoked on January 20, 2025.
- Executive Order 14179 and OMB Memoranda M-25-21 and M-25-22 reshaped the federal AI policy environment in 2025.
- A White House national-security AI directive added another major layer on June 5, 2026.

Those later documents are used as **update-context sources only**, not as original replication sources.

## Results

Current progress:

- Source log expanded with the original paper, original policy pillars, and official update-period sources
- Original appendix tracker reconstructed at 46 rows, including the explicitly excluded `EO13960 section 5(c)(ii)` row
- Counted baseline regenerated at 45 included requirements using `aggregate_count_included`
- Original paper summary metrics regenerated from the requirement-level dataset
- July 24, 2026 requirement-level coding completed in `data/processed/requirements_coded_2026.csv`
- 2026 summary, comparison, status-change, and confidence charts regenerated from the coded dataset

## July 24, 2026 Findings

Using the same 45 counted baseline requirements as the original paper, the update finds:

- `12` implemented (`26.7%`)
- `12` partially implemented (`26.7%`)
- `15` unable to verify (`33.3%`)
- `6` superseded or replaced (`13.3%`)
- `0` not implemented

Interpretation:

- The public record is stronger in 2026 than it was in the original November 2022 baseline, especially for several guidance and workforce requirements.
- A large share of the tracker still cannot be verified conservatively from public evidence alone.
- Several obligations are now better coded as superseded by later policy instruments such as `M-25-21`, `M-25-22`, and the June 5, 2026 national-security directive rather than being forced into the original implementation categories.
- The confidence mix is intentionally cautious across the 45 counted requirements: `7` high-confidence rows, `21` medium-confidence rows, and `17` low-confidence rows.

## Validation Note

The paper contains a small but important internal inconsistency.

- The appendix tracker structure supports **46 tracker rows**.
- Footnote 8 explicitly excludes `EO13960 section 5(c)(ii)` from the aggregate baseline because its deadline had not yet passed.
- After applying that exclusion, the counted baseline is **45 requirements** and reproduces **12 implemented, 26 unknown, and 7 not implemented**.
- The paper's narrative sentence in Section 5 says **11 implemented**, but that value does not match the appendix-derived baseline or the percentages shown in Table 1.

To keep the project transparent, the dataset preserves:

- the appendix-facing status in `appendix_status`
- the counted-baseline logic in `aggregate_count_included`
- the published prose count as a documented paper-level inconsistency rather than a silent data override

## Limitations

This project shares a core limitation with the original paper: it relies heavily on **publicly available evidence**.

That makes the project strong for measuring transparency and visible implementation, but it may undercount actions that occurred internally and were not clearly disclosed.

The July 24, 2026 update is especially conservative. In several rows, later federal AI policy clearly exists, but the public record does not cleanly prove full completion of the original underlying requirement. Those rows are therefore left at `Partially implemented` or `Unable to verify`.

## How to Reproduce

1. Create a Python environment.
2. Install dependencies from `requirements.txt`.
3. Use the notebooks in order:
   - `01_build_requirement_dataset.ipynb`
   - `02_reproduce_original_results.ipynb`
   - `03_update_2026_status.ipynb`
   - `04_visualizations.ipynb`
4. Use the helper modules in `src/` for validation and chart generation.
5. Regenerate the July 24, 2026 coded update and figures with `src/build_2026_update_artifacts.py`.

## Repository Structure

```text
data/
notebooks/
outputs/
report/
src/
```

## Citation

Lawrence, Christie, Isaac Cui, and Daniel E. Ho. 2023. _The Bureaucratic Challenge to AI Governance: An Empirical Assessment of Implementation at U.S. Federal Agencies_. Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society (AIES '23). https://doi.org/10.1145/3600211.3604701
