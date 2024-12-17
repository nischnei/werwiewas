"""Factory for homepageparsers."""

from typing import Literal, Type

from homepageparser.beautifulsoup import BeautifulsoupParser
from homepageparser.html2text import Html2TextParser
from homepageparser.parser_interface import HomepageParser


class HomepageParserFactory:
    """Factory class for homepage parsers."""

    @staticmethod
    def get(parser_type: Literal["bs", "html2text"]) -> Type[HomepageParser]:
        """Return a homepage parser given a string."""
        if parser_type == "bs":
            return BeautifulsoupParser()
        elif parser_type == "html2text":
            return Html2TextParser()
        else:
            raise NotImplementedError(f"Type {parser_type} not supported.")
