# Replication and 2026 Update of U.S. Federal AI Governance Implementation

## Overview

This repository contains a replication-focused portfolio project based on:

**Lawrence, Cui, and Ho (2023). _The Bureaucratic Challenge to AI Governance: An Empirical Assessment of Implementation at U.S. Federal Agencies_.**

The project aims to:

1. Reproduce the original paper's main implementation-status findings.
2. Extend the analysis with a July 2026 update using publicly available evidence.

## Research Questions

1. Can the original paper's main implementation-status results be reproduced?
2. What changed by July 2026 using publicly available evidence?
3. Which federal AI governance requirements remain difficult to verify publicly?

## Original Study

The original paper assessed the implementation of three major U.S. federal AI governance pillars:

- Executive Order 13859, **Maintaining American Leadership in Artificial Intelligence**
- Executive Order 13960, **Promoting the Use of Trustworthy Artificial Intelligence in the Federal Government**
- The **AI in Government Act of 2020**

The authors examined implementation using public materials gathered between late October and mid-November 2022. Their top-line finding was that fewer than 40 percent of the 45 legal requirements they tracked could be publicly verified as implemented.

## Current Project Scope

This repository is being built in two layers:

- A **weekend MVP** that reproduces the core implementation-status result and builds a July 2026 update workflow
- An **optional full replication extension** that can later expand into deeper agency-level tracking

## Data

The repository currently includes:

- `data/raw/source_documents_log.csv` for logging the paper and official policy sources
- `data/raw/original_requirements.csv` with the 45-row original replication baseline
- `data/processed/requirements_coded_2026.csv` for the updated coded dataset
- `data/processed/implementation_status_summary.csv` generated from the 45-row baseline

## Methodology

The project follows the paper's basic logic:

1. Identify line-level legal or policy requirements.
2. Categorize them by policy source and requirement type.
3. Use public evidence to determine whether a requirement appears implemented, partially implemented, not implemented, or not publicly verifiable.
4. Compare the original paper's findings against a July 2026 update.

This repository uses a structured coding workflow so that the evidence trail remains auditable.

## Policy Context for the 2026 Update

The 2026 update will not treat the policy environment as static.

In particular:

- Executive Order 14110 added a major new federal AI governance layer in late 2023.
- OMB Memorandum M-24-10 added agency-use guidance in March 2024.
- Executive Order 14110 was revoked on January 20, 2025.
- Executive Order 14179 and OMB Memoranda M-25-21 and M-25-22 reshaped the federal AI policy environment in 2025.

That means the update phase must distinguish between:

- true non-implementation,
- partial implementation,
- requirements that became harder to verify publicly, and
- requirements whose policy environment changed materially after the original study.

## Results

Current progress:

- Source log seeded with the core paper and official policy documents
- Original 45-row requirement-level dataset extracted from the appendix tracker
- Original paper summary metrics regenerated from the requirement-level dataset
- Reproducible analysis scaffolding added in `src/` and `notebooks/`
- Original-status chart regenerated from the dataset-derived summary

The 2026 coding pass has **not** started yet. The repository is intentionally paused at the validated original-replication baseline.

## Limitations

This project shares a core limitation with the original paper: it relies heavily on **publicly available evidence**.

That makes the project strong for measuring transparency and visible implementation, but it may undercount actions that occurred internally and were not clearly disclosed.

## How to Reproduce

1. Create a Python environment.
2. Install dependencies from `requirements.txt`.
3. Use the notebooks in order:
   - `01_build_requirement_dataset.ipynb`
   - `02_reproduce_original_results.ipynb`
   - `03_update_2026_status.ipynb`
   - `04_visualizations.ipynb`
4. Use the helper modules in `src/` for validation and chart generation.

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
