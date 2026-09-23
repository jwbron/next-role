#!/usr/bin/env python3
"""Render a letter with required disclosures. Never send it."""
import argparse
from pathlib import Path

from material_content import letter_content, local, settings

ROOT = Path(__file__).resolve().parent


def build(root, packet, output=None, *, overwrite=False):
    from resume_renderer import render_letter
    metadata, paragraphs, identity = letter_content(root, packet)
    destination = local(root, output or packet + "/cover-letter.pdf", must_exist=False)
    return render_letter(root, metadata, paragraphs, identity, destination, settings(root), overwrite=overwrite)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=ROOT / "private")
    parser.add_argument("--packet", required=True, help="Role directory relative to the workspace")
    parser.add_argument("--output", help="Preview path relative to the workspace")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        print(build(args.workspace, args.packet, args.output, overwrite=args.overwrite))
    except ImportError:
        parser.exit(1, "Install requirements.txt in a Python virtual environment first.\n")
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    main()
