"""Render the documented markdown subset. Publish only complete, checked PDFs."""
from hashlib import sha256
from html import escape
import os
from pathlib import Path
import re
import tempfile

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

from material_content import local, resume_content, resume_identity, resume_text


def text_markup(text):
    """Escape authored markup. Link plain HTTPS URLs and email addresses."""
    tokens = re.split(r"(https://[^\s<>]+|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,})", text)
    result = []
    for token in tokens:
        if token.startswith("https://") or re.fullmatch(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", token):
            clean = token.rstrip(".,)")
            href = clean if clean.startswith("https://") else "mailto:" + clean
            result.append(f'<link href="{escape(href, quote=True)}" color="#0563C1">{escape(clean)}</link>' + escape(token[len(clean):]))
        else:
            result.append(escape(token))
    return "".join(result)


def fonts_for(root, config, text):
    fonts = config.get("fonts", {})
    if fonts:
        names = []
        for weight in ("regular", "bold"):
            path = local(root, fonts[weight])
            name = "CandidateFont" + sha256(path.read_bytes()).hexdigest()[:16]
            if name not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(name, str(path)))
            supported = pdfmetrics.getFont(name).face.charToGlyph
            missing = {char for char in text if not char.isspace() and ord(char) not in supported}
            if missing:
                raise ValueError(f"Configured {weight} font is missing characters. Choose a font covering your text.")
            names.append(name)
        return tuple(names)
    try:
        text.encode("cp1252")
    except UnicodeEncodeError as exc:
        raise ValueError("Text needs Unicode fonts. Configure regular and bold TrueType fonts in profile/settings.json.") from exc
    return "Helvetica", "Helvetica-Bold"


def styles(root, config, text):
    regular, bold = fonts_for(root, config, text)
    body = ParagraphStyle("body", fontName=regular, fontSize=10.5, leading=14, spaceAfter=5)
    return {
        "body": body,
        "name": ParagraphStyle("name", parent=body, fontName=bold, fontSize=17, leading=21, spaceAfter=4),
        "section": ParagraphStyle("section", parent=body, fontName=bold, spaceBefore=8, keepWithNext=True),
        "title": ParagraphStyle("title", parent=body, fontName=bold, spaceBefore=4, keepWithNext=True),
        "bullet": ParagraphStyle("bullet", parent=body, leftIndent=12, bulletIndent=1),
    }


def make_story(content, style):
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    story = []
    for index, line in enumerate(lines):
        if index == 0:
            story.append(Paragraph(text_markup(line), style["name"]))
        elif line.startswith("### "):
            story.append(Paragraph(text_markup(line[4:]), style["title"]))
        elif line.startswith("## "):
            story.append(Paragraph(text_markup(line[3:]), style["section"]))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceAfter=4))
        elif line.startswith("- "):
            story.append(Paragraph(text_markup(line[2:]), style["bullet"], bulletText="-"))
        else:
            story.append(Paragraph(text_markup(line), style["body"]))
    return story


def publish_pdf(story, output, *, config, author, title, expected, max_pages, overwrite=False):
    from validate_materials import check_pdf
    output = Path(output).absolute()
    if output.suffix.lower() != ".pdf" or output.is_symlink():
        raise ValueError("Output must be a regular .pdf path")
    if output.exists() and not overwrite:
        raise FileExistsError("Output exists. Use --overwrite deliberately.")
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".render-", suffix=".pdf", dir=output.parent)
    os.close(fd)
    temporary = Path(name)
    try:
        document = SimpleDocTemplate(str(temporary), pagesize=A4 if config["paper_size"] == "A4" else letter,
                                     leftMargin=44, rightMargin=44, topMargin=36, bottomMargin=36,
                                     title=title, author=author)
        document.build(story)
        check_pdf(temporary, expected, max_pages)
        if overwrite:
            os.replace(temporary, output)
        else:
            os.link(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return output


def render_resume(root, source, output, config, *, overwrite=False):
    content = resume_content(Path(source).read_text(encoding="utf-8"))
    name, _ = resume_identity(content)
    style = styles(root, config, content)
    return publish_pdf(make_story(content, style), output, config=config, author=name,
                       title=name + " Resume", expected=resume_text(content),
                       max_pages=config["resume_max_pages"], overwrite=overwrite)


def render_letter(root, metadata, paragraphs, identity, output, config, *, overwrite=False):
    name, contact = identity
    heading = metadata["company"] + " | " + metadata["title"]
    expected = "\n".join([name, contact, heading, *paragraphs])
    style = styles(root, config, expected)
    story = [Paragraph(text_markup(name), style["name"]),
             Paragraph(text_markup(contact), style["body"]),
             Paragraph(text_markup(heading), style["title"]), Spacer(1, 10)]
    story.extend(Paragraph(text_markup(p.replace("\n", " ")), style["body"]) for p in paragraphs)
    return publish_pdf(story, output, config=config, author=name, title=name + " Cover Letter",
                       expected=expected, max_pages=config["letter_max_pages"], overwrite=overwrite)
