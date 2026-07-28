# Policy Replication Report

## Overview

This project studies the requirement-level analysis behind Lawrence, Cui, and Ho's 2023 AIES paper on U.S. federal AI governance implementation. It does three things:

1. Reconstruct the appendix-derived counted baseline from the paper.
2. Recode the same 45 counted requirements independently using public evidence that would reasonably have been available by November 15, 2022.
3. Compare that baseline with a limited public-evidence update coded on July 24, 2026.

The goal is not to claim a full end-to-end replication of every part of the paper. The goal is to understand how the requirement-level coding works, where coding judgments matter, and what can still be said from public evidence in 2026.

## Paper Studied

Lawrence, Christie, Isaac Cui, and Daniel E. Ho. 2023. _The Bureaucratic Challenge to AI Governance: An Empirical Assessment of Implementation at U.S. Federal Agencies_. Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society (AIES '23).

The paper tracks implementation across:

- Executive Order 13859
- Executive Order 13960
- The AI in Government Act of 2020

## Method

### Appendix audit

The first step reconstructs the paper's requirement tracker as a structured dataset. This produces a 46-row appendix tracker and a 45-row counted baseline after excluding `EO13960 section 5(c)(ii)`, consistent with the paper's own footnote.

### Independent baseline recoding

The second step recodes the 45 counted requirements using public evidence that would reasonably have been available by November 15, 2022.

This second-pass coding used `original_requirements.csv` as a requirement list during assignment and joined the appendix statuses back only after the row-level coding was complete. It was designed to reduce direct dependence on the appendix labels during assignment, but it was not a formal blinded study because the appendix reconstruction had already been completed earlier in the project.

### July 24, 2026 public-evidence update

The third step preserves the paper-era baseline and adds a separate 2026 coding layer. This update uses only public evidence and is intentionally conservative. If a requirement cannot be verified clearly from public documents, the row is held at `Unable to verify` rather than being pushed into a stronger claim.

The 2026 review should therefore be read as a limited public-evidence update, not as proof of agency noncompliance.

## Findings

### 1. Appendix-derived baseline vs paper prose

The reconstructed counted baseline supports:

- `12` implemented
- `26` unknown
- `7` not implemented

The paper's prose reports `11` implemented requirements. This repository treats that as a documented paper-level inconsistency between prose and appendix-derived counts, rather than silently forcing the row-level data to match the prose.

### 2. Independent second-pass recoding

The independent second-pass recoding produced:

- `11` implemented
- `3` not implemented
- `30` unknown or unable to verify
- `1` excluded because the deadline had not passed

Agreement with the paper appendix was `38 of 45`, or `84.4%`, with `κ = 0.71`.

This matters because it shows that the underlying requirement set is close to the paper's, while also showing how sensitive the final labels are to the treatment of missing public evidence. Under a stricter public-evidence rule, several paper-era `Not implemented` rows are more defensibly treated as unresolved uncertainty.

### 3. July 24, 2026 public-evidence update

On the same 45 counted requirements, the July 24, 2026 update finds:

- `12` implemented
- `8` partially implemented
- `24` unable to verify
- `1` superseded or replaced
- `0` not implemented

This update should be interpreted carefully. It is a requirement-level review of public evidence, not a comprehensive agency compliance determination.

### 4. July 27, 2026 row audit

The row audit reviewed `36` high-risk rows and downgraded `9` of them to `Unable to verify`.

The most important effect of the audit was not to produce a more dramatic result. It was to make the 2026 layer more conservative by pulling back rows that relied on broad strategic pages, indirect policy context, or weak supersession claims.

## Interpretation

Three conclusions stand out.

First, the appendix-derived baseline supports the paper's broad transparency claim, but not its exact prose count of implemented requirements.

Second, the independent second-pass recoding shows that some apparently sharp `Not implemented` judgments soften under a stricter public-evidence interpretation. The result is fewer `Not implemented` rows and more `Unknown / Unable to verify` rows.

Third, the 2026 update suggests that some requirements are easier to describe than they were in late 2022, but a large portion of the baseline still cannot be verified conservatively from public evidence alone.

## Limitations

This project relies on public source evidence and therefore under-observes actions that may have happened internally but were not publicly documented.

That limitation affects both the second-pass baseline recoding and the July 24, 2026 update.

The 2026 layer is especially scoped. It does not attempt a full agency-level replication of the original paper's broader implementation environment.

## AI Assistance Disclosure

AI assistance was used for repository scaffolding, code generation, source-search support, and draft organization. Coding decisions and interpretation were reviewed by the project author against public source evidence.
