"""Helper functions for parsing homepages."""

from typing import Dict, List
from urllib.parse import urlparse, urlunparse


def markdown_to_rag_input(markdown_content: str) -> List[Dict[str, str]]:
    """Process Markdown to create structured data."""
    sections = []
    current_title = None
    print(markdown_content)
    # Iterate through lines to group headers and paragraphs
    for line in markdown_content.splitlines():
        line = line.strip()
        if line.startswith("#"):  # Headers in Markdown start with '#'
            current_title = line.lstrip("# ").strip()
        elif line and current_title:  # Non-empty lines are paragraphs
            sections.append({"title": current_title, "text": line})
    return sections


def sanitize_url(url: str):
    """Sanitize a url to include https."""
    # Parse the URL
    parsed_url = urlparse(url)

    # Ensure the scheme is set to 'https'
    scheme = parsed_url.scheme or "https"

    # Ensure the netloc (domain) is correct
    if not parsed_url.netloc:
        # Handle cases where the domain is part of the path (e.g., "elea.health")
        netloc = parsed_url.path
        path = ""
    else:
        netloc = parsed_url.netloc
        path = parsed_url.path

    # Rebuild the sanitized URL
    sanitized_url = urlunparse((scheme, netloc, path, "", "", ""))
    return sanitized_url
