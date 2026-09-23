"""Read workspace content without rendering, network access, or candidate defaults."""
import json
from pathlib import Path
import re

START = "## Contact and summary\n"
END = "## Editing notes, not resume content"
SECTIONS = {
    "resumes": ("key", "source", "pdf"),
    "answer_pairs": ("source", "heading", "text"),
    "text_artifacts": ("text",),
    "letters": ("packet", "pdf"),
}


def local(root, value, *, must_exist=True):
    if not isinstance(value, str) or not value.strip() or Path(value).is_absolute():
        raise ValueError("Expected a nonempty relative path")
    root = Path(root).resolve()
    path = root / value
    if not path.resolve().is_relative_to(root):
        raise ValueError(f"Path escapes workspace: {value}")
    if must_exist and not path.is_file():
        raise ValueError(f"Missing file: {value}")
    return path


def complete_text(text):
    if not text.strip():
        raise ValueError("Empty submission text")
    if re.search(r"\{\{[^{}]*\}\}|\[(?:TODO|CANDIDATE|CONFIRM|COMPANY):[^\]]*\]", text, re.I):
        raise ValueError("Unresolved placeholder in submission text")
    return text.strip()


def resume_content(text):
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError("Resume needs one content start and one editing-notes boundary")
    if text.index(END) < text.index(START):
        raise ValueError("Editing notes precede resume content")
    content = complete_text(text.split(START, 1)[1].split(END, 1)[0])
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if len(lines) < 4 or any(line.startswith(("#", "- ")) for line in lines[:3]):
        raise ValueError("Resume starts with name, contact, and summary on separate lines")
    if not any(line.startswith("## ") for line in lines[3:]):
        raise ValueError("Resume needs at least one section heading")
    return content


def resume_identity(content):
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    return lines[0], lines[1]


def resume_text(content):
    return "\n".join(re.sub(r"^(?:### |## )", "", line) for line in content.splitlines())


def normalize(text):
    return " ".join(text.replace("\u2022", "").split())


def read_json(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {Path(path).name}")
    return value


def settings(root):
    value = read_json(local(root, "profile/settings.json"))
    if value.get("paper_size") not in ("letter", "A4"):
        raise ValueError("paper_size must be letter or A4")
    for field in ("resume_max_pages", "letter_max_pages"):
        if type(value.get(field)) is not int or not 1 <= value[field] <= 10:
            raise ValueError(f"{field} must be an integer from 1 to 10")
    fonts = value.get("fonts", {})
    if not isinstance(fonts, dict) or (fonts and set(fonts) != {"regular", "bold"}):
        raise ValueError("fonts must be empty or contain regular and bold file paths")
    for font in fonts.values():
        local(root, font)
    return value


def load_manifest(root):
    manifest = read_json(local(root, "resume-manifest.json"))
    if manifest.get("schema_version") != 1:
        raise ValueError("Unsupported manifest schema")
    outputs, keys = set(), set()
    for section, fields in SECTIONS.items():
        entries = manifest.get(section)
        if not isinstance(entries, list):
            raise ValueError(f"Manifest {section} must be a list")
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(f"Invalid {section} entry")
            for field in fields:
                if not isinstance(entry.get(field), str) or not entry[field].strip():
                    raise ValueError(f"{section} entry needs {field}")
                if field in {"source", "pdf", "text", "packet"}:
                    local(root, entry[field], must_exist=False)
            output = local(root, entry[fields[-1]], must_exist=False).resolve()
            if output in outputs:
                raise ValueError("Duplicate manifest output")
            outputs.add(output)
            if section == "resumes":
                if entry["key"] in keys:
                    raise ValueError("Duplicate resume key")
                keys.add(entry["key"])
            for limit in ("min_words", "max_words", "max_characters", "max_paragraphs", "sentences"):
                if limit in entry and (type(entry[limit]) is not int or entry[limit] < 1):
                    raise ValueError(f"Invalid {limit}")
            if entry.get("min_words", 1) > entry.get("max_words", float("inf")):
                raise ValueError("Inconsistent word limits")
    return manifest


def letter_content(root, packet_value):
    packet = local(root, packet_value + "/packet.json").parent
    metadata = read_json(packet / "packet.json")
    for field in ("company", "title"):
        if not isinstance(metadata.get(field), str):
            raise ValueError(f"Packet needs {field}")
        complete_text(metadata[field])
    paragraphs = re.split(r"\n\s*\n", complete_text(local(packet, "cover-letter.txt").read_text(encoding="utf-8")))
    if "required_disclosure" in metadata:
        disclosure = local(packet, metadata["required_disclosure"])
        paragraphs.extend(re.split(r"\n\s*\n", complete_text(disclosure.read_text(encoding="utf-8"))))
    identity = resume_identity(resume_content(local(root, "profile/resume.md").read_text(encoding="utf-8")))
    return metadata, paragraphs, identity


def check_text(text, item):
    text = complete_text(text)
    counts = {"words": len(text.split()), "characters": len(text),
              "paragraphs": len(re.split(r"\n\s*\n", text))}
    for limit, key in (("max_words", "words"), ("max_characters", "characters"),
                       ("max_paragraphs", "paragraphs")):
        if limit in item and counts[key] > item[limit]:
            raise ValueError(f"Answer exceeds {limit}")
    if "min_words" in item and counts["words"] < item["min_words"]:
        raise ValueError("Answer is below min_words")
    if "sentences" in item:
        prose = re.sub(r"https?://[^\s)]+", lambda m: "URL" + (m[0][-1] if m[0][-1] in ".!?" else ""), text)
        count = len(re.findall(r"[.!?](?:[\"')\]]*)(?:\s+|$)", prose))
        if count != item["sentences"]:
            raise ValueError("Sentence count differs from requirement, review manually")
    return counts


def check_answer(root, item):
    source = local(root, item["source"]).read_text(encoding="utf-8")
    marker = "## " + item["heading"] + "\n\n"
    if source.count(marker) != 1:
        raise ValueError("Answer heading missing or ambiguous")
    answer = source.split(marker, 1)[1].split("\n## ", 1)[0].strip()
    paste = local(root, item["text"]).read_text(encoding="utf-8").strip()
    if answer != paste:
        raise ValueError("Combined draft and text file differ")
    return check_text(answer, item)
