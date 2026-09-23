"""Test publication boundaries and skill/template integrity using synthetic files."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from zipfile import ZipFile

from check_starter import check
from export_starter import export

ROOT = Path(__file__).resolve().parents[1]


class StarterTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR"))
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.root = self.directory / "starter"
        self.root.mkdir()
        (self.root / "README.md").write_text("# Fictional starter\n")
        (self.root / "AGENTS.md").write_text("# Public agent instructions\n")
        self.allowed = ["AGENTS.md", "README.md", "starter-files.json"]
        self.save()

    def save(self):
        (self.root / "starter-files.json").write_text(json.dumps(self.allowed))

    def test_real_starter_contract(self):
        self.assertEqual(check(ROOT), [])
        expected = {"onboard", "discover-jobs", "tailor-application", "draft-outreach", "prep-interview",
                    "mock-interview", "debrief", "negotiate", "review-materials"}
        self.assertEqual({p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}, expected)
        for name in expected:
            text = (ROOT / "skills" / name / "SKILL.md").read_text()
            self.assertIn("../../AGENTS.md", text)
            self.assertIn("session.md", text)
        self.assertFalse((ROOT / "agent-handoff.md").exists())
        self.assertNotIn("/AGENTS.md", (ROOT / ".gitignore").read_text().splitlines())
        self.assertIn("AGENTS.md", json.loads((ROOT / "starter-files.json").read_text()))

    def test_manual_submission_boundary_is_explicit(self):
        readme = (ROOT / "README.md").read_text()
        instructions = (ROOT / "AGENTS.md").read_text()
        workflows = (ROOT / "WORKFLOWS.md").read_text()
        tailoring = (ROOT / "skills/tailor-application/SKILL.md").read_text()
        self.assertIn("not an automated application pipeline", readme)
        self.assertIn("manually submit each application", readme)
        self.assertIn("Never submit applications on their behalf", instructions)
        self.assertIn("including when asked to apply automatically or in bulk", instructions)
        self.assertIn("No submission workflow exists", workflows)
        self.assertIn("Never submit applications on the candidate's behalf", tailoring)
        self.assertIn("manual-submission checklist", tailoring)

    def test_manual_review_is_required_for_the_current_version(self):
        readme = (ROOT / "README.md").read_text()
        instructions = (ROOT / "AGENTS.md").read_text()
        checkpoint = (ROOT / "templates/session.md").read_text()
        onboarding = (ROOT / "skills/onboard/SKILL.md").read_text()
        self.assertIn("Nothing in this repo should be blindly used, copied, or submitted", readme)
        self.assertIn("Keep material awaiting candidate review", instructions)
        self.assertIn("Substantive edits since that review", checkpoint)
        self.assertIn("--source-only", onboarding)
        self.assertIn("## Contact and summary", onboarding)

    def test_private_copy_uses_an_independent_destination_and_keeps_data_ignored(self):
        guide = (ROOT / "guides/private-copy.md").read_text()
        readme = (ROOT / "README.md").read_text()
        instructions = (ROOT / "AGENTS.md").read_text()
        self.assertIn("guides/private-copy.md", readme)
        self.assertIn("guides/private-copy.md", instructions)
        self.assertIn("forks of public repositories are public", guide)
        self.assertIn("git remote remove origin", guide)
        self.assertIn("--private --source=. --remote=origin", guide)
        self.assertIn("isPrivate: true", guide)
        self.assertIn("isFork: false", guide)
        self.assertIn("No push has happened yet", guide)
        self.assertIn("`private/` stays ignored", guide)
        self.assertIn("/private/", (ROOT / ".gitignore").read_text().splitlines())

    def test_unexpected_files_are_rejected(self):
        (self.root / "resume.md").write_text("PRIVATE_SENTINEL")
        self.assertIn("Unexpected publication file: resume.md", check(self.root))
        with self.assertRaisesRegex(ValueError, "checks failed"):
            export(self.root, self.directory / "export.zip")

    def test_private_files_are_never_exported(self):
        for directory in ("private", ".venv", ".claude"):
            (self.root / directory).mkdir()
            (self.root / directory / "secret.txt").write_text("PRIVATE_SENTINEL")
        (self.root / "CLAUDE.md").write_text("LOCAL_CONFIGURATION")
        output = export(self.root, self.directory / "export.zip")
        with ZipFile(output) as archive:
            self.assertEqual(set(archive.namelist()), {"next-role/" + path for path in self.allowed})
            self.assertNotIn(b"PRIVATE_SENTINEL", b"".join(archive.read(p) for p in archive.namelist()))
            self.assertEqual(archive.read("next-role/AGENTS.md"), (self.root / "AGENTS.md").read_bytes())
            self.assertNotIn("next-role/CLAUDE.md", archive.namelist())
        with self.assertRaises(FileExistsError):
            export(self.root, output)
        with self.assertRaises(ValueError):
            export(self.root, self.root / "internal.zip")

    def test_private_paths_cannot_be_added_to_publication_list(self):
        for path in ("private/resume.md", "../outside.md", ".env", "resume.pdf", "CLAUDE.md", ".git/config"):
            with self.subTest(path=path):
                self.allowed = ["AGENTS.md", "README.md", "starter-files.json", path]
                self.save()
                self.assertIn("Unsafe publication path", check(self.root))

    def test_canonical_entrypoint_is_required_and_nonempty(self):
        self.allowed.remove("AGENTS.md")
        self.save()
        self.assertIn("Publication set must include the canonical AGENTS.md", check(self.root))
        self.allowed.append("AGENTS.md")
        self.save()
        (self.root / "AGENTS.md").write_text("")
        self.assertIn("Canonical AGENTS.md is empty", check(self.root))
        (self.root / "AGENTS.md").unlink()
        self.assertIn("Missing publication file: AGENTS.md", check(self.root))

    def test_symlink_and_broken_links_fail(self):
        (self.root / "README.md").write_text("[Missing](missing.md)")
        self.assertTrue(any("Broken local link" in error for error in check(self.root)))
        (self.root / "README.md").unlink()
        (self.root / "README.md").symlink_to(ROOT / "README.md")
        self.assertTrue(any("Symlink file" in error for error in check(self.root)))
        (self.root / "alias").symlink_to(ROOT, target_is_directory=True)
        self.assertTrue(any("Symlink directory" in error for error in check(self.root)))

    def test_invalid_json_and_skill_frontmatter_fail(self):
        path = self.root / "skills/example"
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text("Not a skill header")
        self.allowed += ["skills/example/SKILL.md", "data.json"]
        (self.root / "data.json").write_text("{")
        self.save()
        errors = check(self.root)
        self.assertTrue(any("frontmatter" in error for error in errors))
        self.assertTrue(any("Invalid JSON" in error for error in errors))

    @unittest.skipUnless(shutil.which("git"), "git not installed")
    def test_force_tracked_private_file_is_rejected(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)
        private = self.root / "private"
        private.mkdir()
        (private / "secret.md").write_text("SYNTHETIC_PRIVATE_DATA")
        subprocess.run(["git", "add", "--", "private/secret.md"], cwd=self.root, check=True, capture_output=True)
        self.assertIn("Tracked file outside publication set: private/secret.md", check(self.root))


if __name__ == "__main__":
    unittest.main()
