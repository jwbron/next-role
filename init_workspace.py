#!/usr/bin/env python3
"""Create a private workspace from blank templates, never overwrite an existing one."""
import argparse
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent


def initialize(destination):
    destination = Path(destination).absolute()
    # mkdir(exist_ok=False) rejects both existing directories and symlinks.
    destination.mkdir(parents=True, mode=0o700, exist_ok=False)
    for directory in ("profile", "applications", "research", "evidence", "previews"):
        (destination / directory).mkdir(mode=0o700)
    for source in sorted((ROOT / "templates" / "profile").iterdir()):
        shutil.copyfile(source, destination / "profile" / source.name)
    shutil.copyfile(ROOT / "templates" / "tracker.md", destination / "applications" / "tracker.md")
    shutil.copyfile(ROOT / "templates" / "session.md", destination / "session.md")
    (destination / ".gitignore").write_text("*\n", encoding="utf-8")
    manifest = {
        "schema_version": 1,
        "resumes": [{"key": "base", "source": "profile/resume.md", "pdf": "profile/resume.pdf"}],
        "answer_pairs": [], "text_artifacts": [], "letters": [],
    }
    (destination / "resume-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=ROOT / "private")
    args = parser.parse_args()
    try:
        print(initialize(args.workspace))
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc) + "\n")
    print("Blank workspace created. Follow AGENTS.md and the workflow selected for the candidate's request.")
    print("Ignored files are not encrypted. Keep a private backup outside the public starter.")


if __name__ == "__main__":
    main()
