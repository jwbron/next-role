#!/usr/bin/env python3
"""Build one registered resume, without changing the application tracker."""
import argparse
from pathlib import Path

from material_content import load_manifest, local, settings

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=ROOT / "private")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--key")
    parser.add_argument("--output", help="Preview path relative to the workspace")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        entries = load_manifest(args.workspace)["resumes"]
        if args.list:
            if args.key or args.output or args.overwrite:
                parser.error("--list doesn't accept build options")
            for item in entries:
                print(f"{item['key']}: {item['source']} -> {item['pdf']}")
            return 0
        by_key = {item["key"]: item for item in entries}
        if args.key not in by_key:
            parser.error("Choose --key from registered resumes, use --list")
        from resume_renderer import render_resume
        item = by_key[args.key]
        output = local(args.workspace, args.output or item["pdf"], must_exist=False)
        result = render_resume(args.workspace, local(args.workspace, item["source"]), output,
                               settings(args.workspace), overwrite=args.overwrite)
        print(result)
        return 0
    except ImportError:
        parser.exit(1, "Install requirements.txt in a Python virtual environment first.\n")
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
