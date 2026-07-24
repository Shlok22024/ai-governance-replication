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
- The full appendix tracker has been reconstructed at 46 rows, including the excluded `EO13960 §5(c)(ii)` row.
- The counted baseline is 45 included requirements after applying the paper's own exclusion logic.
- The original-status summary and chart are now generated from that dataset rather than from seeded values.
- The repository now contains reusable helpers for validation and chart generation.

## Interpretation

The first wave of work focuses on reproducibility and auditability, so that later policy judgments rest on a traceable dataset rather than ad hoc notes.

## Validation Note

The reconciliation task surfaced two distinct issues:

1. The exact appendix row mentioned in footnote 8, `EO13960 §5(c)(ii)`, was missing from the earlier extraction and is now restored.
2. Once that row is restored and excluded from the counted baseline, the dataset reproduces **12 implemented, 26 unknown, and 7 not implemented** across 45 counted requirements.

That means the paper's narrative sentence reporting **11 implemented** does not appear to be caused by the appendix row structure. The repository therefore treats the `11` count as a documented narrative inconsistency in the paper rather than forcing the row-level data to match it silently.

## Limitations

The project depends on public evidence and will likely under-observe internal actions that were not publicly disclosed.

## Next Steps

The next implementation step is to begin the July 2026 coding pass row by row. That work has not started yet.
