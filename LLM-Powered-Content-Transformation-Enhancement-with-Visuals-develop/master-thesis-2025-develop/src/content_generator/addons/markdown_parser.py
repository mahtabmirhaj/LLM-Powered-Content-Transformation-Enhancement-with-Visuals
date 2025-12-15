import pathlib

from markdown_it import MarkdownIt


def load_markdown(file_path: str) -> str:
    with pathlib.Path(file_path).open("r", encoding="utf-8") as file:
        return file.read()


def cut_to_chapter(markdown_doc: str, stop_chapter: str) -> str:
    md = MarkdownIt()
    tokens = md.parse(markdown_doc)

    collected_content = []
    for token in tokens:
        if token.type == "heading_open":
            title_token = tokens[tokens.index(token) + 1]
            title = title_token.content
            if stop_chapter in title:
                break

        collected_content.append(token.content if token.type == "inline" else token.markup)

    return "".join(collected_content)
