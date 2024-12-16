"""Server running with uvicorn."""

import uvicorn

from backend.backend import MLBackend

app = MLBackend().app


def main():
    """Start and run the server."""
    uvicorn.run("backend.server:app", host="127.0.0.1", port=8000, reload=True)
