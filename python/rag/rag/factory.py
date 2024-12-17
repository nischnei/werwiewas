"""Factory for homepageparsers."""

from typing import Literal, Type

from rag.llmware import LlmwareRag
from rag.rag_interface import RagInterface

# not yet properly tested:
# from rag.chatpgt import ChatGptRag
# from rag.hugging_face import HuggingFace


class RagFactory:
    """Factory class for rag modules."""

    @staticmethod
    def get(rag_type: Literal["llmware"]) -> Type[RagInterface]:
        """Return a homepage parser given a string."""
        if rag_type == "llmware":
            return LlmwareRag()
        else:
            raise NotImplementedError(f"Type {rag_type} not supported.")
