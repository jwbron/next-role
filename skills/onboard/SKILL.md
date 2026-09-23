---
name: onboard
description: Start or refresh a private job search, build an initial resume from confirmed evidence, and gather the candidate wishlist, voice, and stories.
---

# Onboard a candidate

## Start

Read [AGENTS.md](../../AGENTS.md), [privacy](../../guides/privacy.md), and [workflow handoffs](../../WORKFLOWS.md). Resolve the private workspace before writing. If it doesn't exist, explain what will be saved and run `python init_workspace.py` from the starter root after the candidate agrees and the host permits it. Don't ask the candidate to run setup or copy templates when you can do that work. Never overwrite an existing workspace or copy anyone else's profile into it.

Explain that local files may still be processed by the candidate's assistant provider. Ask for redacted summaries rather than confidential exports. The candidate can skip questions and keep sensitive details out of the files. Ask two to four related questions at a time, not the entire inventory at once.

## Resume an existing onboarding

Read `session.md`, `profile/onboarding.md`, the relevant profile files, and the tracker when present. Summarize what is confirmed and ask what changed. Don't repeat answered questions or replace candidate edits with template defaults. A refresh may update one preference or a single experience, it doesn't require restarting.

## First conversation

Establish the immediate goal and urgency, target direction, and whether an existing resume is available. Ask what they want more and less of in their next role. Select the relevant path from their answers rather than making them choose a workflow:

- Existing resume: import only supplied or authorized content, identify old or uncertain facts, and ask about recent work missing from it.
- Blank start: build a timeline through conversation, using employment, projects, education, volunteering, research, or independent work that actually exists.
- Career change: identify the new direction and transferable evidence without retitling old jobs or claiming experience from interest alone.
- Already interviewing: create the minimum confirmed profile needed for the next event, defer the rest explicitly.

A current resume is an input, not proof every claim is still correct. If a file cannot be read, ask for text or a redacted export. Don't claim OCR or source verification occurred when it didn't.

## Gather career evidence

Use [career.md](../../templates/profile/career.md) as the structure for `profile/career.md`. Ask about roles, organizations, date precision, responsibilities, decisions, collaborators, and observed outcomes. Confirm the difference between individual and team work and between proposed, prototyped, shipped, and maintained systems.

For a promising accomplishment, ask what problem existed, what the candidate did, why that approach, and what changed. Ask for a metric only when one may actually exist, including baseline, period, units, and limitations. A qualitative result is acceptable. No degree, metric, people-management title, or public repository is required.

Record sources and confirmation dates. Mark unresolved conflicts and claims not to make. Don't put a job description's requirements into the candidate's history. Don't import employer-private implementation details just to make a bullet more impressive.

## Capture the wishlist

Use [search.md](../../templates/profile/search.md). Cover desired work and level first, then the constraints that could exclude a role: location eligibility, remote or office expectations, hours, travel, on-call, employment type, and timing. Ask about team support, company stage, products, growth, stability, and compensation tradeoffs as relevant.

Separate must-have, preference, avoid, and unknown. Ask for concrete tradeoffs instead of assigning weights. Record the scope of company-specific exceptions. If compensation is discussed, confirm currency and period. A flexible search preference is not a negotiation floor.

Work authorization, sponsorship, demographic answers, legal restrictions, and private thresholds can stay candidate-only. Don't infer them from citizenship-sounding names, location, past jobs, or previous applications.

## Build the first resume and stories

Use [resume.md](../../templates/profile/resume.md) and [the writing guide](../../guides/answers.md). Preserve the exact `## Contact and summary` and `## Editing notes, not resume content` boundaries, with name, contact, and summary as the first three content lines. This is the canonical source format even when no PDF is requested, not an optional formatting choice. Select confirmed evidence for the target direction. Write an accurate summary, relevant experience, and useful skills. Add projects, education, certifications, or other sections only when appropriate. Remove unused template markers and sections instead of making up content.

Discuss length and paper size, then save those choices in `profile/settings.json`. One or two pages can be appropriate, more specialized formats need their own decision. Keep public contact information in the base resume only as the candidate chooses. Don't ask for a full home address.

Build an initial `profile/stories.md` from two or three useful examples if available. Ask for the candidate's reflection rather than inventing lessons. Record gaps for later instead of blocking onboarding until every competency has a story.

Ask for voice preferences or a permitted writing sample and update `profile/voice.md`. Show the draft for candidate correction before calling it confirmed. The starter author's voice isn't the candidate's default.

## Save a useful checkpoint

Update `profile/onboarding.md` with reviewed sources, confirmed facts, declined or deferred inputs, open questions, and candidate review status. Record existing processes in `applications/tracker.md` only to the extent the candidate reports them, without guessing dates or sent attachments.

After saving a usable resume draft, run `python validate_materials.py --source-only` from the repository root (add `--workspace PATH` when needed). This needs no PDF packages and catches broken source boundaries, unresolved markers, and text inconsistencies. Fix structural errors before handing off the draft, or report the specific blocker. A pass doesn't approve the content or check a PDF. If Python is unavailable, inspect the source against the template and record that automated checks weren't run.

If the candidate wants PDFs, follow [material-format.md](../../guides/material-format.md), build the base, run full validation, and request visual review. No packages or rendering are necessary just to finish the conversation.

## Completion

Present the base resume and a concise summary of the wishlist, evidence, and unresolved questions for candidate review. Provide the saved paths without requiring the candidate to inspect every supporting file. Distinguish a first-pass draft from a candidate-approved resume. State which unknowns block the selected next step and which can wait. Recommend the next useful step based on their goal and ask for the decision, rather than presenting an internal skill menu. Don't run an unrequested workflow automatically.

## Session checkpoint

Before stopping or changing workflows, save the canonical files and update `session.md` under the selected private workspace using the checkpoint contract in `AGENTS.md`. Record the pending candidate decision and checks actually performed. Honor declined storage, and don't mark a task complete merely because a draft exists.
