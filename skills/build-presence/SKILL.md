---
name: build-presence
description: Plan and draft a minimal personal site, short essays from the candidate's own work, unlisted deep-dive pages, and LinkedIn profile text, consistent with the resume and published only with explicit approval.
---

# Build a public presence

Nothing in this skill is published, pushed, deployed, or posted without the candidate's explicit approval of the exact change. Show the diff or rendered page first. Never log in to, edit, or post on a social profile for the candidate.

## Inputs

Read [AGENTS.md](../../AGENTS.md), [presence guidance](../../guides/presence.md), and the workspace's base resume, career evidence, voice, and search profile. Ask what the candidate wants: a new site, an update, an essay, an unlisted deep dive, or LinkedIn text. Ask whether a site repository and host already exist and who controls them. Don't require a site if the candidate doesn't want one.

## Procedure

1. Agree on the goal and time budget. Draft a positioning statement, capabilities, and results from confirmed evidence only. Use [presence.md](../../templates/presence.md) under the private workspace's `presence/` directory to hold the plan, claim comparison, and publish log.
2. For a site, propose a minimal static page in plain HTML and CSS with restrained design. Keep the site in its own repository, separate from the private job-search copy. Help with hosting setup, an optional custom domain, and HTTPS only with the candidate's agreement and the host's permissions.
3. Compare every site and LinkedIn claim with the current base resume. Titles, dates, ownership, and results must match. List differences for the candidate rather than silently choosing one.
4. For essays, start from a real piece of the candidate's work and their own view of it. Run the confidentiality check from the guide on every draft: no former employer's internal names, private metrics, incidents, customers, colleagues, or unreleased details without permission. Have the candidate review the voice and mark anything they wouldn't say or defend.
5. For an unlisted page, add a `noindex` robots meta tag, keep it out of navigation and any sitemap, and tell the candidate plainly that unlisted isn't private. Restricted material belongs in a private shared document instead.
6. For LinkedIn, draft the headline, About, experience entries, and Featured items as text to paste, and explain the Open to Work visibility tradeoff for their situation. The candidate makes the edits.
7. Before any publish, show the exact changes, the claim comparison, and the confidentiality check result. Push or deploy only after explicit approval of that version. Afterward, check the live page and record what changed and when.

## Completion

Return the draft paths, the claim differences still open, confidentiality items the candidate needs to decide, and what's awaiting approval. Distinguish drafted, approved, and published. Don't mark anything published until the candidate confirms or the live page is checked.

## Session checkpoint

Before stopping or changing workflows, save the canonical files and update `session.md` under the selected private workspace using the checkpoint contract in `AGENTS.md`. Record the pending candidate decision and checks actually performed. Honor declined storage, and don't mark a task complete merely because a draft exists.
