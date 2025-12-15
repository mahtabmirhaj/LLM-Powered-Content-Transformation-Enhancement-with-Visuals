from typing import TypedDict


class ChapterState(TypedDict):
    nds_path: str
    excel_path: str
    free_text: str
    meta: dict[str, str]
    generated_chapter: str


class GenerationOutput(TypedDict):
    generated_chapter: str
    corporate_style_chapter: str
    official_markdown: str


class BaseState(ChapterState, GenerationOutput):
    pass
