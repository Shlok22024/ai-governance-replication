# Can We See AI Governance Progress?

*A simple reproduction and update of a 2023 study on U.S. federal AI governance*

## What this report is about

This report is about a simple question:

**When the government says it will do something about AI, can the public actually see evidence that it happened?**

To explore that question, I studied a 2023 paper about U.S. federal AI governance. The paper looked at 45 government requirements related to AI and sorted them into categories like completed, not completed, or unclear.

I rebuilt the paper's checklist, checked the paper's own numbers, did my own second check of the same 45 rows, and then looked at newer public records from July 24, 2026.

## The paper I studied

The paper is:

Lawrence, Christie, Isaac Cui, and Daniel E. Ho. 2023. _The Bureaucratic Challenge to AI Governance: An Empirical Assessment of Implementation at U.S. Federal Agencies_.

It focused on three major U.S. government AI rules:

- Executive Order 13859
- Executive Order 13960
- The AI in Government Act of 2020

## A simple way to think about the project

Think of the paper like a long checklist.

Each checklist item says something like:

- Here is what the government said it would do.
- Here is who was supposed to do it.
- Here is whether there was public evidence that it happened.

My project turns that checklist into a spreadsheet. Each requirement becomes one row of data.

That makes it easier to compare answers, count results, and spot places where the paper's wording and the paper's appendix do not fully match.

## What I did

I did the project in three steps:

1. I checked the paper's appendix and rebuilt its 45-row checklist.
2. I did my own second check of the same 45 requirements using public evidence that would reasonably have existed by November 15, 2022.
3. I checked newer public records from July 24, 2026 to see what could be confirmed later.

You can think of step 2 like two people grading the same checklist and comparing answers.

## What I found

### 1. The paper's text and appendix do not fully match

The paper's text says `11` requirements were implemented.

But when I rebuilt the counts from the appendix-based checklist, I got:

- `12` implemented
- `26` unknown
- `7` not implemented

So the first important result is that the appendix supports `12`, even though the prose says `11`.

### 2. My second check was close to the paper, but not identical

My own second check agreed with the paper on `38 of 45` rows.

That is `84.4%` agreement, with `kappa = 0.71` (`kappa` is a common score for how much two sets of answers agree).

This means the paper and my review were often close, but not always. The disagreements are useful because they show where judgment matters.

### 3. Stricter evidence rules change some rows

Under my second check, the 45 rows became:

- `11` implemented
- `3` not implemented
- `30` unknown or unable to verify
- `1` excluded because the deadline had not passed

This is one of the main lessons of the project.

Some rows the paper treated as `not implemented` looked more like `I could not confirm this from public records` when I applied a stricter rule.

That difference matters. It is the difference between saying:

- "I found evidence that this did not happen"

and saying:

- "I could not find enough public evidence to confirm it"

Those are not the same claim.

### 4. Even in 2026, many rows were still hard to confirm

When I checked newer public records from July 24, 2026, I found:

- `12` implemented
- `8` partly implemented
- `24` I could not confirm from public records
- `1` replaced by a newer rule
- `0` not implemented

This does **not** prove agencies failed.

It only shows what could and could not be confirmed from public information by an outside reviewer.

## Why this matters

This project matters because public policy is not just about writing rules. It is also about whether the public can see enough evidence to check progress.

A good analogy is checking receipts after someone says they finished a task. If the receipts are missing, you may not be able to confirm the claim, even if some work really was done.

That is what happened in many rows here. The issue was often public visibility, not necessarily proven failure.

## Limits of this project

This project depends on public records.

That means it may miss work that happened inside agencies but was never clearly published.

So when a row says `unable to verify`, the meaning is simple:

**I could not confirm it from public records.**

It does **not** automatically mean:

**the work was not done.**

## Method transparency

I used AI tools to help organize the repo, draft code, and structure the documentation. I reviewed the coding decisions, source evidence, and final interpretation myself. AI helped with the workflow, but the project conclusions were checked by me.
