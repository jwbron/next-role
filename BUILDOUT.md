# next-role inventory and buildout

## Reused concepts

The source workspace already had a discovery workflow, exact-role application packets, a story bank, interview and debrief templates, an offer-comparison template, central resume and letter builders, answer-mirror checks, and source/PDF parity tests.

Those patterns are retained. Actual profile content, application history, compensation research, interview schedules, recruiter details, PDFs, conversation exports, local reference repos, git history, and code-review-only skills are not included.

## Generalized

- Candidate identity comes from the confirmed base resume, including PDF metadata and letter headers.
- No particular employers, academic credential, dates, accomplishments, languages, locations, or salary expectations are required.
- Page limits and paper size are configurable. Optional candidate-supplied Unicode fonts replace a single person's fixed formatting contract.
- Validation checks structure and consistency, not a fixed set of personal claims or prose preferences.
- Personal data lives in an ignored workspace. Test fixtures use fictional people and organizations, and CI never needs a populated workspace.
- Rendering and validation use Python dependencies rather than system poppler executables.
- `AGENTS.md` is the public, canonical entrypoint. It is included in git's ordinary file set and in exported archives, not treated as ignored local configuration.
- Skill instructions don't depend on a particular assistant or local tool configuration. Hosts that don't load `AGENTS.md` automatically can be instructed to read it.

## Added

- Resumable onboarding from an old resume or a blank start, including early-career and career-change evidence.
- Wishlist, constraint, claim-boundary, voice, and story templates.
- Portable skills for discovery, tailoring, outreach, interview prep, mock interviews, debriefs, negotiation, and material review.
- Technical and adjacent-role practice guides, stage-specific prep, and mock feedback.
- Early compensation preparation in addition to written-offer comparison.
- Agent-owned request routing, setup, template use, manifest maintenance, and checks, without requiring the candidate to manage repository internals.
- Explicitly interactive preparation, not an automated application pipeline. Applications and recruiter messages remain manual, including when automated submission is requested.
- Required manual review of the exact text and attachments before use. Prior approval, templates, examples, agent review, and mechanical checks don't replace candidate review. Substantive edits require renewed review.
- A private session checkpoint for goals, active files, pending decisions, review state, and interrupted-work recovery. Older workspaces can add it without rerunning initialization.
- Safe initialization, a starter publication-file check, generic rendering, and synthetic regression coverage.
- Fresh-agent conversation scenarios for onboarding, resuming with a changed goal, policy restrictions, unsaved practice, actual tool failures, automated-application requests, and reuse of prior draft approval.

## Validation performed

- 45 automated tests pass locally on Python 3.14, using fictional temporary workspaces.
- Coverage includes initialization, two candidate identities, PDF metadata and text, configurable page limits and A4 paper, Unicode font handling, overwrite protection, disclosure enforcement, stale attachments, answer limits, path boundaries, publication checks, and ZIP export exclusions.
- Starter file inventory, canonical entrypoint inclusion, skill frontmatter, JSON, and local markdown file links pass their checks. Initialization saves the session template, preserves existing workspaces, and validation checks session links.
- A fictional resume and cover letter were rendered and visually inspected. This doesn't validate every future layout or script.
- Source-only validation runs without PDF dependencies, catches invalid resume boundaries and missing disclosure sources, and explicitly does not clear stale attachments. Full validation still checks generated PDFs.
- The CI configuration includes Python 3.10 and 3.14. Hosted CI and other operating systems have not been run for this initial build.

## Fresh-agent execution results

Two fresh-context agent sessions executed fictional candidate requests in disposable copies: onboarding from no resume with storage consent supplied, and resuming a saved workspace with a new interview priority and ownership correction. The agents saved drafts and checkpoints, left material awaiting review, preserved unknowns, and asked for missing evidence rather than inventing it. The interview session didn't restart onboarding or infer a completed interview.

The runs also exposed two instruction gaps. The onboarding agent omitted the canonical resume start heading because PDFs weren't requested. The interview agent saved a brief directly under the company rather than a role directory. Instructions now require the source format even without PDFs, source-only validation after usable resume drafts, and a `role-unconfirmed` directory when the exact role isn't known. Regression tests check the source-format failure and new validation mode.

The revised instructions have not yet had another fresh-agent run. Pre-consent startup, restrictive-policy handling, unsaved practice, actual write failure, automated-application refusal, and renewed review after tailoring remain behavioral scenarios to execute. The automated document checks verify that these boundaries are present, not that every agent will follow them.

## Release and product limits

- The reusable starter uses the [MIT License](LICENSE). Review rights and confidentiality separately for material imported into a private workspace.
- No public hosting, repository creation, push, or release is performed by these files.
- Interview practice and market sources need role-specific research at use time. No live listings or salary tables ship as current recommendations.
- The PDF renderer isn't a general document editor. Complex scripts, right-to-left layout, accessibility tagging, and every operating system still need validation.
- Candidate file import is conversational and manual. There is no OCR, LinkedIn login, automatic portfolio scraper, or mailbox integration.
- Backups, encryption, and assistant-provider data policies remain the user's responsibility. Ignore rules and the starter check do not guarantee privacy.
- Resume truth, form compliance, employer restrictions, live availability, negotiation arithmetic, and visual layout require human review.
- Additional formats such as academic CVs, government applications, and region-specific legal fields need their own templates and validation rather than assumptions from software hiring.
