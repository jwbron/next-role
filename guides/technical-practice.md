# Technical practice

These are original practice exercises, not reported employer prompts. Select the relevant track rather than assigning all of them.

## Systems design

For a 60-minute practice, try 8 minutes clarifying scope, 7 defining interfaces and state, 15 tracing the simplest architecture, 18 exploring failures, 7 covering operation and security, and 5 summarizing. This is a rehearsal suggestion, not an employer rubric. Follow the interviewer when they redirect.

Use `templates/system-design.md`. Separate confirmed requirements, proposed assumptions, and open questions. Identify state owners, request identity, failure outcomes, and what would change the design. A diagram should explain a path, not just list technologies.

Practice options:

- A document-processing service: accept uploads, track jobs, retry transient failures, and show results. Discuss duplicate submissions, partial completion, retention, and tenant isolation.
- A notification service: schedule and deliver messages under provider quotas. Discuss timezones, retries, idempotency, opt-outs, and uncertain delivery.
- A usage dashboard: consume events and show customer-level totals. Discuss late events, freshness, backfills, authorization, and authoritative records versus analytics.
- A model gateway for an AI-focused role: choose eligible providers, return partial output safely, enforce budgets, and account for uncertain request outcomes. A retry may cost money, and a disconnected client doesn't prove upstream work stopped.

Estimate units explicitly and label assumptions. For example, 100 requests per second with a 10-second mean service time implies about 1,000 concurrent requests in steady state, before burst headroom. Don't treat an assumption as the employer's traffic.

## Coding and debugging

For a 60-minute practical app mock, reserve 5 minutes for scope, 5 for a running skeleton, 30 for the required flow, 15 for tests and fixes, and 5 for a demonstration. An algorithmic interview needs a different plan, confirm its format first.

Practice options:

- Build a searchable task board with input validation and persistent tasks. Extend it with concurrent edits or failed saves.
- Repair a buggy importer with malformed rows and duplicate records. Demonstrate the reduced failing case and regression test before broad refactoring.
- Build a two-source comparison page. Each result has independent loading, success, and error state. Late responses must not overwrite a newer request.
- For an algorithmic format, practice a graph traversal or bounded cache. State complexity, invariants, empty-input behavior, and tests rather than forcing a web app into the format.

Keep credentials server-side. Test invalid input, normal output, timeouts, partial failures, cancellation, malformed responses, and stale updates when relevant. Mock external providers for repeatable tests. A permitted live call verifies integration, not general reliability.

## Product, portfolio, and analytical tracks

- Product: prioritize improvements to a developer onboarding flow using a small supplied evidence set. State the user problem, alternatives, proposed experiment, and a success metric with its limitations.
- Design: present a workflow redesign, including research limits, accessibility considerations, rejected options, and what changed after feedback. Don't disclose confidential artifacts.
- Data: investigate a drop in activation. Check metric definition, segmentation, data quality, plausible causes, and a plan to distinguish them. Correlation doesn't establish cause.
- Technical leadership: propose a phased migration with ownership, adoption, rollback, and cross-team coordination. Discuss a disagreement and how success will be observed.

## AI-permitted practice

Confirm permission independently for practice, assessment, and live interview. When AI is allowed, the candidate still owns requirements, decisions, code review, tests, and explanation. Give the assistant bounded work and one writer per checkout. Don't treat its completion message as proof.

When a tool fails, identify the failing layer, read the error, and reproduce the smallest case. Don't disable security controls or repeatedly rewrite the solution without a hypothesis. Rehearse with the exact environment and a simpler permitted fallback before interview day.

## Diagram and sharing workflow

Use a local preview first. Markdown and mermaid are optional, a tested editor or whiteboard is sufficient. Keep labels readable and diagrams small. Check the target renderer before relying on it.

A private git host is not a live local preview and isn't automatically an approved upload destination. Ask before publishing prompts or work. Share only a dedicated artifact, never the candidate's whole job-search workspace. Close by explaining the selected design, its main tradeoff, and unresolved questions.
