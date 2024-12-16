"""Parse homepage information with HomepageParser class."""

import html2text
import requests

from homepageparser.parser_interface import HomepageParser


class Html2TextParser(HomepageParser):
    """Class to parse homepage information with html2text module."""

    def parse_response(self, response: requests.Response) -> str:
        """Parse the homepage information from a url as markdown."""
        # Fetch the homepage HTML content
        parser = html2text.HTML2Text()
        parser.ignore_images = True
        parser.ignore_links = True
        parser.ignore_mailto_links = True
        parser.ignore_emphasis = True

        return parser.handle(response.text)
