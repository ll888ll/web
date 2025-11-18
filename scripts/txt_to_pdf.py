#!/usr/bin/env python3
"""
Simple text-to-PDF converter without external dependencies.
Usage: scripts/txt_to_pdf.py <input.txt> <output.pdf>
"""

import io
import sys
import textwrap
from pathlib import Path


PAGE_WIDTH = 612  # 8.5in * 72
PAGE_HEIGHT = 792  # 11in * 72
MARGIN = 54  # 0.75in
LINE_HEIGHT = 14
FONT_SIZE = 11
WRAP_WIDTH = 90


def escape_pdf(text: str) -> str:
    return (
        text.replace("\\", r"\\")
        .replace("(", r"\(")
        .replace(")", r"\)")
        .replace("\r", "")
    )


def wrap_text(text: str, width: int = WRAP_WIDTH) -> list[str]:
    wrapped: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.replace("\t", "    ")
        items = textwrap.wrap(line, width=width, drop_whitespace=False) or [""]
        wrapped.extend(items)
    if not wrapped:
        wrapped.append("")
    return wrapped


def markdown_to_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        stripped = raw.rstrip()
        if not stripped:
            lines.append("")
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[level:].strip()
            if not title:
                continue
            if level == 1:
                heading = title.upper()
                lines.extend(["", heading, "=" * len(heading), ""])
            else:
                heading = title
                lines.extend(["", heading, "-" * len(heading), ""])
            continue

        if stripped.startswith(("-", "*", "+")) and len(stripped) > 1:
            content = stripped[1:].strip()
            bullet = f"- {content}"
            lines.extend(wrap_text(bullet))
            continue

        if stripped.startswith(">"):
            content = stripped[1:].strip()
            quote = f"\"{content}\""
            lines.extend(wrap_text(quote))
            continue

        if set(stripped) == {"-"}:
            lines.extend(["", "-" * 20, ""])
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            lines.append(stripped)
            continue

        lines.extend(wrap_text(stripped))

    if not lines:
        lines.append("")
    return lines


def plain_text_lines(text: str) -> list[str]:
    return wrap_text(text)


def prepare_lines(text: str, is_markdown: bool) -> list[str]:
    return markdown_to_lines(text) if is_markdown else plain_text_lines(text)


def chunk_lines(lines: list[str]) -> list[list[str]]:
    usable_height = PAGE_HEIGHT - 2 * MARGIN
    max_lines = max(1, int(usable_height // LINE_HEIGHT))
    return [lines[i : i + max_lines] for i in range(0, len(lines), max_lines)]


def build_page_stream(lines: list[str]) -> bytes:
    y = PAGE_HEIGHT - MARGIN
    parts = ["BT", f"/F1 {FONT_SIZE} Tf"]
    for line in lines:
        safe = escape_pdf(line if line else " ")
        parts.append(f"1 0 0 1 {MARGIN} {int(y)} Tm ({safe}) Tj")
        y -= LINE_HEIGHT
    parts.append("ET")
    content = "\n".join(parts) + "\n"
    data = content.encode("latin-1")
    header = f"<< /Length {len(data)} >>\nstream\n".encode("latin-1")
    footer = b"endstream\n"
    return header + data + footer


def build_pdf_objects(pages: list[bytes]) -> list[bytes]:
    objects: list[bytes] = []
    # Placeholder for catalog and pages; will append actual bytes later.
    # We know font object number beforehand.
    num_pages = len(pages)
    font_obj_num = 3 + 2 * num_pages
    page_obj_nums = [3 + 2 * i for i in range(num_pages)]
    content_obj_nums = [4 + 2 * i for i in range(num_pages)]

    # Catalog (object 1)
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")

    # Pages (object 2) - kids references page objects.
    kids = " ".join(f"{ref} 0 R" for ref in page_obj_nums)
    pages_dict = f"<< /Type /Pages /Kids [{kids}] /Count {num_pages} >>"
    objects.append(pages_dict.encode("latin-1"))

    # Page + content objects
    for idx, stream in enumerate(pages):
        page_obj_num = page_obj_nums[idx]
        content_obj_num = content_obj_nums[idx]
        page_dict = (
            "<< /Type /Page "
            "/Parent 2 0 R "
            "/MediaBox [0 0 612 792] "
            "/Resources << /Font << /F1 {font} 0 R >> >> "
            "/Contents {content} 0 R >>"
        ).format(font=font_obj_num, content=content_obj_num)
        objects.append(page_dict.encode("latin-1"))
        objects.append(stream)

    # Font object
    font_dict = b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>"
    objects.append(font_dict)
    return objects


def write_pdf(objects: list[bytes], output_path: Path) -> None:
    buffer = io.BytesIO()
    buffer.write(b"%PDF-1.4\n")
    offsets = [0]

    for idx, obj in enumerate(objects, start=1):
        offsets.append(buffer.tell())
        buffer.write(f"{idx} 0 obj\n".encode("latin-1"))
        buffer.write(obj)
        if not obj.endswith(b"\n"):
            buffer.write(b"\n")
        buffer.write(b"endobj\n")

    xref_pos = buffer.tell()
    total = len(objects) + 1
    buffer.write(f"xref\n0 {total}\n".encode("latin-1"))
    buffer.write(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        buffer.write(f"{off:010d} 00000 n \n".encode("latin-1"))
    buffer.write(
        f"trailer << /Size {total} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode(
            "latin-1"
        )
    )
    output_path.write_bytes(buffer.getvalue())


def convert(txt_path: Path, pdf_path: Path) -> None:
    text = txt_path.read_text(encoding="utf-8")
    is_markdown = txt_path.suffix.lower() in {".md", ".markdown"}
    lines = prepare_lines(text, is_markdown=is_markdown)
    page_lines = chunk_lines(lines)
    streams = [build_page_stream(chunk) for chunk in page_lines]
    objects = build_pdf_objects(streams)
    write_pdf(objects, pdf_path)


def main(argv: list[str]) -> None:
    if len(argv) not in (2, 3):
        print("Usage: scripts/txt_to_pdf.py <input.txt> <output.pdf>", file=sys.stderr)
        raise SystemExit(1)
    txt_path = Path(argv[1])
    pdf_path = Path(argv[2]) if len(argv) == 3 else txt_path.with_suffix(".pdf")
    if not txt_path.is_file():
        print(f"Input file not found: {txt_path}", file=sys.stderr)
        raise SystemExit(1)
    convert(txt_path, pdf_path)
    print(f"PDF generado en {pdf_path}")


if __name__ == "__main__":
    main(sys.argv)
