#!/usr/bin/env python3
"""Check private workspace artifacts. Never submit, upload, or print their contents."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from material_content import (check_answer, check_text, letter_content, load_manifest,
                              local, normalize, resume_content, resume_identity,
                              resume_text, settings)

ROOT = Path(__file__).resolve().parent


def check_pdf(path, expected, max_pages):
    from pypdf import PdfReader
    reader = PdfReader(path)
    if not 1 <= len(reader.pages) <= max_pages:
        raise ValueError(f"PDF exceeds configured limit of {max_pages} pages or is empty")
    actual = "\n".join(page.extract_text() or "" for page in reader.pages)
    if normalize(actual) != normalize(expected):
        raise ValueError("PDF text differs from source (missing, extra, or reordered content)")
    return {"pages": len(reader.pages)}


def current_files(root):
    root = Path(root).resolve()
    checkpoint = root / "session.md"
    if checkpoint.is_symlink():
        raise ValueError("Symlinks aren't supported for the session checkpoint")
    if checkpoint.is_file():
        yield checkpoint
    for folder in ("profile", "applications", "research"):
        directory = root / folder
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            relative = path.relative_to(root)
            if "archive" in relative.parts or any(part.startswith(".") for part in relative.parts):
                continue
            if path.is_symlink():
                raise ValueError("Symlinks aren't supported in current workspace material")
            if path.is_file():
                yield path


def check_coverage(root, manifest):
    declared = {local(root, item["pdf"], must_exist=False).resolve() for item in manifest["resumes"] + manifest["letters"]}
    declared.update(local(root, item["text"], must_exist=False).resolve()
                    for item in manifest["answer_pairs"] + manifest["text_artifacts"])
    for path in current_files(root):
        if path.suffix in {".pdf", ".txt"} and path.resolve() not in declared:
            # Packet disclosure sources are inputs, not independently uploaded artifacts.
            if path.suffix == ".txt" and (path.parent / "packet.json").is_file():
                from material_content import read_json
                packet = read_json(path.parent / "packet.json")
                disclosure = packet.get("required_disclosure")
                if disclosure and local(path.parent, disclosure).resolve() == path.resolve():
                    continue
                if path.name == "cover-letter.txt" and any(
                    local(root, item["packet"] + "/packet.json").parent == path.parent
                    for item in manifest["letters"]
                ):
                    continue
            raise ValueError(f"Unregistered artifact: {path.relative_to(root)}")


def check_links(root):
    root = Path(root).resolve()
    for source in current_files(root):
        if source.suffix != ".md":
            continue
        for target in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", source.read_text(encoding="utf-8")):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = (source.parent / unquote(parsed.path)).resolve()
            if not path.is_relative_to(root) or not path.exists():
                raise ValueError(f"Broken or outside-workspace link in {source.relative_to(root)}")


def audit(root, *, source_only=False):
    root = Path(root).resolve()
    try:
        manifest, config = load_manifest(root), settings(root)
    except (ValueError, OSError) as exc:
        return [{"asset": "workspace configuration", "status": "fail", "error": str(exc)}]
    results = []

    def record(asset, check):
        try:
            detail = check()
            results.append({"asset": asset, "status": "pass", **(detail or {})})
        except Exception as exc:
            # PDF parsers have several exception types. Preserve the rest of the audit.
            # Do not include parser exception text, it can quote private source contents.
            error = str(exc) if isinstance(exc, (ValueError, OSError)) else type(exc).__name__
            results.append({"asset": asset, "status": "fail", "error": error})

    def resume(item):
        content = resume_content(local(root, item["source"]).read_text(encoding="utf-8"))
        base = resume_content(local(root, "profile/resume.md").read_text(encoding="utf-8"))
        if resume_identity(content) != resume_identity(base):
            raise ValueError("Resume identity differs from the base resume")
        if source_only:
            return {"pdf_checked": False}
        return check_pdf(local(root, item["pdf"]), resume_text(content), config["resume_max_pages"])

    def letter(item):
        metadata, paragraphs, identity = letter_content(root, item["packet"])
        if source_only:
            return {"pdf_checked": False}
        expected = "\n".join([*identity, metadata["company"] + " | " + metadata["title"], *paragraphs])
        return check_pdf(local(root, item["pdf"]), expected, config["letter_max_pages"])

    for item in manifest["resumes"]:
        record(item["key"], lambda item=item: resume(item))
    for item in manifest["letters"]:
        record(item["pdf"], lambda item=item: letter(item))
    for item in manifest["answer_pairs"]:
        record(item["text"], lambda item=item: check_answer(root, item))
    for item in manifest["text_artifacts"]:
        record(item["text"], lambda item=item: check_text(local(root, item["text"]).read_text(encoding="utf-8"), item))
    record("artifact coverage", lambda: check_coverage(root, manifest))
    record("local links", lambda: check_links(root))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=ROOT / "private")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--source-only", action="store_true",
                        help="Check source structure and text without PDF dependencies or PDF checks")
    args = parser.parse_args()
    results = audit(args.workspace, source_only=args.source_only)
    ok = all(result["status"] == "pass" for result in results)
    scope = "source-only" if args.source_only else "full"
    if args.json:
        print(json.dumps({"ok": ok, "scope": scope, "results": results}, indent=2))
    else:
        if args.source_only:
            print("Source-only validation. PDFs were not checked.")
        for result in results:
            print(f"{result['status'].upper()}: {result['asset']} {result.get('error', '')}".rstrip())
        print("Checks don't verify facts, visual layout, employer policy, or submission status.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
