# Agent workflow routing and handoffs

Follow [AGENTS.md](AGENTS.md) first. Choose the workflow from the candidate's request and current files, not a fixed sequence they must finish. The agent gathers input, selects evidence, maintains files, and runs permitted checks. The candidate confirms facts, sets preferences, makes decisions, and sends material. This is an interactive preparation workflow, not an automated application pipeline. Every application is reviewed and submitted manually by the candidate.

## Route the request

| Candidate intent | Load | Minimum useful input | If input is missing |
| --- | --- | --- | --- |
| Start a search, build a resume, change direction, or refresh the profile | [onboard](skills/onboard/SKILL.md) | Immediate goal and candidate conversation | Ask about the goal and existing resume, then work in small batches |
| Find jobs or compare opportunities | [discover-jobs](skills/discover-jobs/SKILL.md) | Desired work, relevant constraints, existing processes | Ask what changes the search, don't require a finished resume |
| Prepare an application for manual submission or tailor a resume, letter, or answer | [tailor-application](skills/tailor-application/SKILL.md) | Exact role context and relevant confirmed experience | Collect missing facts inline and request real form questions, not a full onboarding restart |
| Contact a recruiter, ask for a referral, or follow up | [draft-outreach](skills/draft-outreach/SKILL.md) | Recipient, actual relationship, desired next step | Ask for those details before implying a relationship or message history |
| Prepare for an upcoming interview | [prep-interview](skills/prep-interview/SKILL.md) | Role, known stage/format, available prep time | Make a provisional brief, ask about unknown logistics and relevant stories |
| Practice or rehearse | [mock-interview](skills/mock-interview/SKILL.md) | Agreed format, time budget, feedback timing | Propose a suitable practice track and ask one question at a time |
| Describe an interview that happened | [debrief](skills/debrief/SKILL.md) | Candidate account of a completed event | Confirm which event happened before updating status |
| Discuss pay, negotiate, or choose an offer | [negotiate](skills/negotiate/SKILL.md) | Early discussion versus actual offer, candidate priorities | Prepare questions when terms are unknown, don't fabricate a package |
| Check existing materials | [review-materials](skills/review-materials/SKILL.md) | Scope and current files | Ask which packet to inspect, don't rewrite by default |
| Continue or resume without a new task | Read `session.md` and canonical files first | Last saved goal and pending decision | Summarize the checkpoint and ask what changed, use onboarding if no prior work exists |
| Apply automatically, submit a batch, or schedule an application campaign | No submission workflow exists | No additional credentials or permissions are needed | Decline automated submission and offer role research, reviewed drafts, or a manual-submission checklist |

If a request spans workflows, propose an order based on the candidate's goal and deadline. Follow agreed preparation work without repeatedly asking permission for each internal file operation. Still pause for missing facts and candidate decisions. Don't turn an agreed plan or approved drafts into an unattended pipeline. There is no authorization that enables agent-run application submission in this workflow.

If the request is ambiguous between materially different tasks, ask one focused question. Don't make the candidate learn skill names or select templates. The table is for the agent, not an intake questionnaire.

## Run the selected workflow

1. Read the selected skill, its linked guidance, and the relevant workspace files. Load only the candidate material needed for the task, not every application or raw export.
2. State the immediate result you're working toward. Ask two to four related questions at a time, or one question per mock-interview turn. Wait for answers before continuing the interview.
3. Update confirmed facts in their canonical files. Draft with explicit unknowns in private notes, not invented details in submission copy. For usable resume drafts, run source-only validation even when no PDF is requested. Save a checkpoint after useful progress rather than waiting for the entire search to be complete.
4. Present the actual text and attachment paths for manual review, explain consequential changes, and flag unresolved claims or restrictions. The candidate must review the exact version they intend to use, not blindly copy a template or rely on an earlier approval. Keep facts confirmed, draft prepared, candidate approved, mechanically checked, and externally submitted as separate states. Substantive edits require renewed review.
5. Run available checks, report their actual scope, save the pending decision in `session.md`, and recommend the next useful step. Leave sending and submission to the candidate, and don't advance to an unrelated workflow.

A passing validator only checks specified mechanical properties. It isn't evidence that the material is true, current, compliant with employer rules, or representative of the candidate. Don't label material ready for use while candidate review or material questions remain pending. Manual review cannot authorize prohibited AI assistance.

## Handoffs between workflows

| From | Preserve | Before the next step |
| --- | --- | --- |
| Onboarding to discovery | Search wishlist, claim boundaries, profile review state | Confirm the search scope and relevant constraints |
| Discovery to application | Exact role, dated sources, fit rationale, unresolved eligibility | Candidate selects the opportunity, check existing routes and current policy |
| Application to interview prep | Relevant evidence, private gaps, actual role/form context | Confirm stage and format, prepared materials don't imply an interview |
| Prep to mock | Selected practice track, learning goal, available time | Agree on feedback timing and whether to save notes |
| Interview to debrief | Prior prep and confirmed scheduling | Candidate confirms the event occurred and supplies their account |
| Debrief to next-round prep | Direct feedback, new facts, candidate reactions | Confirm the next stage rather than inferring it |
| Any stage to negotiation | Actual compensation statements and candidate criteria | Distinguish preparation from a real offer and genuine alternatives |

A blank salary target, no degree, career gap, missing metric, or skipped sensitive field doesn't block every workflow. Record unknowns that matter to the next decision and defer the rest.

## Recover and resume

`session.md` is a small navigation record, not a second fact registry. It points to the current profile, packet, and tracker. It records the task state as not started, gathering input, drafting, awaiting candidate review, blocked, paused, or complete, independently of employer-process status. Completion means the requested local result is finished, not that an application was submitted.

When the checkpoint is absent in an older workspace, create it from [the blank session template](templates/session.md) after reading the existing files. Don't rerun the initializer or overwrite the workspace. If state conflicts with the candidate's new correction, update canonical facts, identify affected drafts, and preserve actual submitted history.

| Limitation | Agent response |
| --- | --- |
| No web access or an inaccessible form | Use supplied sources, record retrieval limits, request actual questions, don't claim live verification |
| No Python or PDF packages | Continue intake and markdown drafting, offer permitted setup when attachments are needed |
| No file-writing access | Continue in conversation, explicitly say nothing was saved, don't claim a durable checkpoint |
| Rendering or validation failure | Preserve the previous output, report the failure, diagnose it before retrying |
| Unknown or restrictive AI policy | Clarify the actual stage rules, request candidate-authored text when required, don't evade restrictions |
| Interrupted session | Read the checkpoint and affected files, determine what actually saved, resume without repeating confirmed questions |
| Candidate declines storage | Keep the declined content out of every file, including the checkpoint |

Don't infer completed interviews from old dates, fresh availability from old research, approval from an existing file, or submission from a generated PDF.
