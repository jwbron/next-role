#!/usr/bin/env python3
"""Package only reviewed publication files, excluding personal workspaces and history."""
import argparse
import json
import os
from pathlib import Path
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

from check_starter import ROOT, check


def export(root, output):
    root = Path(root).resolve()
    output = Path(output).absolute()
    if output.is_symlink() or output.exists():
        raise FileExistsError("Export destination already exists. Choose a new filename.")
    if output.suffix.lower() != ".zip" or output.resolve().is_relative_to(root):
        raise ValueError("Choose a .zip destination outside the starter directory")
    errors = check(root)
    if errors:
        raise ValueError("Starter checks failed:\n" + "\n".join(errors))
    paths = json.loads((root / "starter-files.json").read_text(encoding="utf-8"))
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".starter-export-", suffix=".zip", dir=output.parent)
    os.close(fd)
    temporary = Path(name)
    try:
        with ZipFile(temporary, "w", compression=ZIP_DEFLATED) as archive:
            for value in sorted(paths):
                archive.write(root / value, "next-role/" + value)
        os.link(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        print(export(ROOT, args.output))
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc) + "\n")
    print("Only listed starter files were packaged. Review their contents before publishing.")


if __name__ == "__main__":
    main()
