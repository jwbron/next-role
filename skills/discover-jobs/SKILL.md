---
name: discover-jobs
description: Find and compare software or adjacent roles against a confirmed candidate wishlist, with exact-role sources, freshness limits, and no automatic applications.
---

# Discover jobs

## Inputs

Read [AGENTS.md](../../AGENTS.md), the workspace's search profile, career evidence, base resume, and tracker. If the target direction or a material constraint is missing, ask only what changes this search. Don't require complete onboarding.

## Procedure

1. Agree on scope: role families, geography, desired work, approximate number of leads, and time available. Carry forward exclusions and existing processes. Don't reopen a skipped company without a reason from the candidate.
2. Use distinct queries for actual work, not only titles. Aggregators can find leads, official employer pages or a recruiting contact establish the exact role. If web access is unavailable, use candidate-supplied sources and label availability unverified.
3. Capture official URL, requisition, title, work, level, location and hours eligibility, compensation units, source, check date, and retrieval limits. Use [job-source.json](../../templates/job-source.json) for a selected role or [search.md](../../templates/search.md) for the run. Don't pretend a source record is a raw API response.
4. Distinguish verified open, accessible but unlisted, confirmed unavailable, and fetch failed. Don't interpret access denial as closure. A remote label doesn't establish eligibility everywhere.
5. Deduplicate exact requisitions and company routes against the tracker. Alternatives at an already-applied company may be recruiter-discussion context rather than another application.
6. Present a short ranked set with relevant evidence, gaps, candidate-stated interest versus inferred fit, and the next question. Compare cash, equity, and liquidity separately. Unknown compensation isn't automatically a rejection unless the candidate chooses that filter.
7. Save the actual run under `research/` with a date, including new or changed leads, exclusions, queries, failed retrievals, and remaining checks. Don't write a research log for work that wasn't performed.

## Completion

Return the shortlist path, why the order fits the candidate's preferences, and what needs rechecking. Ask which role, if any, they want to pursue. Don't connect search results to automatic application preparation or submission, and don't schedule an unattended campaign. The candidate chooses roles and reviews the resulting drafts. Application submission is always manual.

## Session checkpoint

Before stopping or changing workflows, save the canonical files and update `session.md` under the selected private workspace using the checkpoint contract in `AGENTS.md`. Record the pending candidate decision and checks actually performed. Honor declined storage, and don't mark a task complete merely because a draft exists.
