"""Class defning rag based on llmware api."""

from llmware.prompts import Prompt

from rag.rag_interface import RagInterface


class LlmwareRag(RagInterface):
    """The LlmwareRag class."""

    def __init__(self):
        """Construct the LlmwareRag class."""
        model_name = "bling-phi-3-gguf"
        self.prompter = Prompt().load_model(model_name)

    def query_context(self, context: str, query: str, **kwargs) -> str:
        """Overwritten query context function."""
        output = self.prompter.prompt_main(
            prompt=query, context=context, prompt_name="default_with_context", temperature=0.30
        )

        return output["llm_response"]
