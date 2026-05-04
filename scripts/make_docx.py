from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]


def paragraph_xml(text: str) -> str:
    text = text.rstrip()
    if not text:
        return "<w:p/>"

    style = ""
    content = text
    if text.startswith("# "):
        style = '<w:pPr><w:pStyle w:val="Title"/></w:pPr>'
        content = text[2:]
    elif text.startswith("## "):
        style = '<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
        content = text[3:]
    elif text.startswith("### "):
        style = '<w:pPr><w:pStyle w:val="Heading2"/></w:pPr>'
        content = text[4:]
    elif text.startswith("- "):
        content = f"• {text[2:]}"

    return f"<w:p>{style}<w:r><w:t xml:space=\"preserve\">{escape(content)}</w:t></w:r></w:p>"


def markdown_to_docx(markdown_path: Path, docx_path: Path) -> None:
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    body = []
    in_code = False
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            body.append(paragraph_xml(f"    {line}"))
            continue
        if line.startswith("|"):
            body.append(paragraph_xml(line))
            continue
        body.append(paragraph_xml(line))

    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {''.join(body)}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>"""

    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:rPr><w:b/><w:sz w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:rPr><w:b/><w:sz w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:rPr><w:b/><w:sz w:val="24"/></w:rPr>
  </w:style>
</w:styles>"""

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(docx_path, "w", ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", rels)
        docx.writestr("word/_rels/document.xml.rels", doc_rels)
        docx.writestr("word/document.xml", document)
        docx.writestr("word/styles.xml", styles)


def main() -> None:
    pairs = [
        ("docs/RoadSense_AI_Software_Impacts_Paper.md", "docs/RoadSense_AI_Software_Impacts_Paper.docx"),
        ("docs/Project_Report.md", "docs/RoadSense_AI_Project_Report.docx"),
    ]
    for source, target in pairs:
        markdown_to_docx(ROOT / source, ROOT / target)


if __name__ == "__main__":
    main()
