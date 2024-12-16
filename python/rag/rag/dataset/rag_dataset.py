"""Class to define a RAG dataset."""

from dataclasses import dataclass
from typing import Dict, List

import faiss
import torch
from datasets import Dataset, Features, Sequence, Value
from transformers import DPRContextEncoder, DPRContextEncoderTokenizerFast

device = "cuda" if torch.cuda.is_available() else "cpu"


@dataclass
class RagDatasetConfig:
    """Contains all dataset configurations needed."""

    # Size of the text snippets.
    text_chunk_size = 100
    # Overlap of the chunks.
    text_chunk_overlap = 20
    # The batch size to use when computing the passages embeddings using the DPR context encoder.
    dpr_context_encoder_batch_size: int = 16
    # The dimension of the embeddings to pass to the HNSW Faiss index
    index_hnsw_args_d: int = 768
    # The number of bi-directional links created for every new element during the HNSW index construction
    index_hnsw_args_m: int = 128
    # The context encoder name
    context_encoder_name = "facebook/dpr-ctx_encoder-multiset-base"


class RagDataset:
    """Defines a dataset used for input to RAG models."""

    def __init__(self, dataset_config: RagDatasetConfig = RagDatasetConfig()):
        """Construct the RagDataset class."""
        self.cfg = dataset_config

        self.ctx_encoder = DPRContextEncoder.from_pretrained(self.cfg.context_encoder_name)
        self.ctx_tokenizer = DPRContextEncoderTokenizerFast.from_pretrained(self.cfg.context_encoder_name)

    def create_dataset(self, context: List[Dict[str, str]]):
        """Create a dataset based on titles and texts."""
        # Create dataset based on chunked context information
        chunked_context = self.process_context_to_chunks(context)
        dataset = Dataset.from_dict(
            {
                "title": [chunk["title"] for chunk in chunked_context],
                "text": [chunk["text"] for chunk in chunked_context],
            }
        )

        # Compute embeddings
        new_features = Features(
            {
                "text": Value("string"),
                "title": Value("string"),
                "embeddings": Sequence(Value("float32")),
            }
        )  # optional, save as float32 instead of float64 to save space
        dataset = dataset.map(
            lambda batch: self.generate_embedding(
                batch,
                ctx_encoder=self.ctx_encoder,
                ctx_tokenizer=self.ctx_tokenizer,
            ),
            batched=True,
            batch_size=self.cfg.dpr_context_encoder_batch_size,
            features=new_features,
        )

        # Let's use the Faiss implementation of HNSW for fast approximate nearest neighbor search
        index = faiss.IndexHNSWFlat(
            self.cfg.index_hnsw_args_d,
            self.cfg.index_hnsw_args_m,
            faiss.METRIC_INNER_PRODUCT,
        )
        dataset.add_faiss_index("embeddings", custom_index=index)

        return dataset

    def process_context_to_chunks(self, context: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Divide the text into smaller chunks."""
        chunked_context = []
        for section in context:
            print(section["text"])

            text = section["text"].split(" ")
            chunks = [
                " ".join(text[i : i + self.cfg.text_chunk_size]).strip()
                for i in range(0, len(text), self.cfg.text_chunk_size)
            ]

            for chunk in chunks:
                chunked_context.append({"title": section["title"], "text": chunk})

        return chunked_context

    @staticmethod
    def generate_embedding(
        documents: dict,
        ctx_encoder: DPRContextEncoder,
        ctx_tokenizer: DPRContextEncoderTokenizerFast,
    ) -> dict:
        """Compute the DPR embeddings of document passages."""
        input_ids = ctx_tokenizer(
            documents["title"],
            documents["text"],
            truncation=True,
            padding="longest",
            return_tensors="pt",
        )["input_ids"]
        embeddings = ctx_encoder(input_ids.to(device=device), return_dict=True).pooler_output
        return {"embeddings": embeddings.detach().cpu().numpy()}
