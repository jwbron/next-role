# next-role

An agent-guided job search for software engineers and adjacent roles, including product, design, data, security, and technical leadership. Open this repository in your coding agent and describe what you need. The agent interviews you, maintains your private workspace, and prepares the material. You confirm the facts, make decisions, and send applications and messages yourself.

This is an interactive preparation workflow, not an automated application pipeline. It must not be used to apply to roles automatically or in bulk. You review and manually submit each application. The agent doesn't fill and submit application forms, send recruiter messages, or run unattended application campaigns.

Nothing in this repo should be blindly used, copied, or submitted. Templates and fictional examples aren't your experience, agent drafts can contain mistakes, and research can be stale. Manually review the exact text and attachments you intend to use. Check factual claims, ownership, dates, contact details, tone, confidentiality, and employer instructions, and inspect the rendered PDFs. Passing tests or approving an earlier version doesn't replace that review. Your review also doesn't override an employer's restrictions on AI use.

Start with an existing resume or no resume at all. The workflow covers career evidence and preferences, discovery, tailored applications, a personal site and LinkedIn, interview preparation and practice, debriefs, and negotiation. Local setup, PDF generation, and validation can be automated, application decisions and submissions cannot.

## Create your private copy first

If you'll use github for your search, [create an independent private copy](guides/private-copy.md) before adding personal information. Don't use the Fork button: a fork of this public repo stays public and cannot be made private independently. The guide includes agent-assisted setup, terminal commands, and repository creation through the github website when the github CLI isn't available.

A local-only copy is also supported. In either setup, `private/` remains ignored by git, so repository pushes don't back up your personal search files. Keep a separate private backup.

## Start a conversation

1. Open your verified private copy, or a local-only copy, in your preferred coding agent.
2. Say `Help me start a job search.` The agent reads [AGENTS.md](AGENTS.md), checks for existing work, and guides you through onboarding. If your host doesn't load `AGENTS.md` automatically, say `Read AGENTS.md and help me start a job search.`
3. Answer a few questions at a time and review what the agent drafts. You can skip optional questions, change priorities, or pause and return later.

You don't need to pick skills, copy templates, edit JSON, or run setup commands yourself. The agent handles local setup with your agreement and within its tool permissions. If it can't access files or run tools, it should say what it cannot save or verify, not pretend the work happened.

If you're already applying or interviewing, start there. For example, say `Help me prepare for this hiring-manager interview` and provide the relevant context. The agent should collect what's needed for that task rather than require complete onboarding first.

## What the agent does

- Builds or refreshes your base resume, career evidence, story bank, wishlist, and writing preferences.
- Finds roles against your stated criteria, checks them against employers' live job boards, and distinguishes current evidence from unknowns.
- Tailors resumes, answers, and useful letters to the exact role and its restrictions.
- Drafts referral requests and recruiter follow-ups without sending them.
- Creates stage-specific interview prep and runs one-question-at-a-time practice.
- Records what actually happened in an interview and prepares for the next step.
- Helps plan a simple personal site, short essays from your own work, and LinkedIn text, publishing nothing without your approval.
- Explains compensation components, models private equity scenarios, compares actual offers, and drafts honest negotiation requests.
- Saves progress so a later agent session can resume without repeating the whole intake.

[AGENTS.md](AGENTS.md) is the canonical entrypoint. [WORKFLOWS.md](WORKFLOWS.md) routes requests to the ten portable skills under `skills/`. Guides and templates are supporting material for the agent, not required reading for the candidate. See [skill usage](guides/skill-usage.md) for host compatibility.

No particular slash command, agent subscription, or external integration is required. Research needs web access or sources you supply. Python 3.10 or newer supports workspace setup and optional PDF tools. Conversation and markdown drafting don't require PDF dependencies.

## Your data stays separate

| Path | Contents | Share? |
| --- | --- | --- |
| `AGENTS.md`, `skills/`, `templates/`, `guides/` | Reusable workflow instructions | Review before publishing |
| `tests/fixtures/` | Fictional test material | Yes, not real candidate evidence |
| `private/session.md` | Current task, saved files, and pending decisions | No |
| `private/profile/` | Resume, career evidence, preferences, and voice | No |
| `private/applications/` | Tracker, drafts, interview prep, and offer notes | No |
| `private/research/`, `private/evidence/`, `private/previews/` | Research, imports, and previews | No |
| `private/presence/` | Site plan, essay drafts, and publish log before approval | No, publish only approved pages from a separate site repository |

The agent asks before initializing the workspace or importing personal material. `private/` is ignored by git, and the initializer adds another ignore file inside it. Ignore rules aren't encryption and don't prevent forced adds, uploads, cloud sync, or assistant-provider retention. Keep a private backup. Don't publish a populated workspace or its history. See [privacy guidance](guides/privacy.md).

The agent shouldn't invent missing experience or legal answers or help evade application and interview AI restrictions.

## Local tools, for agents and maintainers

Run commands from the repository root. Material commands accept `--workspace PATH` for a nondefault private workspace. Output paths are relative to that workspace and cannot escape it.

- Initialize after the candidate agrees: `python init_workspace.py`
- Install optional PDF dependencies with appropriate approval: `python -m venv .venv && .venv/bin/python -m pip install -r requirements.txt`
- List registered resumes: `.venv/bin/python build_resume.py --list`
- Build the confirmed base: `.venv/bin/python build_resume.py --key base`
- Preview a change: `.venv/bin/python build_resume.py --key base --output previews/resume.pdf`
- Deliberately replace an attachment: `.venv/bin/python build_resume.py --key base --overwrite`
- Build a role letter: `.venv/bin/python build_cover_letter.py --packet applications/example-company/example-role`
- Check source drafts without PDF dependencies: `python validate_materials.py --source-only`
- Validate sources and attachments: `.venv/bin/python validate_materials.py`
- Validate the reusable starter: `python check_starter.py`
- Run fictional regression tests: `.venv/bin/python -m unittest discover -v`

On Windows, use `.venv\Scripts\python.exe` instead of `.venv/bin/python`. The example-company path is a placeholder, not an installed packet. Read [material formats](guides/material-format.md) before editing registrations or rendering.

The blank workspace intentionally fails source validation until its placeholders are replaced with a structurally valid draft, and full validation also requires built attachments. Neither result establishes candidate approval. Rendering uses configurable page limits, Letter or A4 paper, and optional Unicode fonts. It refuses unresolved template markers and preserves an existing PDF if rendering or text checks fail. Required letter disclosures are included automatically. Mechanical checks don't establish factual accuracy, policy compliance, visual quality, or application status.

## Development and release

[BUILDOUT.md](BUILDOUT.md) records the inventory, validation, and remaining limits. [Agent scenarios](tests/agent-scenarios.md) define behavioral checks for a fresh agent session. Automated Python tests verify tooling and document contracts, not whether a model follows every instruction.

The reusable source, skills, templates, and guides are licensed under the [MIT License](LICENSE). Keep candidate data in private workspaces, outside the publication file set. The license doesn't remove the need to review imported material for rights, confidentiality, and employer restrictions.

After reviewing the reusable files, package them with `python export_starter.py --output ../next-role.zip`. The exporter uses `starter-files.json` and refuses an existing destination. It includes the public `AGENTS.md` but excludes personal workspaces, local host configuration, the virtual environment, and git history. Don't zip the entire directory yourself. Add new reusable files to the publication list explicitly and run the checks.
