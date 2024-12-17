"""Tests for the server."""

import pytest
from fastapi import File, Form, UploadFile
from fastapi.testclient import TestClient

from backend.backend import MLBackend

QUESTION = "Who is the business lead of elea?"
HOMEPAGE = """top of page
Start Vision Team Contact Members Mehr
Use tab to navigate through the menu items.
We shape the future of healthcare
Deeply embedded Artificial Intelligence in healthcare
elea represents the forefront of AI technology, tailored and deeply integrated to support healthcare provider workflows 
and significantly enhance medical care, ensuring that clinicians remain in control with real-time data and decision 
support. With its intuitive design optimized for mobile devices, operating elea becomes an immersive experience. 
It facilitates the easy management and supervision of all essential aspects of clinical care from admission to 
diagnosis, treatment, and discharge.
Our Team
Our vision
Saving millions of lives.
With elea, we save lives.
The most advanced artificial intelligence in healthcare supports the optimization of diagnostic and therapeutic 
treatment procedures, assists with documentation, and enables doctors to focus on what they do best: saving lives.
With elea, healthcare professionals can focus on patients and ensure that they receive the best treatment.
We shape the future of healthcare.
Core Team
Dr. Christoph Schröder CEO
Software business leader, decade long leadership experience in high tech research and development.
Dr. med. Sebastian Casu CMO
Medical thought leader, medical director and industry influencer with decade long experience.
Tobias Lygren Tech Lead
Technologist, Software and AI industry leader with experience delivering innovative and high quality products as startup
founder.
Stephan Frank Business Lead
Accomplished business and product leader with in-depth expertise in data protection and legal regulations.
If you have any further questions, please do not hesitate to contact us!"""
ANSWER = "Stephan Frank"


class BackendMock(MLBackend):  # noqa: D101
    def init_homepage_parser(self):
        """Basically do nothing here."""
        pass

    def init_speech_recognition(self):
        """Basically do nothing here."""
        pass

    def register_routes(self):
        """Register routes with decorators."""

        @self.app.post("/process-audio/")
        async def process_audio(file: UploadFile = File(...), url: str = Form(...)):
            return {"question": QUESTION}

        @self.app.post("/process-url/")
        async def process_url(url: str = Form(...)):
            """Step 2: Fetch homepage content."""
            return {"homepage": HOMEPAGE}

        @self.app.post("/process-rag/")
        async def process_rag(homepage: str = Form(...), query: str = Form(...)):
            """Step 3: Generate an answer using RAG."""
            response = self.rag.query_context(context=homepage, query=query)
            return {"answer": response.encode("utf-8")}


@pytest.fixture
def client():
    """Return a test client."""
    backend = BackendMock()
    with TestClient(backend.app) as test_client:
        yield test_client


def test_audio_communication_mocked(client):
    """Tests communication with the backend."""
    # Simulate the file upload and form data as in a `curl` request
    test_wav_file = b"test"
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
    assert response_json["question"] == QUESTION


def test_homepage_parsing_communication_mocked(client):
    """Tests communication with the backend."""
    # Simulate the file upload and form data as in a `curl` request
    url_text = "elea.health"

    response = client.post(
        "/process-url/",
        data={"url": url_text},
    )

    # Assert the response status code
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Parse the response JSON
    response_json = response.json()

    # Assert the response content
    assert response_json["homepage"] == HOMEPAGE


def test_rag_processing_and_communication_regression(client):
    """Tests communication with the backend."""
    # Simulate the file upload and form data as in a `curl` request
    response = client.post(
        "/process-rag/",
        data={
            "homepage": HOMEPAGE,
            "query": QUESTION,
        },
    )

    # Assert the response status code
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Parse the response JSON
    response_json = response.json()

    # Assert the response content
    assert ANSWER in response_json["answer"]
