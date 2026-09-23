---
name: tailor-application
description: Tailor an exact-role resume, application answers, and optional letter from confirmed candidate evidence, honoring form limits and AI-use restrictions.
---

# Tailor an application

This skill prepares files for manual submission. Never submit applications on the candidate's behalf or automate application-form entry. If asked to apply automatically or in bulk, explain the boundary and offer to research selected roles, prepare drafts for review, or make a manual-submission checklist. Don't create browser scripts, API submission calls, or scheduled application jobs.

## Inputs

Read [AGENTS.md](../../AGENTS.md), [answers](../../guides/answers.md), and [material formats](../../guides/material-format.md). In the workspace read the base resume, career evidence, search preferences, voice, stories, tracker, and existing files for the exact role.

Ask for the official role link or supplied posting, any current draft, actual questions, and known policy. When no posting exists, record the recruiting conversation as the source and leave formal title or level unknown if not confirmed.

## Procedure

1. Check existing processes and duplicate-application rules. Refresh role availability when possible, preserving retrieval dates and failures. Don't make another route merely to improve wording on an already submitted application.
2. Create or update `applications/<company>/<role>/`. Use [application.md](../../templates/application.md), [packet.json](../../templates/packet.json), and [job-source.json](../../templates/job-source.json). Preserve older submitted artifacts, don't copy their claims uncritically.
3. Capture the exact written questions and known limits. Ask for pasted questions when form access fails. Record field/stage AI rules and any initial-draft requirement. Stop prohibited drafting and request the candidate's own text. Unknown permission is unresolved, not a guessed allowance.
4. Identify two or three central capabilities and map them to confirmed evidence IDs. Keep missing experience distinct from missing wording. Put the private rationale and gaps in `prep.md`, not the upload copy.
5. Tailor `resume.md` by selecting, ordering, and explaining supported evidence. Preserve identity, job titles, dates, attribution, and actual results. Use an accurate term from the posting where useful, not a keyword list disguised as experience.
6. Draft only useful and permitted material. A cover letter should add a genuine reason or example. Answers should address actual prompts without inventing motivation, lessons, or legal answers. Preserve candidate edits and voice. Use [answers.md](../../templates/answers.md) and keep notes outside answer sections.
7. Register current PDFs, answer mirrors, and standalone text in the workspace manifest. Preserve the canonical resume boundaries and run `python validate_materials.py --source-only --workspace PATH` on source drafts, even when attachments aren't requested yet. Use the central builders, never a per-role script. Include required disclosures through `packet.json`. Build requested outputs, run full `validate_materials.py --workspace PATH`, and inspect the rendered pages or ask the candidate to do so.
8. Present the actual answers, resume, and attachment paths for manual candidate review. Highlight meaningful changes and unresolved claims. Ask the candidate to check facts, ownership, contact details, dates, metrics, voice, confidentiality, and exact form/policy requirements. They must inspect attachments before use. Keep the packet awaiting review until this version is explicitly reviewed, and renew review after substantive edits. Neither validation nor approval of the base resume authorizes use of a tailored copy. If anything material is unresolved, keep a clearly partial packet rather than calling it ready to submit.

## Completion

Give exact current file paths, the tailoring rationale, checks actually run, visual-review status, and candidate-only fields or decisions. Prepared isn't submitted. The candidate reviews each packet, makes final edits, and submits it manually. Approval of a draft isn't permission for the agent to upload or submit it. Update the tracker only with confirmed process information and preserve the actual submitted version when known.

## Session checkpoint

Before stopping or changing workflows, save the canonical files and update `session.md` under the selected private workspace using the checkpoint contract in `AGENTS.md`. Record the pending candidate decision and checks actually performed. Honor declined storage, and don't mark a task complete merely because a draft exists.
