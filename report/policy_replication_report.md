# Policy Replication Report

## Introduction

This project reproduces and extends the main findings of Lawrence, Cui, and Ho's 2023 paper on U.S. federal AI governance implementation.

## Original Paper Summary

The original paper studied three major federal AI governance pillars and found that, based on public evidence available as of November 2022, only a minority of tracked legal requirements could be verified as implemented.

## Replication Approach

The replication work in this repository proceeds in two stages:

1. Reproduce the paper's top-line implementation summary using structured data and reusable analysis code.
2. Build a requirement-level dataset that supports a July 2026 update.

## 2026 Update Methodology

The update phase will use publicly available evidence from official federal sources, including executive orders, OMB memoranda, agency guidance, and agency AI-related disclosures.

## Findings

Current status:

- Core source documents have been logged.
- The original paper's top-line summary has been captured in machine-readable form.
- The repository now contains reusable helpers for validation and chart generation.

## Interpretation

The first wave of work focuses on reproducibility and auditability, so that later policy judgments rest on a traceable dataset rather than ad hoc notes.

## Limitations

The project depends on public evidence and will likely under-observe internal actions that were not publicly disclosed.

## Next Steps

The next implementation step is to extract the original requirement-level tracker into `data/raw/original_requirements.csv` and begin coding the July 2026 update row by row.
