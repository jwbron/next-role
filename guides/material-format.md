# Material formats and builders

The builders support a small markdown subset, not arbitrary markdown or a universal resume format. Writing workflows can use other formats without these tools.

## Resume

Use [the resume template](../templates/profile/resume.md). Content begins after the exact heading `## Contact and summary` and ends before `## Editing notes, not resume content`. The first three nonempty lines are name, contact line, and summary. They can contain any confirmed identity, no employer or degree is required.

After that, use `## Section`, `### Entry`, single-line paragraphs, and `- Bullet`. Long lines wrap automatically. No tables, inline markdown emphasis, embedded images, or nested bullets are interpreted. Plain HTTPS URLs and email addresses become links. Private editing notes never enter the PDF. Keep claim-evidence notes in `profile/career.md`, not inside a public paragraph.

`profile/resume.md` is also the name/contact source for letters. Tailored resumes must preserve that identity. Change identity in the base and relevant variants together. There are no default employers, metrics, graduation dates, or academic credentials.

## Rendering settings

[settings.json](../templates/profile/settings.json) selects `paper_size` (`letter` or `A4`), `resume_max_pages`, and `letter_max_pages`. Page limits range from 1 to 10. Choose the actual desired length, don't shrink text just to preserve an old draft.

The built-in Helvetica fonts cover a limited Western character set. For other characters, copy licensed TrueType font files into the private workspace and set `fonts` to an object with `regular` and `bold` relative paths. The renderer checks glyph coverage and fails rather than knowingly replacing characters. Do not redistribute fonts without checking their license. Right-to-left shaping, complex scripts, and accessibility tagging have not been validated. Use a suitable external editor when this renderer doesn't meet the candidate's needs.

Every render uses a temporary file, checks extracted text and page count, then publishes the output. A failure preserves the previous attachment. An existing output needs `--overwrite`. Visually inspect intentional changes, text equality doesn't establish layout quality.

## Resume manifest

Paths in `resume-manifest.json` are relative to the workspace, not the starter or role directory. All four arrays are required. Empty arrays are valid for a workspace that isn't using those artifact types.

A resume entry uses `key`, `source`, and `pdf`. For example: `{"key":"example-role","source":"applications/example-company/example-role/resume.md","pdf":"applications/example-company/example-role/resume.pdf"}`.

An answer mirror entry uses `source`, `heading`, and `text`. The combined source must have exactly one `## Exact question` heading, a blank line, and the answer before the next second-level heading. Private notes belong under their own heading. Don't place notes inside the answer section. For example: `{"source":"applications/example-company/example-role/answers.md","heading":"Why this role?","text":"applications/example-company/example-role/why-role.txt","max_words":200}`.

Standalone upload text uses `text_artifacts`: `{"text":"applications/example-company/example-role/outreach.txt"}`. Do not register the same output in two arrays. `letters` uses `packet` and `pdf`: `{"packet":"applications/example-company/example-role","pdf":"applications/example-company/example-role/cover-letter.pdf"}`.

Verified limits can include `min_words`, `max_words`, `max_characters`, `max_paragraphs`, or `sentences`. Don't add arbitrary constraints. Sentence counting is heuristic and character counting uses Python string length, which may differ from a form's counter. Check the live form too.

## Role packet

Copy [packet.json](../templates/packet.json) into the exact-role directory and replace every template marker. `company` and `title` are required for letters. Record the official URL, requisition, dates, question source, and policy in readable notes and the source record. Preserve uncertainty with `null` or prose, not invented values.

For a required AI disclosure, add `required_disclosure` pointing to a text file relative to the packet. The builder automatically appends it and fails if it is missing or still contains a template marker. Do not use the disclosure mechanism to evade a ban on AI-generated initial answers.

## Validation scope

Run `python validate_materials.py --source-only` after saving a usable draft, even if the candidate doesn't want PDFs. This mode needs only the Python standard library. It checks registered source structure, identity, text, required disclosure sources, artifact coverage, and local links without requiring or reading the registered PDFs. Output explicitly states that PDFs were not checked. A stale attachment can still exist, so a source-only pass never clears an attachment for use.

Full validation checks registered PDF/source parity, configured page limits, base/tailored identity, known answer limits, answer mirrors, unresolved template markers, unregistered current PDF/text artifacts, and explicit local markdown file links, including the current `session.md` checkpoint. Current links stay inside the workspace. Store source URLs as remote links and refer to reusable starter paths as code text.

Historical `archive/` directories, `evidence/` imports, and `previews/` are excluded from current-material checks. Exclusion is not approval to resend or publish them. Draft markdown not registered as an artifact isn't fact-checked or certified ready. Link checks don't validate headings, browser permissions, or remote availability.

Only the documented `{{...}}` and `[TODO: ...]`, `[CANDIDATE: ...]`, `[CONFIRM: ...]`, `[COMPANY: ...]` markers are detected. Other unfinished prose still requires human review. Neither mode confirms facts, employer-policy compliance, voice, or readiness for submission. The candidate must manually review the exact text and attachments before using them, and review substantive changes again. Don't turn the validator into a factual decision engine.
