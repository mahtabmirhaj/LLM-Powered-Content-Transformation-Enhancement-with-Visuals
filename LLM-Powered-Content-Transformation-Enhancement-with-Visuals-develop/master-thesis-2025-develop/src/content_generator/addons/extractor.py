import abc
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from content_generator.prompts.rag import RAG_PROMT
from content_generator.prompts.picture_extractor import PICTURE_EXTRACT


class Extractor(abc.ABC):
    @abc.abstractmethod
    def extract(self, search_information: str, context: Any) -> str:
        pass


class LLMExtractor(Extractor):
    def __init__(self, model: BaseChatModel) -> None:
        super().__init__()
        self._model = model

    def extract(self, search_information: str, context: Any) -> str:
        messages = [
            self._make_system_message_(context),
            HumanMessage(content=search_information),
        ]

        response = self._model.invoke(messages)
        return response.content

    @abc.abstractmethod
    def _make_system_message_(self, context: Any):
        """strategy for system message"""


class AsistantExtractor(LLMExtractor):
    def _make_system_message_(self, context: str):
        return SystemMessage(content=RAG_PROMT.format(CONTEXT=context))


class PictureExtractor(LLMExtractor):
    def _make_system_message_(self, context: Any):
        return SystemMessage(
            content=[
                {"type": "text", "text": PICTURE_EXTRACT},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{context}"},
                },
            ],
        )


if __name__ == "__main__":
    from content_generator.multi_agent.models.model_provider import model

    context = """
           The Eiffel Tower (/ˈaɪfəl/ EYE-fəl; French: Tour Eiffel [tuʁ ɛfɛl]) is a wrought-iron
           lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel,
           whose company designed and built the tower from 1887 to 1889
        """
    e = AsistantExtractor(
        model,
    )
    res = e.extract("When tower was built?", context)
    print(res)
