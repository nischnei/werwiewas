"""Defines a ChatGPT version of a RAG."""

import os

import openai

from rag.rag_interface import RagInterface


class ChatGptRag(RagInterface):
    """Retrieval augmented generation using ChatGpt prompts."""

    def __init__(self):
        """Construct the ChatGptRag class."""
        super().__init__()

        self.openai.api_key = os.environ("OPENAI_KEY")

    def query_context(self, context, query, **kwargs):
        """Query a certain context using a user query."""
        # Query GPT with the extracted content and the user's query
        prompt = f"Extract relevant information based on the following query: '{query}'.\n\nWebsite content:\n{context}"

        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use 'gpt-4' or 'gpt-3.5-turbo' based on your subscription
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        # Extract and return the GPT response
        return response["choices"][0]["message"]["content"]
