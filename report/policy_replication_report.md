# Policy Replication Report

## Introduction

This project reconstructs, stress-tests, and extends the main findings of Lawrence, Cui, and Ho's 2023 paper on U.S. federal AI governance implementation.

This deliverable is a **Phase 1 MVP**, not a full replication of every component of the original paper.

## Original Paper Summary

The original paper studied three major federal AI governance pillars and found that, based on public evidence available as of November 2022, only a minority of tracked legal requirements could be verified as implemented.

## Replication Approach

The replication work in this repository proceeds in three stages:

1. Reconstruct the appendix tracker and the 45-row counted baseline.
2. Run an independent blind recoding pass using only public evidence that would reasonably have been available by November 15, 2022.
3. Build a requirement-level dataset that supports a conservative public-evidence update coded on Friday, July 24, 2026.

## Blind Recoding Methodology

The Phase 1B blind recode is meant to behave more like an actual replication exercise than a simple appendix transcription.

- The coding pass used `original_requirements.csv` only as a requirement list during assignment.
- The blind pass did **not** use `appendix_status` or `aggregate_status` while assigning `replication_status`.
- After all 45 counted rows were coded, the appendix-era status labels were joined back for agreement analysis.

The blind pass used four categories:

- `Implemented`
- `Not implemented`
- `Unknown / Unable to verify`
- `Excluded because deadline had not passed`

This step matters because it separates two questions that can otherwise get blurred together:

1. What status does the appendix appear to assign?
2. What status would an independent coder assign from public evidence alone?

## 2026 Update Methodology

The update phase uses only publicly available evidence from official federal sources, including executive orders, OMB memoranda, agency guidance, and agency AI-related disclosures.

Two coding rules matter most:

- The original baseline fields remain untouched so the paper replication and the 2026 update can be compared side by side.
- Weak or indirect public evidence is treated conservatively. When the public record does not clearly prove completion, the row is coded as `Unable to verify` or given lower confidence rather than upgraded aggressively.

## Findings

The repository now has three substantive findings layers: the appendix reconstruction, the blind recode, and the July 24, 2026 update.

### Blind Recoding

- The blind pass coded all `45` counted requirements using a November 15, 2022 public-evidence cutoff.
- It found `11` implemented rows, `3` not implemented rows, `30` rows that remained unknown or unable to verify, and `1` row treated as excluded because its deadline had not yet been triggered.
- After normalizing label names, the blind pass agreed with the paper appendix on `38` of `45` rows, for an `84.4%` agreement rate.
- The main disagreements came from the blind pass being more conservative about inferring public noncompliance from silence and more cautious about deadline-trigger logic for follow-on requirements.

### July 24, 2026 Update

The July 24, 2026 coding pass is complete, and a focused row audit was applied on Monday, July 27, 2026.

- The full appendix tracker remains at 46 rows, including the excluded `EO13960 section 5(c)(ii)` row.
- The comparable baseline remains 45 counted requirements after applying the paper's own exclusion logic.
- On that 45-row baseline, the post-audit coded update finds that public evidence supports `12` implemented requirements, `8` partially implemented requirements, `24` requirements that remain unable to verify, and `1` requirement that is clearly superseded or replaced.
- No counted requirement is coded `Not implemented` in 2026. That does not mean every obligation is complete; it reflects the deliberate choice to avoid over-classifying weak public evidence.
- The row audit reviewed `36` high-risk rows and downgraded `9` of them to `Unable to verify`.

## Interpretation

The combined results suggest a mixed picture rather than a simple success story.

- The appendix reconstruction and blind recode are close enough to show that the project is tracking the same underlying requirement set as the paper.
- The seven disagreements are analytically useful: they show where public-evidence coding choices, deadline logic, and whole-of-government assumptions materially affect the baseline.
- In particular, the blind pass is less willing to call a row `Not implemented` when the obligation could have been satisfied internally but not publicly documented.

- Some requirements clearly moved forward, especially the guidance and workforce pieces connected to the AI in Government Act.
- Several `Unknown` baseline rows can still be described more precisely than they were in 2022, but the audit showed that some earlier partial or superseded judgments were not supported strongly enough by direct public evidence.
- A large share of the tracker still cannot be verified conservatively from public evidence alone, which keeps transparency and observability at the center of the project.
- Policy change still matters, but the audit applied a stricter standard for `Superseded or replaced` and retained that label only where the newer public requirement clearly absorbed the older coordination function.

## Validation Note

The reconciliation task surfaced two distinct issues:

1. The exact appendix row mentioned in footnote 8, `EO13960 section 5(c)(ii)`, was missing from the earlier extraction and is now restored.
2. Once that row is restored and excluded from the counted baseline, the dataset reproduces **12 implemented, 26 unknown, and 7 not implemented** across 45 counted requirements.

That means the paper's narrative sentence reporting **11 implemented** does not appear to be caused by the appendix row structure. The repository therefore treats the `11` count as a documented narrative inconsistency in the paper rather than forcing the row-level data to match it silently.

## Limitations

The project depends on public evidence and will likely under-observe internal actions that were not publicly disclosed.

That limitation is especially important for both the blind recode and the July 24, 2026 pass.

- In the blind pass, a more cautious standard shifts several rows from paper-era `Not implemented` or `Implemented` calls into `Unknown / Unable to verify`.
- In the 2026 pass, several rows likely reflect real implementation activity that is not yet documented cleanly enough on public-facing government pages to justify stronger coding.

The July 27 audit intentionally sharpened that constraint. If the evidence was strategic, indirect, agency-specific, or merely suggestive of later policy evolution, the row was pushed back toward `Unable to verify` rather than left in a more assertive status.

## Next Steps

Phase 1 is complete.

Phase 2 is future extension work focused on agency-level depth rather than baseline publication polish:

- Expand the project into a deeper agency-level validation workflow.
- Add a more complete agency inventory and compliance-plan extension dataset.
- Build the planned dashboard and other agency-comparison outputs on top of the audited Phase 1 baseline.
