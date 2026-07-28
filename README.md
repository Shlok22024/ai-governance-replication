# Can We See AI Governance Progress?

*A simple reproduction and update of a 2023 study on U.S. federal AI governance*

Governments write a lot of AI rules. But a harder question is: can the public actually check whether those rules were followed?

In this project, I studied a 2023 research paper about U.S. federal AI governance. The paper looked at 45 AI-related government requirements and checked whether each one had been completed, not completed, or could not be verified.

I rebuilt that checklist, checked the paper's counts, did my own second check of the same requirements, and then looked at newer public records from 2026.

The goal was not to prove that agencies failed. The goal was simpler: understand how policy research turns legal text into data, and see how much AI governance progress can be confirmed from public records.

## What this project is

Think of the original paper like a long checklist.

Each requirement is one item on that checklist. My project turns that checklist into a spreadsheet, where each row is one requirement and each column answers simple questions like:

- What did the government say it would do?
- Who was supposed to do it?
- Is there public evidence that it happened?

In other words, this project is about taking legal text and turning it into something we can compare, count, and check.

## Why I did it

I wanted to understand how policy research works at the row-by-row level.

It is easy to read a paper's headline result. It is harder, and more useful, to understand how the authors turned dozens of long legal requirements into a table of answers.

This project let me practice three things at once:

- reading a research paper carefully
- turning policy text into structured data
- checking whether public records support the final claims

## What I found

1. The paper's text says `11` requirements were implemented, but its own appendix supports `12`.
2. My second check agreed with the paper on `38 out of 45` requirements.
3. Some requirements the paper called `not implemented` looked more like `unclear from public records` under a stricter evidence rule.
4. In the 2026 update, many requirements were still hard to confirm from public information.
5. `Unable to verify` does not mean `not done`. It means I could not find enough public evidence to confirm it.

## Why it matters

This matters because AI governance is not just about writing rules. It is also about whether the public can see evidence that those rules were carried out.

A simple analogy is checking receipts after someone says a task was done. If there is no receipt, that does not automatically prove the task never happened. But it does mean an outside reviewer cannot confirm it.

That is the main lesson of this project: public transparency and actual government action are not always the same thing.

## How to read this project

Think of the original paper as a checklist.

Each row asks:

- What did the government say it would do?
- Who was responsible?
- Was there public evidence that it happened?

My project rebuilt that checklist and checked the answers.

You can read the project in three parts:

1. Check the paper's appendix and counts.
2. Compare the paper's answers with my own second check.
3. Look at newer public records from 2026 and see what is easier or harder to confirm.

## How I did it

1. I read the original paper.
2. I rebuilt its 45-row requirement checklist.
3. I compared the paper's text with its appendix.
4. I did my own second check of the requirements.
5. I updated the results using newer public records.
6. I documented where the evidence was clear and where it was not.

## Main results

### First check: the paper's own appendix

The appendix-based baseline supports:

- `12` implemented
- `26` unknown
- `7` not implemented

So the first important finding is simple: the paper's text says `11` implemented, but the appendix-based count supports `12`.

![Chart showing the paper's original counts](outputs/figures/implementation_status_original.png)

### Second check: my own review of the same 45 requirements

My second check produced:

- `11` implemented
- `3` not implemented
- `30` unknown or unable to verify
- `1` excluded because the deadline had not passed

You can think of this like two people grading the same checklist and then comparing answers. My second check matched the paper on `38 of 45` rows, which is `84.4%` agreement, with `kappa = 0.71` (`kappa` is just a common score for how much two sets of answers agree).

The biggest difference is that I was more careful about calling something `not implemented` when the public record was thin. In several cases, I thought the more honest answer was: *I cannot confirm this from public records*.

![Chart comparing my second check with the paper's appendix](outputs/figures/second_pass_recoding_vs_paper_appendix.png)

### Third check: newer public records from July 24, 2026

When I checked newer public records, I found:

- `12` implemented
- `8` partly implemented
- `24` I could not confirm from public records
- `1` replaced by a newer rule
- `0` not implemented

This should not be read as proof that agencies failed. It should be read as a check of what an outside person can confirm from public records.

![Chart showing what newer public records support in 2026](outputs/figures/implementation_status_2026.png)

![Chart comparing the original counts with the 2026 update](outputs/figures/original_vs_2026_comparison.png)

![Chart showing how rows changed between the original baseline and the 2026 update](outputs/figures/status_change_matrix.png)

## Simple interpretation

Here is the short version:

- The paper's main idea holds up: many AI governance requirements are hard to verify from public records.
- But the exact counts depend on how strict you are about evidence.
- My second check suggests some rows marked `not implemented` are better described as `unclear from public records`.
- Even by July 2026, many requirements were still hard to confirm from public information.

## Limits of this project

This project is based on public documents, not internal government records.

That means it is good for studying transparency, but it may miss work that happened behind the scenes.

So if a row says `unable to verify`, that does **not** mean the work definitely was not done. It only means I could not confirm it from the public record I reviewed.

## Where to look next

If you want the main data files, start here:

- `data/raw/original_requirements.csv`
- `data/processed/original_second_pass_recoding.csv`
- `data/processed/requirements_coded_2026.csv`
- `data/processed/row_audit_2026.csv`
- `data/processed/summary_stats.md`

If you want the longer write-up, read:

- `report/policy_replication_report.md`

If you want field-by-field descriptions of the datasets, read:

- `data/data_dictionary.md`

## Method transparency

I used AI tools to help organize the repo, draft code, and structure the documentation. I reviewed the coding decisions, source evidence, and final interpretation myself. AI helped with the workflow, but the project conclusions were checked by me.

## How to reproduce the files

1. Install the Python packages in `requirements.txt`.
2. Rebuild the paper's checklist and original counts:

```bash
python src/build_original_replication_artifacts.py
```

3. Rebuild my second check:

```bash
python src/build_second_pass_recoding_artifacts.py
```

4. Rebuild the July 24, 2026 update:

```bash
python src/build_2026_update_artifacts.py
```

5. Rebuild the audit of higher-risk rows:

```bash
python src/build_row_audit_2026.py
```

6. Rebuild the summary numbers used in this README and the report:

```bash
python src/build_summary_stats.py
```
