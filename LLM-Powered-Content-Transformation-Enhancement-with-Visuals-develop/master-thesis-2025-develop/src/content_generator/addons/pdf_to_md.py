import pathlib

import pymupdf4llm


def parse_to_md(pdf_path: str) -> str:
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return md_text


def save_md(md_text: str, md_path: str):
    pathlib.Path(md_path).write_bytes(md_text.encode())
    print(f"# Markdown file saved to: {md_path}")
