"""Tests for the server."""
import pytest
from fastapi.testclient import TestClient

from backend.backend import MLBackend

QUESTION = "How is life?"
ANSWER = "Pretty good lately."

class BackendMock(MLBackend): # noqa: D101
    def process_audio(self, file):  # noqa: D102
        return QUESTION
    def process_url(self, url):  # noqa: D102
        return ""
    def process_rag(self, information, query):  # noqa: D102
        return ANSWER

@pytest.fixture
def client():
    """Return a test client."""
    return TestClient(BackendMock().app)

def test_process_audio(client):
    """Tests communication with the backend."""
    # Simulate the file upload and form data as in a `curl` request
    test_wav_file = b'test'
    url_text = "elea.health"

    response = client.post(
        "/process-audio/",
        files={"file": ("test_audio.wav", test_wav_file, "audio/wav")},
        data={"url": url_text},
    )

    # Assert the response status code
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Parse the response JSON
    response_json = response.json()

    # Assert the response content
    assert  response_json["question"] == QUESTION
    assert  response_json["answer"] == ANSWER
