---
name: literature-review
description: Find, read, and synthesize primary research papers for a technical or scientific question, verify every citation, and record each claim with its evaluation conditions. Use for literature reviews, related work, "what does the research say", choosing a method from papers, or checking a cited claim.
license: MIT
---

# Literature review

Answer a research question from primary sources the reader can check.

## Not for

- Facts answerable from official documentation or the repository itself: read those directly.
- Auditing the repo's own claims or code: use `repo-audit`.

## Scope the question

1. Write the question as one sentence with its object, metric, and setting, such as "Does LoRA rank above 16 improve 7B instruction-tuning accuracy on held-out tasks?".
2. Name what would change the answer: model or system scale, dataset, compute budget, date range, and the baseline that counts.
3. Decide the depth before searching: a quick check (3-5 key papers), a method choice (5-15 papers plus reference implementations), or a survey (search log, inclusion rules, and a coverage statement).

## Search

- Use the strongest academic search the host offers (an arXiv or paper-search tool, Semantic Scholar, Google Scholar, ACL Anthology, OpenReview, PubMed for biomedicine), then general web search for venue pages, code, and errata.
- Run several queries with synonyms and the field's own terms. Follow citations both ways from the two or three most central papers: what they cite, and what cites them.
- Prefer the published version over a preprint when they differ, and record which one you read. Check for retractions, errata, and later replications or refutations.
- Keep a search log: query, source, date, and how many results you screened.

## Read

For each paper you rely on, open the full text, not only the abstract, and record:

- the claim, in your own words, with the table, figure, or section it comes from;
- the evaluation conditions: datasets, model or system size, baselines, metric, number of runs or seeds, and variance or confidence intervals when reported;
- what the authors say limits the result, and what you notice that they do not;
- whether code, data, or weights are released, and whether the released code matches the paper.

Separate what a paper measured from what it speculates. Never upgrade "we observe on one benchmark" to "X works".

## Verify citations

Every reference in your answer must resolve to a real paper you opened: correct authors, title, venue, year, and a stable link (DOI, arXiv ID, or ACL/OpenReview URL). Say so and do not cite a source as support when you cannot open it. Do not invent page numbers, quotes, or results.

## Synthesize

- Group papers by the answer they support, not by publication order. Explain the difference in setup before calling one result wrong when results disagree.
- Weigh evidence by design: several seeds outweigh one favourable run; a replication outweighs the original claim.
- State what the evidence does not cover, including the reader's own setting when it differs from every paper's.
- Name the reference implementation to start from and the one experiment that would confirm the finding in the target environment, whenever the review informs an implementation. Use `scientific-visualization` for figures and `benchmark-checklist` before reporting a measured reproduction.

## Hand back

1. The answer in two to four sentences, with confidence and the main caveat.
2. A claims table: claim, paper, evidence location, conditions, and strength.
3. Disagreements and open questions.
4. References with stable links, plus the search log for a survey-depth review.

## Done when

- Every cited reference was opened in full text and has a stable link; the final text names any source you could not open.
- Each row of the claims table has a location (table, figure, or section) and its conditions.

## If it fails

Add a differently worded query or a citation hop from a central paper when the search finds nothing new, then rescreen. Report the gap and lower the stated confidence rather than citing an unopened paper. Do not relax the full-text rule.

## Example

Answer: Raising LoRA rank above 16 gave no reliable gain on held-out tasks at 7B in the one controlled study found (moderate confidence); no paper covers your 13B setting.

| Claim | Paper | Evidence | Conditions | Strength |
|-------|-------|----------|------------|----------|
| Rank 16 and rank 64 score within noise | `<Author et al., year, venue>` | Table `<n>` | 7B, `<dataset>`, 3 seeds, accuracy | Controlled, one model family |

Open questions: results at 13B.

References: `<Author et al., title, venue, year>`, `<arXiv ID or DOI link>`.
