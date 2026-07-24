# Policy Replication Report

## Introduction

This project reproduces and extends the main findings of Lawrence, Cui, and Ho's 2023 paper on U.S. federal AI governance implementation.

## Original Paper Summary

The original paper studied three major federal AI governance pillars and found that, based on public evidence available as of November 2022, only a minority of tracked legal requirements could be verified as implemented.

## Replication Approach

The replication work in this repository proceeds in two stages:

1. Reproduce the paper's top-line implementation summary using structured data and reusable analysis code.
2. Build a requirement-level dataset that supports a conservative public-evidence update coded on Friday, July 24, 2026.

## 2026 Update Methodology

The update phase uses only publicly available evidence from official federal sources, including executive orders, OMB memoranda, agency guidance, and agency AI-related disclosures.

Two coding rules matter most:

- The original baseline fields remain untouched so the paper replication and the 2026 update can be compared side by side.
- Weak or indirect public evidence is treated conservatively. When the public record does not clearly prove completion, the row is coded as `Unable to verify` or given lower confidence rather than upgraded aggressively.

## Findings

The July 24, 2026 coding pass is complete.

- The full appendix tracker remains at 46 rows, including the excluded `EO13960 section 5(c)(ii)` row.
- The comparable baseline remains 45 counted requirements after applying the paper's own exclusion logic.
- On that 45-row baseline, the coded update finds `12` implemented, `12` partially implemented, `15` unable to verify, and `6` superseded or replaced.
- No counted requirement is coded `Not implemented` in 2026. That does not mean every obligation is complete; it reflects the deliberate choice to avoid over-classifying weak public evidence.
- Six requirements are now better treated as superseded or replaced by later policy instruments rather than forced into the original implementation categories.

## Interpretation

The update suggests a mixed picture rather than a simple success story.

- Some requirements clearly moved forward, especially the guidance and workforce pieces connected to the AI in Government Act.
- Several `Unknown` baseline rows can now be described more precisely as partially implemented.
- A large share of the tracker still cannot be verified conservatively from public evidence alone, which keeps transparency and observability at the center of the project.
- Policy change also matters: by July 24, 2026, some obligations are more accurately described as superseded by `M-25-21`, `M-25-22`, or the June 5, 2026 national-security AI directive.

## Validation Note

The reconciliation task surfaced two distinct issues:

1. The exact appendix row mentioned in footnote 8, `EO13960 section 5(c)(ii)`, was missing from the earlier extraction and is now restored.
2. Once that row is restored and excluded from the counted baseline, the dataset reproduces **12 implemented, 26 unknown, and 7 not implemented** across 45 counted requirements.

That means the paper's narrative sentence reporting **11 implemented** does not appear to be caused by the appendix row structure. The repository therefore treats the `11` count as a documented narrative inconsistency in the paper rather than forcing the row-level data to match it silently.

## Limitations

The project depends on public evidence and will likely under-observe internal actions that were not publicly disclosed.

That limitation is especially important for the July 24, 2026 pass. Several rows likely reflect real implementation activity that is not yet documented cleanly enough on public-facing government pages to justify stronger coding.

## Next Steps

The immediate next step is review rather than broader expansion:

- Re-check any low-confidence `Partially implemented` assignments to see whether they should remain there or be downgraded to `Unable to verify`.
- Expand the source log if additional official agency inventory or compliance pages are incorporated.
- If the weekend MVP holds up, proceed to the deeper full-replication extension with more agency-level validation and documentation.
