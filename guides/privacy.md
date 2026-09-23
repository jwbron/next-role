# Keep personal data private

The reusable starter and a populated search workspace have different audiences. Share the former, never assume permission to share the latter.

## Before onboarding

Explain that an assistant may send text to its provider even when files are local and ignored by git. The candidate decides what to provide. Use summaries and redacted examples instead of confidential source exports. Don't request credentials or identity documents.

Use `private/` or an explicitly selected external private directory. The initializer sets the workspace directory to owner-only access on systems that support it. This isn't a cross-platform encryption or access-control guarantee. Don't place a private workspace in a cloud-synced public folder.

## Before sharing

Inspect the exact selected files and full staged diff, not just their filenames. Check document text, PDF metadata and extracted text, contact details, source snapshots, comments, calendar data, negotiation notes, and old attachments. Renaming a file doesn't sanitize it.

Never publish the populated workspace's git history. Deleting a secret in the latest commit doesn't remove earlier copies. If personal data was exposed, stop publication, remove access where possible, and assess remediation. Rotate exposed credentials through their owner, don't print them in a report.

`python check_starter.py` rejects unexpected files and populated private directories outside the ignored workspace. It isn't a general personal-information detector. Human inspection is still required, especially for modifications to allowed source files. Public CI runs on fictional fixtures only and must never upload personal documents.

## Interviews and assessments

AI permission doesn't authorize uploading an employer's prompt, sharing it in a public repository, or using external tools with confidential data. Confirm tools, destination, and disclosure separately. Use a dedicated artifact directory for screen sharing and hide unrelated tabs and notifications.

## Retention and backup

Choose a private backup and retention policy. Ignored files won't be saved by ordinary git commits. Don't delete original resumes, submitted versions, or feedback without asking. References can be stored as a redacted summary with a source/date instead of the original confidential document.
