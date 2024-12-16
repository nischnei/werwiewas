"""Defines the RagInterface class."""

from abc import ABC, abstractmethod


class RagInterface(ABC):
    """Abstract base class for rag classes."""

    @abstractmethod
    def query_context(self, context: str, query: str, **kwargs) -> str:
        """Abstract method to query context, must be implemented by derived classes."""
        pass
