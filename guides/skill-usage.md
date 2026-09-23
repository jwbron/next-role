# Agent entrypoint and skill loading

Start at [AGENTS.md](../AGENTS.md). It defines startup, privacy, authority, checkpoints, and completion. Use [WORKFLOWS.md](../WORKFLOWS.md) to select the skill from the candidate's intent. Don't ask the candidate to manage skill installation or choose internal workflow names.

## Host discovery

Hosts that support repository `AGENTS.md` can load the entrypoint automatically. Other hosts need an explicit instruction to read it. Don't promise automatic discovery in every assistant. Host-specific loaders may point to this file, but must not become a second maintained copy of the workflow rules.

Skills live at `skills/<name>/SKILL.md` with a name and description in frontmatter. Read the selected file directly even if the host doesn't automatically discover that directory. Resolve references relative to the skill file and retain access to the whole repository. Copying a skill file alone loses its guides and templates.

No slash command or agent-specific tool is required. If a user wants host-specific installation, follow that host's current documentation and permission rules. Don't rewrite global configuration or bypass protected paths as part of starting a search.

## Agent responsibilities

The agent selects and loads a skill, asks relevant questions, saves approved personal inputs in the private workspace, fills templates, updates the artifact manifest, and runs permitted checks. The candidate supplies facts and decisions. Don't turn routine file maintenance into homework for them.

Skills inherit the startup and checkpoint rules from `AGENTS.md`. Read `session.md` when resuming, then check the canonical files. Save pending decisions after useful progress, not just at the end of onboarding. When the candidate changes goals, follow the new request without treating a previous checkpoint as an instruction to continue unwanted work.

## Capability limits

- File access: keep candidate-specific work in the selected private workspace. If writes fail, say what wasn't saved.
- Web access: use it when available and authorized. Otherwise use supplied sources and mark availability not reverified.
- Python: use it for setup, rendering, and validation. Intake and markdown drafting can proceed without it. Don't install packages without appropriate approval.
- Structured questions: use them if the host supports them, otherwise ask in conversation. Wait for real answers rather than simulating the user.
- Delegation: optional, not required. Follow the host's permissions and isolation rules.

Only report actions actually performed. An inaccessible posting isn't closed, a successful render isn't candidate approval, and a drafted message isn't sent.
