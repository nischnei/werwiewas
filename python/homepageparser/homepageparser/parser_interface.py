"""Parse homepage information with HomepageParser class."""

from abc import ABC, abstractmethod

import requests

from homepageparser.utils import sanitize_url


class HomepageParser(ABC):
    """Class to parse homepage information."""

    def __init__(self):
        """Init the session."""
        self.session = requests.Session()
        # Header to be able to access more homepages, otherwise requests get blocked often.
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

    def parse(self, url: str) -> str:
        """Parse the homepage information from a url as markdown."""
        # Fetch the homepage HTML content
        response = self.session.get(sanitize_url(url))
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch the URL. Status code: {response.status_code}"
            )

        return self.parse_response(response)

    @abstractmethod
    def parse_response(response: requests.Response) -> str:
        """Parse the html response, has to be overwritten by inherited class."""
        pass
