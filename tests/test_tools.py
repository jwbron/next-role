"""Fictional, temporary workspaces only. Never read a real candidate workspace."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from pypdf import PdfReader

from build_cover_letter import build
from init_workspace import initialize
from material_content import (END, START, check_answer, check_text, load_manifest,
                              local, resume_content, settings)
from resume_renderer import render_resume, text_markup
from validate_materials import audit, check_pdf

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = (ROOT / "tests/fixtures/resume.md").read_text(encoding="utf-8")


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR"))
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.root = initialize(self.directory / "workspace")
        self.source = self.root / "profile/resume.md"
        self.source.write_text(FIXTURE, encoding="utf-8")
        self.pdf = self.root / "profile/resume.pdf"
        self.config = settings(self.root)

    def render(self):
        return render_resume(self.root, self.source, self.pdf, self.config)

    def failures(self):
        return [result for result in audit(self.root) if result["status"] == "fail"]

    def save_manifest(self, manifest):
        (self.root / "resume-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    def packet(self):
        path = self.root / "applications/example-company/example-role"
        path.mkdir(parents=True)
        (path / "packet.json").write_text(json.dumps({"company": "Example Company", "title": "Engineer"}), encoding="utf-8")
        (path / "cover-letter.txt").write_text("I build reliable tools.\n\nI help users recover from errors.\n", encoding="utf-8")
        return path, path.relative_to(self.root).as_posix()

    def test_init_copies_blank_templates_and_refuses_overwrite(self):
        blank = initialize(self.directory / "blank")
        self.assertIn("{{NAME}}", (blank / "profile/resume.md").read_text())
        self.assertEqual((blank / ".gitignore").read_text(), "*\n")
        self.assertEqual((blank / "session.md").read_text(), (ROOT / "templates/session.md").read_text())
        self.assertIn("Task state: not started", (blank / "session.md").read_text())
        self.assertEqual(load_manifest(blank)["resumes"][0]["key"], "base")
        self.assertIn("placeholder", audit(blank)[0]["error"])
        (self.root / "session.md").write_text("A real saved checkpoint, don't overwrite.")
        with self.assertRaises(FileExistsError):
            initialize(self.root)
        self.assertEqual(self.source.read_text(), FIXTURE)
        self.assertEqual((self.root / "session.md").read_text(), "A real saved checkpoint, don't overwrite.")

    def test_init_rejects_existing_symlink(self):
        target = self.directory / "link"
        target.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(FileExistsError):
            initialize(target)

    def test_complete_workspace_passes(self):
        self.render()
        self.assertEqual(self.failures(), [])

    def test_source_only_passes_without_pdfs_and_marks_scope(self):
        results = audit(self.root, source_only=True)
        self.assertTrue(all(result["status"] == "pass" for result in results))
        self.assertIs(results[0]["pdf_checked"], False)
        self.assertFalse(self.pdf.exists())
        self.assertEqual(self.failures()[0]["asset"], "base")

    def test_source_only_catches_noncanonical_draft_without_pdf_packages(self):
        self.source.write_text(FIXTURE.replace(START, ""))
        result = subprocess.run([sys.executable, "-S", str(ROOT / "validate_materials.py"),
                                 "--workspace", str(self.root), "--source-only", "--json"],
                                cwd=self.directory, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["scope"], "source-only")
        self.assertFalse(report["ok"])
        self.assertIn("content start", report["results"][0]["error"])
        self.source.write_text(FIXTURE)
        result = subprocess.run([sys.executable, "-S", str(ROOT / "validate_materials.py"),
                                 "--workspace", str(self.root), "--source-only"],
                                cwd=self.directory, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PDFs were not checked", result.stdout)

    def test_source_only_does_not_clear_stale_attachment(self):
        self.render()
        self.source.write_text(FIXTURE.replace("Python, SQL", "Python, SQL, spreadsheets"))
        self.assertTrue(all(result["status"] == "pass" for result in audit(self.root, source_only=True)))
        self.assertIn("differs", self.failures()[0]["error"])

    def test_source_only_enforces_required_disclosure_without_letter_pdf(self):
        path, relative = self.packet()
        (path / "packet.json").write_text(json.dumps({"company": "Example Company", "title": "Engineer", "required_disclosure": "disclosure.txt"}))
        manifest = load_manifest(self.root)
        manifest["letters"].append({"packet": relative, "pdf": relative + "/cover-letter.pdf"})
        self.save_manifest(manifest)
        results = audit(self.root, source_only=True)
        self.assertTrue(any(result["status"] == "fail" for result in results))
        (path / "disclosure.txt").write_text("Required fictional disclosure.")
        self.assertTrue(all(result["status"] == "pass" for result in audit(self.root, source_only=True)))
        self.assertFalse((path / "cover-letter.pdf").exists())

    def test_identity_and_notes_in_pdf(self):
        self.render()
        reader = PdfReader(self.pdf)
        text = "\n".join(page.extract_text() for page in reader.pages)
        self.assertIn("Alex Example", text)
        self.assertNotIn("PRIVATE_NOTES_SENTINEL", text)
        self.assertNotIn("Editing notes", text)
        self.assertEqual(reader.metadata.author, "Alex Example")
        self.assertEqual(reader.metadata.title, "Alex Example Resume")

    def test_different_candidate_without_fixed_employers_or_education(self):
        self.source.write_text(FIXTURE.replace("Alex Example", "Casey Sample").replace("alex@example.com", "casey@example.org")
                               .replace("Software engineer", "Product designer")
                               .replace("Example Cooperative: Software Engineer, 2020-2024", "Independent portfolio, 2024-2025"))
        self.render()
        self.assertEqual(self.failures(), [])
        self.assertEqual(PdfReader(self.pdf).metadata.author, "Casey Sample")

    def test_contact_links_escape_markup(self):
        self.assertEqual(text_markup("Data < ML & APIs"), "Data &lt; ML &amp; APIs")
        self.assertIn('href="mailto:casey@example.org"', text_markup("casey@example.org"))
        self.assertIn('href="https://example.org"', text_markup("https://example.org."))
        self.assertIn("&quot;", text_markup('https://example.org/"bad'))

    def test_source_boundaries_fail_closed(self):
        for text in (FIXTURE.replace(END, "Notes"), FIXTURE + START,
                     END + "\n" + FIXTURE.replace(END, "Notes"), "plain text"):
            with self.subTest(text=text[:30]), self.assertRaises(ValueError):
                resume_content(text)

    def test_empty_or_incomplete_submission_fails(self):
        for text in ("", "{{NAME}}", "[TODO: fill]", "[CANDIDATE: confirm]", "[CONFIRM: metric]"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                check_text(text, {})
        self.source.write_text(FIXTURE.replace("Alex Example", "{{NAME}}"))
        with self.assertRaisesRegex(ValueError, "placeholder"):
            self.render()
        self.assertFalse(self.pdf.exists())

    def test_output_needs_explicit_overwrite(self):
        self.pdf.write_bytes(b"original")
        with self.assertRaises(FileExistsError):
            self.render()
        self.assertEqual(self.pdf.read_bytes(), b"original")
        render_resume(self.root, self.source, self.pdf, self.config, overwrite=True)
        self.assertTrue(self.pdf.read_bytes().startswith(b"%PDF"))

    def test_overflow_preserves_previous_output(self):
        self.pdf.write_bytes(b"original")
        self.source.write_text(FIXTURE.replace("## Skills", ("- More detail about a fictional task and its limitations.\n" * 160) + "\n## Skills"))
        with self.assertRaisesRegex(ValueError, "limit"):
            render_resume(self.root, self.source, self.pdf, self.config, overwrite=True)
        self.assertEqual(self.pdf.read_bytes(), b"original")
        self.assertEqual(list(self.pdf.parent.glob(".render-*.pdf")), [])

    def test_configurable_pages_and_a4(self):
        self.config["paper_size"] = "A4"
        self.config["resume_max_pages"] = 3
        self.source.write_text(FIXTURE.replace("## Skills", ("- Another short fictional accomplishment.\n" * 45) + "\n## Skills"))
        self.render()
        reader = PdfReader(self.pdf)
        self.assertGreater(len(reader.pages), 1)
        self.assertLessEqual(len(reader.pages), 3)
        self.assertAlmostEqual(float(reader.pages[0].mediabox.width), 595.2756, places=2)

    def test_output_suffix_and_symlink_rules(self):
        with self.assertRaises(ValueError):
            render_resume(self.root, self.source, self.root / "bad.txt", self.config)
        target = self.root / "target.pdf"
        target.write_bytes(b"original")
        self.pdf.symlink_to(target)
        with self.assertRaises(ValueError):
            render_resume(self.root, self.source, self.pdf, self.config, overwrite=True)
        self.assertEqual(target.read_bytes(), b"original")

    def test_unconfigured_unicode_fails_instead_of_replacing_characters(self):
        self.source.write_text(FIXTURE.replace("Alex Example", "李 Example"))
        with self.assertRaisesRegex(ValueError, "Unicode fonts"):
            self.render()
        self.assertFalse(self.pdf.exists())

    def test_configured_unicode_font_and_missing_glyph(self):
        # Reportlab ships licensed test fonts, no host font or personal data dependency.
        import reportlab
        fontdir = Path(reportlab.__file__).parent / "fonts"
        for name in ("Vera.ttf", "VeraBd.ttf"):
            shutil.copyfile(fontdir / name, self.root / "profile" / name)
        self.config["fonts"] = {"regular": "profile/Vera.ttf", "bold": "profile/VeraBd.ttf"}
        # Select a non-cp1252 character covered by the bundled font.
        from reportlab.pdfbase.ttfonts import TTFont
        chars = TTFont("ProbeFixture", str(fontdir / "Vera.ttf")).face.charToGlyph
        character = next(chr(code) for code in (0x100, 0x131, 0x17F, 0x3A9) if code in chars)
        self.source.write_text(FIXTURE.replace("Alex Example", character + " Example"))
        self.render()
        self.assertIn(character, PdfReader(self.pdf).pages[0].extract_text())
        self.source.write_text(FIXTURE.replace("Alex Example", "李 Example"))
        original = self.pdf.read_bytes()
        with self.assertRaisesRegex(ValueError, "missing characters"):
            render_resume(self.root, self.source, self.pdf, self.config, overwrite=True)
        self.assertEqual(self.pdf.read_bytes(), original)

    def test_stale_pdf_is_rejected(self):
        self.render()
        self.source.write_text(FIXTURE.replace("Python, SQL", "Python, SQL, spreadsheets"))
        self.assertIn("differs", self.failures()[0]["error"])

    def test_pdf_extra_text_is_rejected(self):
        self.render()
        with self.assertRaisesRegex(ValueError, "differs"):
            check_pdf(self.pdf, "A different source", 2)

    def test_tailored_identity_drift_is_rejected(self):
        self.render()
        folder = self.root / "applications/example/role"
        folder.mkdir(parents=True)
        source = folder / "resume.md"
        source.write_text(FIXTURE.replace("Alex Example", "Another Person"))
        render_resume(self.root, source, folder / "resume.pdf", self.config)
        manifest = load_manifest(self.root)
        manifest["resumes"].append({"key": "role", "source": "applications/example/role/resume.md", "pdf": "applications/example/role/resume.pdf"})
        self.save_manifest(manifest)
        self.assertIn("identity", self.failures()[0]["error"])

    def test_answer_mirrors_and_limits(self):
        (self.root / "answers.md").write_text("## Why this role?\n\nA clear answer.\n\n## Private notes\n\nNot submission copy.\n")
        (self.root / "answer.txt").write_text("A clear answer.\n")
        entry = {"source": "answers.md", "heading": "Why this role?", "text": "answer.txt", "max_words": 3}
        self.assertEqual(check_answer(self.root, entry)["words"], 3)
        (self.root / "answer.txt").write_text("Changed answer.")
        with self.assertRaisesRegex(ValueError, "differ"):
            check_answer(self.root, entry)
        (self.root / "answers.md").write_text("No exact heading")
        with self.assertRaisesRegex(ValueError, "heading"):
            check_answer(self.root, entry)

    def test_all_limit_types(self):
        for text, limits in (("One two three.", {"max_words": 2}), ("Short.", {"min_words": 2}),
                             ("Characters.", {"max_characters": 3}), ("First.\n\nSecond.", {"max_paragraphs": 1}),
                             ("One sentence.", {"sentences": 2})):
            with self.subTest(limits=limits), self.assertRaises(ValueError):
                check_text(text, limits)
        check_text("See https://example.com/page. It is useful.", {"sentences": 2})

    def test_manifest_validation(self):
        good = load_manifest(self.root)
        entry = good["resumes"][0]
        cases = [None, [], {}, {**good, "schema_version": 2}, {**good, "resumes": "bad"},
                 {**good, "resumes": [None]}, {**good, "resumes": [entry, entry]},
                 {**good, "resumes": [{**entry, "pdf": "../escaped.pdf"}]},
                 {**good, "text_artifacts": [{"text": "answer.txt", "max_words": True}]},
                 {**good, "text_artifacts": [{"text": "answer.txt", "min_words": 10, "max_words": 2}]},
                 {**good, "letters": [{"packet": "example", "pdf": entry["pdf"]}]}]
        for manifest in cases:
            with self.subTest(manifest=manifest):
                self.save_manifest(manifest)
                self.assertEqual(self.failures()[0]["asset"], "workspace configuration")
        self.save_manifest({"schema_version": 1, "resumes": [], "answer_pairs": [], "text_artifacts": [], "letters": []})
        self.assertEqual(load_manifest(self.root)["resumes"], [])

    def test_invalid_settings(self):
        for change in ({"paper_size": "legal"}, {"resume_max_pages": True}, {"letter_max_pages": 0},
                       {"fonts": {"regular": "missing.ttf"}}, {"fonts": {"regular": "../bad", "bold": "../bad"}}):
            with self.subTest(change=change):
                (self.root / "profile/settings.json").write_text(json.dumps({**self.config, **change}))
                with self.assertRaises(ValueError):
                    settings(self.root)

    def test_local_paths_cannot_escape(self):
        for path in ("../outside", str(self.directory / "outside"), "", None):
            with self.subTest(path=path), self.assertRaises(ValueError):
                local(self.root, path, must_exist=False)
        (self.root / "outside").symlink_to(self.directory, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "escapes"):
            local(self.root, "outside/file", must_exist=False)

    def test_artifact_coverage_and_archive_exclusion(self):
        self.render()
        (self.root / "applications/unknown.txt").write_text("Unregistered.")
        self.assertIn("Unregistered", self.failures()[0]["error"])
        (self.root / "applications/unknown.txt").unlink()
        archive = self.root / "applications/example/role/archive"
        archive.mkdir(parents=True)
        (archive / "old.pdf").write_bytes(b"history")
        self.assertEqual(self.failures(), [])

    def test_local_links_and_missing_pdf_do_not_abort_audit(self):
        self.render()
        (self.root / "profile/links.md").write_text("[Base](resume.md) [Public](https://example.org)\n")
        self.assertEqual(self.failures(), [])
        (self.root / "profile/links.md").write_text("[Broken](missing.md)\n")
        self.pdf.unlink()
        errors = self.failures()
        self.assertEqual(len(errors), 2)
        self.assertEqual(errors[-1]["asset"], "local links")

    def test_session_checkpoint_links_are_checked(self):
        self.render()
        (self.root / "session.md").write_text("[Base](profile/resume.md)\n")
        self.assertEqual(self.failures(), [])
        (self.root / "session.md").write_text("[Missing](profile/missing.md)\n")
        self.assertIn("Broken or outside-workspace link", self.failures()[0]["error"])

    def test_older_workspace_can_be_validated_without_a_checkpoint(self):
        self.render()
        (self.root / "session.md").unlink()
        self.assertEqual(self.failures(), [])

    def test_session_checkpoint_cannot_be_a_symlink(self):
        self.render()
        checkpoint = self.root / "session.md"
        checkpoint.unlink()
        checkpoint.symlink_to(self.source)
        self.assertTrue(any("session checkpoint" in result["error"] for result in self.failures()))

    def test_letter_identity_and_required_disclosure(self):
        path, relative = self.packet()
        (path / "packet.json").write_text(json.dumps({"company": "Example Company", "title": "Engineer", "required_disclosure": "disclosure.txt"}))
        (path / "disclosure.txt").write_text("I used AI to refine this application.")
        output = build(self.root, relative)
        reader = PdfReader(output)
        text = reader.pages[0].extract_text()
        self.assertIn("Alex Example", text)
        self.assertIn("I used AI to refine this application.", text)
        self.assertEqual(reader.metadata.author, "Alex Example")
        with self.assertRaises(FileExistsError):
            build(self.root, relative)
        self.render()
        manifest = load_manifest(self.root)
        manifest["letters"].append({"packet": relative, "pdf": relative + "/cover-letter.pdf"})
        self.save_manifest(manifest)
        self.assertEqual(self.failures(), [])
        (path / "cover-letter.txt").write_text("Changed letter.")
        self.assertIn("differs", self.failures()[0]["error"])

    def test_missing_or_placeholder_disclosure_fails(self):
        path, relative = self.packet()
        metadata = {"company": "Example Company", "title": "Engineer", "required_disclosure": "disclosure.txt"}
        (path / "packet.json").write_text(json.dumps(metadata))
        with self.assertRaises(ValueError):
            build(self.root, relative)
        (path / "disclosure.txt").write_text("{{DISCLOSURE}}")
        with self.assertRaisesRegex(ValueError, "placeholder"):
            build(self.root, relative)
        metadata["required_disclosure"] = "../../../profile/voice.md"
        (path / "packet.json").write_text(json.dumps(metadata))
        with self.assertRaisesRegex(ValueError, "escapes"):
            build(self.root, relative)

    def test_letter_overflow_preserves_existing_output(self):
        path, relative = self.packet()
        output = build(self.root, relative)
        original = output.read_bytes()
        (path / "cover-letter.txt").write_text(("A long fictional letter paragraph. " * 80 + "\n\n") * 10)
        with self.assertRaises(ValueError):
            build(self.root, relative, overwrite=True)
        self.assertEqual(output.read_bytes(), original)
        self.assertEqual(list(path.glob(".render-*.pdf")), [])

    def test_cli_end_to_end_from_another_directory(self):
        def run(script, *args):
            return subprocess.run([sys.executable, str(ROOT / script), "--workspace", str(self.root), *args],
                                  cwd=self.directory, capture_output=True, text=True)
        listed = run("build_resume.py", "--list")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertIn("base: profile/resume.md", listed.stdout)
        built = run("build_resume.py", "--key", "base")
        self.assertEqual(built.returncode, 0, built.stderr)
        before = self.pdf.read_bytes()
        preview = run("build_resume.py", "--key", "base", "--output", "previews/test.pdf")
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertEqual(self.pdf.read_bytes(), before)
        checked = run("validate_materials.py", "--json")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertTrue(json.loads(checked.stdout)["ok"])
        self.assertNotIn("Alex Example", checked.stdout)
        self.assertNotEqual(run("build_resume.py", "--key", "missing").returncode, 0)
        self.assertNotEqual(run("build_resume.py", "--key", "base", "--output", "../escape.pdf").returncode, 0)
        self.assertNotEqual(run("build_resume.py", "--list", "--key", "base").returncode, 0)
        path, relative = self.packet()
        letter = run("build_cover_letter.py", "--packet", relative)
        self.assertEqual(letter.returncode, 0, letter.stderr)
        self.assertTrue((path / "cover-letter.pdf").exists())


if __name__ == "__main__":
    unittest.main()
