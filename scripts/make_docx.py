from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]


def image_xml(rel_id: str, alt: str) -> str:
    return f"""
<w:p>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="5486400" cy="3135600"/>
        <wp:docPr id="1" name="{escape(alt)}"/>
        <a:graphic>
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic>
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="{escape(alt)}"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rel_id}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="5486400" cy="3135600"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>"""


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
        content = f"- {text[2:]}"

    content = content.replace("**", "")
    return f"<w:p>{style}<w:r><w:t xml:space=\"preserve\">{escape(content)}</w:t></w:r></w:p>"


def markdown_to_docx(markdown_path: Path, docx_path: Path, two_column: bool = False) -> None:
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    body = []
    images = []
    in_code = False
    for line in lines:
        if line.startswith("![") and "](" in line and line.endswith(")"):
            alt = line[2:].split("](", 1)[0]
            image_ref = line.split("](", 1)[1][:-1]
            image_path = (markdown_path.parent / image_ref).resolve()
            if image_path.exists():
                rel_id = f"rId{len(images) + 2}"
                media_name = f"image{len(images) + 1}{image_path.suffix}"
                images.append((rel_id, image_path, media_name, alt))
                body.append(image_xml(rel_id, alt))
                continue
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

    columns_xml = '<w:cols w:num="2" w:space="720"/>' if two_column else ""
    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
  xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
  xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>
    {''.join(body)}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720"/>
      {columns_xml}
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
  <Default Extension="svg" ContentType="image/svg+xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    image_rels = "\n".join(
        f'  <Relationship Id="{rel_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{media_name}"/>'
        for rel_id, _image_path, media_name, _alt in images
    )
    doc_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>""".replace("</Relationships>", f"{image_rels}\n</Relationships>")

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(docx_path, "w", ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", rels)
        docx.writestr("word/_rels/document.xml.rels", doc_rels)
        docx.writestr("word/document.xml", document)
        docx.writestr("word/styles.xml", styles)
        for _rel_id, image_path, media_name, _alt in images:
            docx.write(image_path, f"word/media/{media_name}")


def markdown_to_html(markdown_path: Path, html_path: Path, two_column: bool = False) -> None:
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    if two_column:
        css = (
            "body{font-family:'Times New Roman',serif;max-width:1100px;margin:28px auto;"
            "line-height:1.25;color:#111;font-size:14px;column-count:2;column-gap:34px;text-align:justify}"
            "h1{font-size:24px;text-align:center;column-span:all;margin-bottom:8px}"
            "h2{font-size:15px;text-transform:uppercase;border:0;text-align:left;break-after:avoid}"
            "h3{font-size:14px;font-style:italic;break-after:avoid}"
            "p,li{break-inside:avoid}pre,table,img{break-inside:avoid;column-span:all}"
            "img{max-width:100%;display:block;margin:8px auto}pre{background:#f4f6f7;padding:10px;overflow:auto;text-align:left}"
            "code{font-family:Consolas,monospace}table{border-collapse:collapse;width:100%;font-size:12px}"
            "td,th{border:1px solid #777;padding:5px;text-align:left}"
        )
    else:
        css = (
            "body{font-family:Arial,sans-serif;max-width:900px;margin:40px auto;line-height:1.55;color:#172124}"
            "h1{font-size:32px}h2{font-size:24px;border-bottom:1px solid #ddd;padding-bottom:4px}"
            "h3{font-size:19px}pre{background:#f4f6f7;padding:14px;border-radius:6px;overflow:auto}"
            "code{background:#f4f6f7;padding:2px 4px;border-radius:4px}table{border-collapse:collapse;width:100%}"
            "td,th{border:1px solid #ccc;padding:8px;text-align:left}img{max-width:100%;display:block;margin:16px auto}"
        )
    html = [
        "<!doctype html>",
        "<html><head><meta charset=\"utf-8\"><title>RoadSense AI Report</title>",
        f"<style>{css}</style>",
        "</head><body>",
    ]
    in_code = False
    table_rows = []

    def flush_table() -> None:
        if not table_rows:
            return
        html.append("<table>")
        for row in table_rows:
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            if set("".join(cells)) <= {"-", ":", " "}:
                continue
            tag = "th" if not any("<tr>" in item for item in html[-1:]) else "td"
            html.append("<tr>" + "".join(f"<{tag}>{escape(cell)}</{tag}>" for cell in cells) + "</tr>")
        html.append("</table>")
        table_rows.clear()

    for line in lines:
        if line.startswith("```"):
            flush_table()
            html.append("</pre>" if in_code else "<pre>")
            in_code = not in_code
            continue
        if in_code:
            html.append(escape(line))
            continue
        if line.startswith("|"):
            table_rows.append(line)
            continue
        flush_table()
        display_line = line.replace("**", "")
        if line.startswith("![") and "](" in line and line.endswith(")"):
            alt = line[2:].split("](", 1)[0]
            image_ref = line.split("](", 1)[1][:-1]
            html.append(f"<img src=\"{escape(image_ref)}\" alt=\"{escape(alt)}\">")
        elif line.startswith("# "):
            html.append(f"<h1>{escape(display_line[2:])}</h1>")
        elif line.startswith("## "):
            html.append(f"<h2>{escape(display_line[3:])}</h2>")
        elif line.startswith("### "):
            html.append(f"<h3>{escape(display_line[4:])}</h3>")
        elif line.startswith("- "):
            html.append(f"<ul><li>{escape(display_line[2:])}</li></ul>")
        elif not line.strip():
            html.append("<br>")
        else:
            html.append(f"<p>{escape(display_line)}</p>")
    flush_table()
    html.append("</body></html>")
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text("\n".join(html), encoding="utf-8")


def markdown_to_rtf(markdown_path: Path, rtf_path: Path) -> None:
    text = markdown_path.read_text(encoding="utf-8")
    escaped = text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
    escaped = escaped.replace("\n", "\\par\n")
    rtf = "{\\rtf1\\ansi\\deff0{\\fonttbl{\\f0 Arial;}}\\fs22\n" + escaped + "\n}"
    rtf_path.parent.mkdir(parents=True, exist_ok=True)
    rtf_path.write_text(rtf, encoding="utf-8")


def main() -> None:
    pairs = [
        ("docs/RoadSense_AI_Software_Impacts_Paper.md", "docs/RoadSense_AI_Software_Impacts_Paper.docx"),
        ("docs/Project_Report.md", "docs/RoadSense_AI_Project_Report.docx"),
        ("docs/separate/01_Project_Customization_Report.md", "docs/separate/RoadSense_AI_Project_Customization_Report.docx"),
        ("docs/separate/02_Inference_and_API_Report.md", "docs/separate/RoadSense_AI_Inference_and_API_Report.docx"),
        ("docs/separate/03_Docker_and_GitHub_Report.md", "docs/separate/RoadSense_AI_Docker_GitHub_Report.docx"),
        ("docs/separate/04_Kubernetes_Deployment_Report.md", "docs/separate/RoadSense_AI_Kubernetes_Report.docx"),
        ("docs/separate/05_Software_Paper_Work.md", "docs/separate/RoadSense_AI_Software_Paper_Work.docx"),
        ("docs/separate/06_Final_Compiled_Report.md", "docs/separate/RoadSense_AI_Final_Compiled_Report.docx"),
    ]
    for source, target in pairs:
        is_ieee_paper = source.endswith("RoadSense_AI_Software_Impacts_Paper.md")
        markdown_to_docx(ROOT / source, ROOT / target, two_column=is_ieee_paper)

    for source, target in pairs:
        markdown = ROOT / source
        output_base = ROOT / target
        is_ieee_paper = source.endswith("RoadSense_AI_Software_Impacts_Paper.md")
        markdown_to_html(markdown, output_base.with_suffix(".html"), two_column=is_ieee_paper)
        markdown_to_rtf(markdown, output_base.with_suffix(".rtf"))


if __name__ == "__main__":
    main()
