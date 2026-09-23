#!/usr/bin/env python3
"""Check the reusable publication file set and local links, not candidate truth."""
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
LOCAL_DIRECTORIES = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "private",
                     ".agents", ".claude", ".codex", ".cursor", ".opencode", ".pi"}
LOCAL_FILES = {"CLAUDE.md", ".mcp.json", ".DS_Store"}


def check(root):
    root = Path(root).resolve()
    errors = []
    try:
        allowed = json.loads((root / "starter-files.json").read_text(encoding="utf-8"))
        if not isinstance(allowed, list) or any(not isinstance(p, str) for p in allowed):
            raise ValueError("Expected a list of relative publication paths")
        if len(allowed) != len(set(allowed)):
            raise ValueError("Duplicate publication path")
        if "AGENTS.md" not in allowed:
            raise ValueError("Publication set must include the canonical AGENTS.md")
        for value in allowed:
            path = Path(value)
            if (path.is_absolute() or ".." in path.parts or not path.parts
                    or any(part in LOCAL_DIRECTORIES for part in path.parts)
                    or path.name in LOCAL_FILES or path.suffix.lower() == ".pdf"
                    or path.name.startswith(".env")):
                raise ValueError("Unsafe publication path")
        allowed = set(allowed)
    except (ValueError, OSError) as exc:
        return [str(exc)]

    found = set()
    for directory, children, names in os.walk(root):
        parent = Path(directory)
        for name in list(children):
            path = parent / name
            if path.is_symlink():
                errors.append(f"Symlink directory in starter: {path.relative_to(root)}")
        children[:] = sorted(name for name in children if name not in LOCAL_DIRECTORIES
                             and not (parent / name).is_symlink())
        for name in names:
            path = parent / name
            relative = path.relative_to(root).as_posix()
            if relative in LOCAL_FILES:
                continue
            if path.is_symlink():
                errors.append(f"Symlink file in starter: {relative}")
                continue
            found.add(relative)
    for path in sorted(found - allowed):
        errors.append(f"Unexpected publication file: {path}")
    for path in sorted(allowed - found):
        errors.append(f"Missing publication file: {path}")

    if (root / ".git").exists():
        result = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=False)
        if result.returncode:
            errors.append("Couldn't inspect tracked publication files")
        else:
            tracked = set(result.stdout.decode().rstrip("\0").split("\0")) - {""}
            for path in sorted(tracked - allowed):
                errors.append(f"Tracked file outside publication set: {path}")

    for value in sorted(allowed & found):
        path = root / value
        if path.suffix not in {".md", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".json":
            try:
                json.loads(text)
            except ValueError:
                errors.append(f"Invalid JSON: {value}")
            continue
        for target in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", text):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                errors.append(f"Broken local link: {value} -> {target}")
        if value == "AGENTS.md" and not text.strip():
            errors.append("Canonical AGENTS.md is empty")
        if path.name == "SKILL.md":
            expected_name = path.parent.name
            if not text.startswith(f"---\nname: {expected_name}\ndescription: ") or "\n---\n" not in text[4:]:
                errors.append(f"Invalid skill frontmatter: {value}")
    return errors


def main():
    errors = check(ROOT)
    for error in errors:
        print("FAIL: " + error)
    if not errors:
        print("PASS: reusable file set, skill frontmatter, JSON, and local file links")
    print("This isn't a personal-data scanner. Inspect contents and history before publishing.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
