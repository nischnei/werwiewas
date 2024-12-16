"""Hugging face rag implementation."""

from homepageparser.utils import markdown_to_rag_input
from transformers import RagRetriever, RagSequenceForGeneration, RagTokenizer

from rag.dataset.rag_dataset import RagDataset, RagDatasetConfig
from rag.rag_interface import RagInterface

DEFAULT_MODEL = "facebook/rag-sequence-nq"


class HuggingFace(RagInterface):
    """Hugging Face RAG implementation."""

    def __init__(self, pretrained_model_name=DEFAULT_MODEL):
        """Construct the Hugging Face Rag class."""
        super().__init__()
        self.pretrained_model_name: str = pretrained_model_name
        rag_datset_cfg = RagDatasetConfig()
        self.dataset = RagDataset(dataset_config=rag_datset_cfg)

        self.tokenizer = RagTokenizer.from_pretrained(self.pretrained_model_name)

    def query_context(self, context: str, query: str):
        """Query a list of strings."""
        # Markdown to List[Dict[str, str]]
        context = markdown_to_rag_input(markdown_content=context)

        # Step 1: build the dataset
        dataset = self.dataset.create_dataset(context=context)

        # Step 2: Load the dataset into the rag retriever
        retriever = RagRetriever.from_pretrained(
            retriever_name_or_path=self.pretrained_model_name, index_name="custom", indexed_dataset=dataset
        )
        model = RagSequenceForGeneration.from_pretrained(self.pretrained_model_name, retriever=retriever)

        # Step 3: Retrieve the answer
        input_ids = self.tokenizer.question_encoder(query, return_tensors="pt")["input_ids"]
        generated = model.generate(input_ids)
        generated_string = self.tokenizer.batch_decode(generated, skip_special_tokens=True)[0]

        return generated_string
