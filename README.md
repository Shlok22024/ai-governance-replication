# Can We See AI Governance Progress?

*A simple reproduction and update of a 2023 study on U.S. federal AI governance*

Governments write a lot of AI rules. But a harder question is: can the public actually check whether those rules were followed?

In this project, I studied a 2023 research paper about U.S. federal AI governance. The paper looked at 45 AI-related government requirements and checked whether each one had been completed, not completed, or could not be verified.

I rebuilt that checklist, checked the paper's counts, did my own second check of the same requirements, and then looked at newer public records from 2026.

The goal was not to prove that agencies failed. The goal was simpler: understand how policy research turns legal text into data, and see how much AI governance progress can be confirmed from public records.

## What this project is

This project turns a long list of government AI requirements into a spreadsheet.

You can think of it like taking a complicated checklist and turning it into rows of data so the answers can be counted and compared. Each row asks a simple question: does the public record clearly show that this requirement was completed, not completed, or still unclear?

## What I found

1. The paper's text says `11` requirements were implemented, but its own appendix supports `12`.
2. My second check agreed with the paper on `38 out of 45` requirements.
3. Some requirements the paper called `not implemented` looked more like `unclear from public records` under a stricter evidence rule.
4. In the 2026 update, many requirements were still hard to confirm from public information.
5. `Unable to verify` does not mean `not done`. It means I could not find enough public evidence to confirm it.

The original paper marked `7` requirements as not implemented. In my second check, only `3` stayed in that category; the others looked more like cases where the public record was unclear.

## Why it matters

AI governance is not just about writing rules. It is also about whether outside people can check if those rules were carried out.

A simple analogy is checking receipts after someone says a task was done. If there is no receipt, that does not automatically prove the task never happened. But it does mean an outside reviewer cannot confirm it.

That is the main lesson of this project: public transparency and actual government action are not always the same thing.

## How I did it

1. I read the original paper.
2. I rebuilt its 45-row requirement checklist.
3. I compared the paper's text with its appendix.
4. I did my own second check of the requirements.
5. I updated the results using newer public records.
6. I documented where the evidence was clear and where it was not.

I used AI tools to help organize the repo, draft code, and structure the documentation. I reviewed the coding decisions, source evidence, and final interpretation myself. AI helped with the workflow, but the project conclusions were checked by me.

## Results and charts

### 1. Checking the paper's own appendix

The appendix-based baseline supports:

- `12` implemented
- `26` unknown
- `7` not implemented

So the first important finding is simple: the paper's text says `11` implemented, but the appendix-based count supports `12`.

![Chart showing the paper's original counts](outputs/figures/implementation_status_original.png)

### 2. My own second check of the same 45 requirements

My second check produced:

- `11` implemented
- `3` not implemented
- `30` unclear or unable to verify
- `1` excluded because the deadline had not passed

You can think of this like two people grading the same checklist and comparing answers. My second check matched the paper on `38 of 45` rows, which is `84.4%` agreement, with `kappa = 0.71`.

![Chart comparing my second check with the paper's appendix](outputs/figures/second_pass_recoding_vs_paper_appendix.png)

### 3. Checking newer public records from July 24, 2026

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

## Limitations

This project uses public documents, not internal government records.

That makes it useful for studying transparency, but it may miss work that happened behind the scenes.

So if a row says `unable to verify`, that does not mean the work definitely was not done. It only means I could not confirm it from the public record I reviewed.

## How to reproduce

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

## Files

Start with these files if you want to explore the project:

- `data/raw/original_requirements.csv`
- `data/processed/original_second_pass_recoding.csv`
- `data/processed/requirements_coded_2026.csv`
- `data/processed/row_audit_2026.csv`
- `data/processed/summary_stats.md`
- `report/policy_replication_report.md`
- `data/data_dictionary.md`
