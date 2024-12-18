"""Defines beautifulsoup homepage parsing class."""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from homepageparser.parser_interface import HomepageParser
from homepageparser.utils import sanitize_url


class BeautifulsoupParser(HomepageParser):
    """Class to parse homepage information."""

    def __init__(self):
        """Init the webdriver."""
        super().__init__()

        # Set up Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode for efficiency
        options.add_argument("--lang=en-US")  # Set language preference to English

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the webdriver."""
        self.driver.quit()  # Clean up when exiting the context

    def parse(self, url: str):
        """Parse the page using a webdriver and bs4."""
        # Load the webpage
        self.driver.get(sanitize_url(url))

        # Wait for the page to load (you can adjust time or use WebDriverWait for specific elements)
        self.driver.implicitly_wait(10)

        # Get the rendered HTML
        rendered_html = self.driver.page_source

        return self.parse_response(rendered_html)

    def parse_response(self, response: str):
        """Not used."""
        # Parse the HTML with BeautifulSoup.
        soup = BeautifulSoup(response, "html.parser")

        # Extract headings and paragraphs.
        content = []
        # Track if an element was already visited.
        visited = set()
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span']):
            if tag not in visited:
                text = tag.get_text(strip=True)
                if text:  # Only include non-empty text
                    content.append(text)
                # Mark all child tags as visited.
                visited.update(tag.find_all(True))

        return "\n".join(content)
